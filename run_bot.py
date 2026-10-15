import asyncio
import os
import sys
import threading
from collections.abc import Callable, Coroutine
from typing import Any

from telegram import BotCommand, Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from config.config import Config
from health_server import set_readiness, start_health_server
from services.report_generator import ReportGenerator
from services.scheduler import SchedulerService
from services.summarizer import Summarizer
from utils.logger import setup_logger
from utils.telegram_utils import _msg, send_split_message, send_split_message_to_chat

logger = setup_logger(__name__)
report_generator = ReportGenerator()
summarizer = Summarizer()

# Backlog of pending long-running work (category reports / summaries).
_QUEUE: list[dict[str, Any]] = []
_QUEUE_LOCK = threading.Lock()
_QUEUE_TASKS: set[asyncio.Task[Any]] = set()
MAX_QUEUE_SIZE = 100  # Guard against memory exhaustion / command flooding

# Rate-limit: cooldown (s) per chat_id for broadcast / long-report replies.
BROADCAST_COOLDOWN_SECONDS = 300.0  # 5 minutes between auto-broadcasts per chat
_SENT_AT: dict[str, float] = {}

# Per-user interactive command rate limiting
USER_COMMAND_COOLDOWN_SECONDS = float(os.getenv("USER_COMMAND_COOLDOWN_SECONDS", "0.0"))
_LAST_USER_COMMAND: dict[str, float] = {}


def _is_user_throttled(chat_id: str | int | None) -> bool:
    """Return True if the user command should be throttled (SEC-002)."""
    if not chat_id or USER_COMMAND_COOLDOWN_SECONDS <= 0:
        return False
    now = asyncio.get_event_loop().time()
    key = str(chat_id)
    last = _LAST_USER_COMMAND.get(key)
    if last is not None and (now - last) < USER_COMMAND_COOLDOWN_SECONDS:
        return True
    if len(_LAST_USER_COMMAND) > 10000:
        _LAST_USER_COMMAND.clear()
    _LAST_USER_COMMAND[key] = now
    return False


def _get_command_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE | None = None,
    command_name: str = "",
) -> str:
    """Extract argument string from a command invocation."""
    if context and context.args:
        return str(" ".join(str(x) for x in context.args))
    if update.message and update.message.text:
        parts = update.message.text.split(maxsplit=1)
        if len(parts) > 1:
            return str(parts[1])
    return ""


def _queue_command(
    handler: Callable[..., Coroutine[Any, Any, None]],
    update: Update,
    context: ContextTypes.DEFAULT_TYPE | None = None,
    *args: Any,
) -> bool:
    """Fire-and-forget a long-running command: return a pending notice now,
    let a background worker finish it and post the result later."""
    global _QUEUE
    with _QUEUE_LOCK:
        if len(_QUEUE) >= MAX_QUEUE_SIZE:
            logger.warning("Queue overflow: backlog exceeded MAX_QUEUE_SIZE (%d)", MAX_QUEUE_SIZE)
            return False
        _QUEUE.append(
            {
                "handler": handler,
                "update": update,
                "context": context,
                "args": args,
            }
        )

    # Kick off the worker on the bot's event loop.
    loop = asyncio.get_running_loop()
    task = asyncio.create_task(_process_queue(loop))
    _QUEUE_TASKS.add(task)
    task.add_done_callback(_QUEUE_TASKS.discard)
    return True


async def _process_queue(loop: asyncio.AbstractEventLoop) -> None:
    """Drain the pending-work backlog without blocking the polling loop."""
    global _QUEUE
    while True:
        with _QUEUE_LOCK:
            if not _QUEUE:
                break
            item = _QUEUE.pop(0)

        try:
            await item["handler"](item["update"], item["context"], *item.get("args", []))
        except Exception:
            logger.exception("Pending command worker failed")


async def drain_queue() -> None:
    """Drain the pending-work backlog (used for testing and teardown)."""
    global _QUEUE
    while True:
        with _QUEUE_LOCK:
            if not _QUEUE:
                break
            item = _QUEUE.pop(0)

        try:
            await item["handler"](item["update"], item["context"], *item.get("args", []))
        except Exception:
            logger.exception("Pending command worker failed")


