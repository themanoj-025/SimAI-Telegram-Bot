import asyncio
import sys
import time

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
from services.report_generator import ReportGenerator
from services.scheduler import SchedulerService
from services.summarizer import Summarizer
from utils.logger import setup_logger
from utils.telegram_utils import send_split_message

logger = setup_logger(__name__)
report_generator = ReportGenerator()
summarizer = Summarizer()


def _get_command_query(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
    command_name: str = "",
) -> str:
    if context.args:
        return " ".join(context.args).strip()

    message_text = update.message.text.strip() if update.message and update.message.text else ""
    if not message_text:
        return ""

    lowered = message_text.lower()
    command_prefix = f"/{command_name.lower()}" if command_name else ""

    if command_prefix and lowered.startswith(command_prefix):
        parts = message_text.split(maxsplit=1)
        return parts[1].strip() if len(parts) > 1 else ""

    if command_name and lowered.startswith(command_name.lower()):
        return message_text[len(command_name) :].strip()

    return message_text


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    welcome = """*AI Daily Intelligence Bot*

*Core Commands:*
/daily - Full daily intelligence report
/summary - AI-powered news summary
/tools - Discover new AI tools
/jobs - AI-related job opportunities
/startups - Startups and funding news
/models - New AI model releases
/trending - Reddit AI trends
/learn - Learning resources

*News and Content:*
/news - Global AI news
/papers - Research papers
/blogs - AI blog posts
/india - Indian AI news
/youtube - Latest AI YouTube videos
/twitter - Latest AI tweets

*AI Intelligence Features:*
/compare GPT-4o vs Claude vs Gemini
/roadmap ai engineer - Step-by-step learning path
/leaderboard - Top AI models ranked

/help - Show all commands

_Fresh AI updates every 2 hours._"""
    await update.message.reply_text(welcome, parse_mode="Markdown")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await start_command(update, context)


async def generic_command(update: Update, context: ContextTypes.DEFAULT_TYPE, category: str) -> None:
    await update.message.reply_text("Fetching updates...")
    try:
        report = await report_generator.generate_report(category)
        await send_split_message(update, report)
    except Exception as e:
        logger.error(f"Error in {category} command: {e}")
        await update.message.reply_text(f"Error fetching {category}. Try again.")


async def daily_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await generic_command(update, context, "all")


async def summary_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Generating AI summary...")
    try:
        from scrapers.news_scraper import NewsScraper

        news = await NewsScraper().fetch_news(10)
        articles = [
            article.to_dict() if hasattr(article, "to_dict") else article for article in news
        ]
        summary = await summarizer.summarize_articles(articles)
        await send_split_message(update, f"*AI News Summary*\n\n{summary}")
    except Exception as e:
        logger.error(f"Error in summary command: {e}")
        await update.message.reply_text("Error generating summary.")


async def compare_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    args = _get_command_query(update, context, "compare")
    if not args:
        await update.message.reply_text(
            "*Usage:* `/compare GPT-4o vs Claude vs Gemini`\n\n"
            "Supported models: GPT-4o, GPT-4.5, Claude, Gemini, Llama, DeepSeek, Mistral, Qwen, Grok",
            parse_mode="Markdown",
        )
        return

    await update.message.reply_text("Comparing AI models...")
    try:
        result = await report_generator.generate_compare(args)
        await send_split_message(update, result)
    except Exception as e:
        logger.error(f"Error in compare command: {e}")
        await update.message.reply_text("Error generating comparison. Try again.")


async def roadmap_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    role = _get_command_query(update, context, "roadmap") or "ai engineer"
    await update.message.reply_text("Building your AI roadmap...")
    try:
        result = await report_generator.generate_roadmap(role)
        await send_split_message(update, result)
    except Exception as e:
        logger.error(f"Error in roadmap command: {e}")
        await update.message.reply_text("Error generating roadmap. Try again.")


async def leaderboard_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    filter_term = _get_command_query(update, context, "leaderboard")
    await update.message.reply_text("Fetching AI model leaderboard...")
    try:
        result = await report_generator.generate_leaderboard(filter_term)
        await send_split_message(update, result)
    except Exception as e:
        logger.error(f"Error in leaderboard command: {e}")
        await update.message.reply_text("Error fetching leaderboard. Try again.")


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
        await update.message.reply_text("Try /daily, /compare, /roadmap, /leaderboard, or /help.")


def make_broadcast_callback(app: Application, chat_id: str, loop_holder: list) -> None:
    """Create a scheduler callback that broadcasts fresh content safely from a worker thread."""

    def callback() -> None:
        logger.info("2-hour auto-refresh triggered - generating a fresh AI Daily Brief...")

        async def _run() -> None:
            try:
                report = await report_generator.generate_report("all", force_refresh=True)
                max_len = 4000
                chunks = [report[i : i + max_len] for i in range(0, len(report), max_len)]

                for chunk in chunks:
                    try:
                        await app.bot.send_message(
                            chat_id=chat_id, text=chunk, parse_mode="Markdown"
                        )
                    except Exception as e:
                        logger.error(f"Auto-broadcast chunk send failed: {e}")

                logger.info("Auto-broadcast sent successfully.")
            except Exception as e:
                logger.error(f"Auto-broadcast error: {e}")

        if loop_holder and loop_holder[0] is not None:
            asyncio.run_coroutine_threadsafe(_run(), loop_holder[0])
        else:
            logger.warning("Auto-broadcast skipped because the event loop is not ready yet.")

    return callback


def main() -> None:
    config = Config()
    logger.info("Starting bot...")

    if not config.TELEGRAM_BOT_TOKEN:
        raise ValueError("TELEGRAM_BOT_TOKEN is required. Set it in your environment or .env file.")

    loop_holder = [None]

    async def post_init(application: Application) -> None:
        loop_holder[0] = asyncio.get_running_loop()
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

    def create_handler(category_name) -> None:
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
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            if attempt < max_retries:
                wait = retry_delay * (2 ** (attempt - 1))  # exponential backoff
                logger.info(f"Restarting in {wait}s...")
                time.sleep(wait)
            else:
                logger.critical("Max retries reached. Exiting.")
                sys.exit(1)
