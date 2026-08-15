import os
import sys

# Ensure the repository root is importable regardless of where this script
# is invoked from (repo root or a subdirectory such as tests/).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

from telegram import Message, Update
from telegram.ext import ContextTypes

import run_bot


def make_update(message_text: str = "/test"):
    update = MagicMock(spec=Update)
    update.message = AsyncMock(spec=Message)
    update.message.text = message_text
    update.effective_chat.id = 123456789
    return update


async def test_basic_commands():
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []

    start_update = make_update("/start")
    await run_bot.start_command(start_update, context)
    assert start_update.message.reply_text.await_count == 1

    help_update = make_update("/help")
    await run_bot.help_command(help_update, context)
    assert help_update.message.reply_text.await_count == 1


async def test_report_commands():
    categories = [
        ("daily", "all"),
        ("tools", "tools"),
        ("jobs", "jobs"),
        ("startups", "startups"),
        ("models", "models"),
        ("trending", "trending"),
        ("learn", "learn"),
        ("news", "news"),
        ("papers", "papers"),
        ("blogs", "blogs"),
        ("india", "india"),
        ("youtube", "youtube"),
        ("twitter", "twitter"),
    ]

    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []

    with patch.object(run_bot, "send_split_message", new=AsyncMock()) as mock_send:
        with patch.object(
            run_bot.report_generator,
            "generate_report",
            new=AsyncMock(return_value="Report body"),
        ) as mock_report:
            for command_name, expected_category in categories:
                update = make_update(f"/{command_name}")
                if command_name == "daily":
                    await run_bot.daily_command(update, context)
                else:
                    await run_bot.generic_command(update, context, expected_category)
                mock_report.assert_any_await(expected_category)
            assert mock_send.await_count == len(categories)


async def test_summary_command():
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []
    update = make_update("/summary")

    fake_articles = [
        {"title": "Story A", "link": "https://example.com/a", "source": "Example"}
    ]

    with patch.object(run_bot, "send_split_message", new=AsyncMock()) as mock_send:
        with patch(
            "scrapers.news_scraper.NewsScraper.fetch_news",
            new=AsyncMock(return_value=fake_articles),
        ):
            with patch.object(
                run_bot.summarizer,
                "summarize_articles",
                new=AsyncMock(return_value="Short summary"),
            ):
                await run_bot.summary_command(update, context)
                assert mock_send.await_count == 1


async def test_ai_feature_commands():
    with patch.object(run_bot, "send_split_message", new=AsyncMock()) as mock_send:
        compare_context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        compare_context.args = ["GPT-4o", "vs", "Claude"]
        compare_update = make_update("/compare GPT-4o vs Claude")
        with patch.object(
            run_bot.report_generator,
            "generate_compare",
            new=AsyncMock(return_value="Compare output"),
        ):
            await run_bot.compare_command(compare_update, compare_context)

        roadmap_context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        roadmap_context.args = ["ai", "engineer"]
        roadmap_update = make_update("/roadmap ai engineer")
        with patch.object(
            run_bot.report_generator,
            "generate_roadmap",
            new=AsyncMock(return_value="Roadmap output"),
        ):
            await run_bot.roadmap_command(roadmap_update, roadmap_context)

        leaderboard_context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
        leaderboard_context.args = []
        leaderboard_update = make_update("/leaderboard")
        with patch.object(
            run_bot.report_generator,
            "generate_leaderboard",
            new=AsyncMock(return_value="Leaderboard output"),
        ):
            await run_bot.leaderboard_command(leaderboard_update, leaderboard_context)

        assert mock_send.await_count == 3


async def test_compare_usage_prompt():
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []
    update = make_update("/compare")
    await run_bot.compare_command(update, context)
    assert update.message.reply_text.await_count == 1


async def main():
    await test_basic_commands()
    await test_report_commands()
    await test_summary_command()
    await test_ai_feature_commands()
    await test_compare_usage_prompt()
    print("All slash command smoke tests passed.")


if __name__ == "__main__":
    asyncio.run(main())