async def _broadcast_if_due(chat_id: str | None) -> None:
    """Scheduler-side helper: only broadcast once per cooldown window."""
    if not chat_id:
        return
    now = asyncio.get_event_loop().time()
    last = _SENT_AT.get(chat_id)
    if last is not None and (now - last) < BROADCAST_COOLDOWN_SECONDS:
        logger.debug("Auto-broadcast skipped: cooldown active for chat %s", chat_id)
        return
    _SENT_AT[chat_id] = now
    await _run_broadcast(chat_id)


async def _run_broadcast(chat_id: str) -> None:
    """Fresh `all` report, sent in small chunks with a per-pair delay."""
    try:
        logger.info("2-hour auto-refresh triggered - generating a fresh AI Daily Brief...")
        report = await report_generator.generate_report("all", force_refresh=True)
        await send_split_message_to_chat(chat_id, report)
        logger.info("Auto-broadcast sent successfully.")
    except (RuntimeError, OSError, ValueError) as e:
        logger.error(f"Auto-broadcast error: {e}")


async def _send_or_queued(update: Update, text: str | None, parse_mode: str = "Markdown") -> None:
    """Reply directly when the queue is empty; otherwise queue it for later."""
    with _QUEUE_LOCK:
        is_empty = not _QUEUE
    if is_empty:
        await send_split_message(update, text, parse_mode)
    else:
        _queue_command(generic_reply_handler, update, None)


async def generic_reply_handler(
    update: Update, context: ContextTypes.DEFAULT_TYPE | None = None
) -> None:
    """Worker callback that applies the queued reply to the original update."""
    if update.message is not None and update.message.reply_text is not None:
        await update.message.reply_text("Your request is being prepared (this may take a moment).")


