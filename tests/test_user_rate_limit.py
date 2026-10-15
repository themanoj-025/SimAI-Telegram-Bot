import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from telegram import Message, Update
from telegram.ext import ContextTypes

import run_bot


def make_update(message_text: str = "/summary", chat_id: int = 99999) -> Update:
    update = MagicMock(spec=Update)
    update.message = AsyncMock(spec=Message)
    update.message.text = message_text
    update.effective_chat = MagicMock()
    update.effective_chat.id = chat_id
    return update


@pytest.mark.asyncio
async def test_user_rate_limiting_throttles_burst() -> None:
    """Regression test for SEC-002: throttles rapid consecutive interactive commands."""
    update = make_update("/summary", chat_id=11111)
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []

    # Enable throttling for this test
    run_bot.USER_COMMAND_COOLDOWN_SECONDS = 5.0
    run_bot._LAST_USER_COMMAND.clear()

    try:
        with patch.object(run_bot, "_queue_command", return_value=True):
            # First command succeeds
            await run_bot.summary_command(update, context)
            assert update.message.reply_text.call_args_list[-1][0][0] == "Generating AI summary..."

            # Immediate second command is throttled
            await run_bot.summary_command(update, context)
            assert (
                update.message.reply_text.call_args_list[-1][0][0]
                == "Please wait a moment before sending another command."
            )
    finally:
        run_bot.USER_COMMAND_COOLDOWN_SECONDS = 0.0
        run_bot._LAST_USER_COMMAND.clear()


@pytest.mark.asyncio
async def test_queue_overflow_rejected() -> None:
    """Regression test for SEC-002: rejects tasks when queue reaches MAX_QUEUE_SIZE."""
    update = make_update("/news", chat_id=22222)
    context = MagicMock(spec=ContextTypes.DEFAULT_TYPE)
    context.args = []

    # Reset state
    run_bot.USER_COMMAND_COOLDOWN_SECONDS = 0.0
    with run_bot._QUEUE_LOCK:
        orig_queue = list(run_bot._QUEUE)
        # Fill queue to capacity
        run_bot._QUEUE = [{"fake": i} for i in range(run_bot.MAX_QUEUE_SIZE)]

    try:
        await run_bot.generic_command(update, context, "news")
        assert (
            update.message.reply_text.call_args_list[-1][0][0]
            == "Server is currently busy. Please try again shortly."
        )
    finally:
        with run_bot._QUEUE_LOCK:
            run_bot._QUEUE = orig_queue
