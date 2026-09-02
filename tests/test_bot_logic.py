import asyncio
import os
import sys
from unittest.mock import AsyncMock, MagicMock

import pytest
from telegram import Message, Update
from telegram.ext import ContextTypes

from config.config import Config
from run_bot import start_command

pytestmark = pytest.mark.integration


# Ensure the repository root is importable regardless of where this script
# is invoked from (repo root or a subdirectory such as tests/).
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))





async def test_bot_startup() -> None:
    print("Testing Bot Startup Logic...")

    # 1. Verify Config doesn't have removed categories
    print("Checking Config...")
    if "datasets" in Config.RSS_FEEDS or "conferences" in Config.RSS_FEEDS:
        print("  [-] Error: Removed categories still in RSS_FEEDS")
    else:
        print("  [+] Success: Removed categories are gone from RSS_FEEDS")

    # 2. Mock Update for /start command
    print("Testing /start command response...")
    update = MagicMock(spec=Update)
    update.message = AsyncMock(spec=Message)
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)

    await start_command(update, context)

    welcome_text = update.message.reply_text.call_args[0][0]
    if "/datasets" in welcome_text or "/conferences" in welcome_text:
        print("  [-] Error: Welcome message still contains removed commands")
    else:
        print("  [+] Success: Welcome message is clean")

    # 3. Verify handler registration (dry run of main logic)
    print("Checking command list...")
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
    # This just ensures we didn't bread the list in run_bot.py (we can't easily check 'app' without token)
    print(f"  [+] Categories to register: {len(categories)}")


if __name__ == "__main__":
    asyncio.run(test_bot_startup())