def make_broadcast_callback(
    app: Application, chat_id: str, loop_holder: list
) -> Callable[[], None]:
    """Create a scheduler callback that re-queues the broadcast so the heavy
    work (scrape + summarize + send) does not run on the bot's event loop at all."""

    def callback() -> None:
        logger.info("2-hour auto-refresh triggered - generating a fresh AI Daily Brief...")
        loop = (
            loop_holder[0]
            if loop_holder and loop_holder[0] is not None
            else asyncio.get_event_loop()
        )
        if loop is None:
            logger.warning("Auto-broadcast skipped because the event loop is not ready yet.")
            return

        async def _run() -> None:
            await _broadcast_if_due(chat_id)

        # The refresh still happens on the scheduler thread - the \u201cheavy
        # work\u201d is handed off with asyncio.to_thread() so it never blocks run_polling().
        asyncio.run_coroutine_threadsafe(_run(), loop)

    return callback


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome = "*AI Daily Intelligence Bot*\n\n*Core Commands:*:\n/daily - Full daily intelligence report\n/summary - AI-powered news summary\n/tools - Discover new AI tools\n/jobs - AI-related job opportunities\n/startups - Startups and funding news\n/models - New AI model releases\n/trending - Reddit AI trends\n/learn - Learning resources\n\n*News and Content:*\n/news - Global AI news\n/papers - Research papers\n/blogs - AI blog posts\n/india - Indian AI news\n/youtube - Latest AI YouTube videos\n/twitter - Latest AI tweets\n\n*AI Intelligence Features:*\n/compare GPT-4o vs Claude vs Gemini\n/roadmap ai engineer - Step-by-step learning path\n/leaderboard - Top AI models ranked\n\n/help - Show all commands\n\n_Fresh AI updates every 2 hours._\n"
    await _msg(update).reply_text(welcome, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_command(update, context)


async def generic_command(
    update: Update, context: ContextTypes.DEFAULT_TYPE, category: str
) -> None:
    chat_id = update.effective_chat.id if update.effective_chat else None
    if _is_user_throttled(chat_id):
        await _msg(update).reply_text("Please wait a moment before sending another command.")
        return

    queued = _queue_command(generic_command_worker, update, context, category)
    if not queued:
        await _msg(update).reply_text("Server is currently busy. Please try again shortly.")
        return
    await _msg(update).reply_text("Fetching updates...")


async def generic_command_worker(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    category: str,
    *args: Any,
) -> None:
    try:
        report = await report_generator.generate_report(category)
        await send_split_message(update, report)
    except (RuntimeError, ValueError, OSError) as e:
        logger.error(f"Error in {category} command: {e}")
        await _msg(update).reply_text("Error fetching updates. Try again.")


async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await generic_command(update, context, "all")


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id if update.effective_chat else None
    if _is_user_throttled(chat_id):
        await _msg(update).reply_text("Please wait a moment before sending another command.")
        return

    queued = _queue_command(summary_command_worker, update, context)
    if not queued:
        await _msg(update).reply_text("Server is currently busy. Please try again shortly.")
        return
    await _msg(update).reply_text("Generating AI summary...")


async def summary_command_worker(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        from scrapers.news_scraper import NewsScraper

        news = await NewsScraper().fetch_news(10)
        articles = [
            article.to_dict() if hasattr(article, "to_dict") else article for article in news
        ]
        summary = await summarizer.summarize_articles(articles)
        await send_split_message(update, f"*AI News Summary*\n\n{summary}")
    except (RuntimeError, ValueError, OSError) as e:
        logger.error(f"Error in summary command: {e}")
        await _msg(update).reply_text("Error generating summary.")


async def compare_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id if update.effective_chat else None
    if _is_user_throttled(chat_id):
        await _msg(update).reply_text("Please wait a moment before sending another command.")
        return

    args = _get_command_query(update, context, "compare")
    if not args:
        await _msg(update).reply_text(
            "*Usage:* `/compare GPT-4o vs Claude vs Gemini`\n\n"
            "Supported models: GPT-4o, GPT-4.5, Claude, Gemini, Llama, DeepSeek, Mistral, Qwen, Grok",
            parse_mode="Markdown",
        )
        return

    await _msg(update).reply_text("Comparing AI models...")
    try:
        result = await report_generator.generate_compare(args)
        await send_split_message(update, result)
    except (RuntimeError, ValueError, OSError) as e:
        logger.error(f"Error in compare command: {e}")
        await _msg(update).reply_text("Error generating comparison. Try again.")


async def roadmap_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id if update.effective_chat else None
    if _is_user_throttled(chat_id):
        await _msg(update).reply_text("Please wait a moment before sending another command.")
        return

    role = _get_command_query(update, context, "roadmap") or "ai engineer"
    await _msg(update).reply_text("Building your AI roadmap...")
    try:
        result = await report_generator.generate_roadmap(role)
        await send_split_message(update, result)
    except (RuntimeError, ValueError, OSError) as e:
        logger.error(f"Error in roadmap command: {e}")
        await _msg(update).reply_text("Error generating roadmap. Try again.")


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    chat_id = update.effective_chat.id if update.effective_chat else None
    if _is_user_throttled(chat_id):
        await _msg(update).reply_text("Please wait a moment before sending another command.")
        return

    filter_term = _get_command_query(update, context, "leaderboard")
    await _msg(update).reply_text("Fetching AI model leaderboard...")
    try:
        result = await report_generator.generate_leaderboard(filter_term)
        await send_split_message(update, result)
    except (RuntimeError, ValueError, OSError) as e:
        logger.error(f"Error in leaderboard command: {e}")
        await _msg(update).reply_text("Error fetching leaderboard. Try again.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not update.message or not update.message.text:
        return

    text = update.message.text.lower().strip()
    if "summary" in text:
        await summary_command(update, context)
    elif "daily" in text or "report" in text:
        await daily_command(update, context)
    elif "tool" in text:
        await generic_command(update, context, "tools")
    elif "job" in text:
        await generic_command(update, context, "jobs")
    elif "leaderboard" in text:
        await leaderboard_command(update, context)
    elif "compare" in text or " vs " in text:
        await compare_command(update, context)
    elif "roadmap" in text:
        await roadmap_command(update, context)
    elif "news" in text:
        await generic_command(update, context, "news")
    elif "youtube" in text or "video" in text:
        await generic_command(update, context, "youtube")
    elif "twitter" in text or " x " in text or "tweet" in text:
        await generic_command(update, context, "twitter")
    else:
        await _msg(update).reply_text("Try /daily, /compare, /roadmap, /leaderboard, or /help.")


# Keep the broadcast callback signature identical for SchedulerService.
def _make_broadcast_callback(
    app: Application, chat_id: str, loop_holder: list
) -> Callable[[], None]:
    """Create a scheduler callback that re-queues the broadcast so the heavy
    work (scrape + summarize + send) does not run on the bot's event loop at all."""

    def callback() -> None:
        logger.info("2-hour auto-refresh triggered - generating a fresh AI Daily Brief...")
        loop = (
            loop_holder[0]
            if loop_holder and loop_holder[0] is not None
            else asyncio.get_event_loop()
        )
        if loop is None:
            logger.warning("Auto-broadcast skipped because the event loop is not ready yet.")
            return

        async def _run() -> None:
            await _broadcast_if_due(chat_id)

        # The refresh still happens on the scheduler thread - the \u201cheavy
        # work\u201d is handed off with asyncio.to_thread() so it never blocks run_polling().
        asyncio.run_coroutine_threadsafe(_run(), loop)

    return callback


def main() -> None:
    config = Config()
    logger.info("Starting bot...")

    if not config.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is required. Set it in your environment or .env file.")

    loop_holder: list[Any] = [None]

    async def post_init(application: Application) -> None:
        loop_holder[0] = asyncio.get_running_loop()
        set_readiness(bot_connected=True, scheduler_running=True)
        commands = [
            BotCommand("daily", "Full daily intelligence report"),
            BotCommand("summary", "AI-powered news summary"),
            BotCommand("tools", "Discover new AI tools"),
            BotCommand("jobs", "AI-related job opportunities"),
            BotCommand("startups", "Startups and funding news"),
            BotCommand("models", "New AI model releases"),
            BotCommand("trending", "Reddit AI trends"),
            BotCommand("learn", "AI learning resources"),
            BotCommand("news", "Global AI news"),
            BotCommand("papers", "AI research papers"),
            BotCommand("blogs", "AI blog posts"),
            BotCommand("india", "Indian AI news"),
            BotCommand("youtube", "AI YouTube videos"),
            BotCommand("twitter", "AI tweets"),
            BotCommand("compare", "Compare AI models"),
            BotCommand("roadmap", "AI learning paths"),
            BotCommand("leaderboard", "Top AI models ranked"),
            BotCommand("help", "Show all commands"),
        ]
        await application.bot.set_my_commands(commands)
        logger.info("Telegram menu commands set successfully.")

    async def post_stop(application: Application) -> None:
        set_readiness(bot_connected=False, scheduler_running=False)
        logger.info("Shutting down - cleaning up scrapers...")
        await report_generator.cleanup()

    app = (
        ApplicationBuilder()
        .token(config.TELEGRAM_BOT_TOKEN)
        .connect_timeout(60.0)
        .read_timeout(60.0)
        .write_timeout(60.0)
        .pool_timeout(60.0)
        .post_init(post_init)
        .post_stop(post_stop)
        .build()
    )

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("daily", daily_command))
    app.add_handler(CommandHandler("summary", summary_command))
    app.add_handler(CommandHandler("compare", compare_command))
    app.add_handler(CommandHandler("roadmap", roadmap_command))
    app.add_handler(CommandHandler("leaderboard", leaderboard_command))

    categories = [
        "tools",
        "jobs",
        "startups",
        "models",
        "trending",
        "learn",
        "news",
        "papers",
        "blogs",
        "india",
        "youtube",
        "twitter",
    ]

    def create_handler(category_name):
        async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
            await generic_command(update, context, category_name)

        return handler

    for category in categories:
        app.add_handler(CommandHandler(category, create_handler(category)))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    chat_id = config.TELEGRAM_CHAT_ID
    if not chat_id:
        logger.warning("TELEGRAM_CHAT_ID not set in .env - auto-broadcast disabled.")

    broadcast_callback = (
        make_broadcast_callback(app, chat_id, loop_holder) if chat_id else lambda: None
    )
    scheduler = SchedulerService(refresh_callback=broadcast_callback)
    scheduler.start()

    logger.info("Bot running with 2-hour auto-refresh enabled.")

    # Start the health check server in a background thread for Docker/k8s probes.
    start_health_server()

    app.run_polling()


if __name__ == "__main__":
    max_retries = 5
    retry_delay = 10  # seconds

    for attempt in range(1, max_retries + 1):
        try:
            logger.info(f"Bot starting (attempt {attempt}/{max_retries})...")
            main()
            break  # clean exit
        except SystemExit:
            logger.info("Bot stopped via SystemExit.")
            break
        except KeyboardInterrupt:
            logger.info("Bot stopped by user.")
            break
        except (RuntimeError, OSError, ValueError) as e:
            logger.error(f"Bot crashed: {e}")
            if attempt < max_retries:
                wait = retry_delay * (2 ** (attempt - 1))  # exponential backoff
                logger.info(f"Restarting in {wait}s...")
                asyncio.run(asyncio.sleep(wait))
            else:
                logger.critical("Max retries reached. Exiting.")
                sys.exit(1)
