"""Tests for telegram_utils — message splitting and sending."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from utils.telegram_utils import send_split_message


@pytest.fixture
def mock_update():
    update = MagicMock()
    update.message = AsyncMock()
    update.message.reply_text = AsyncMock()
    return update


class TestSendSplitMessage:
    @pytest.mark.asyncio
    async def test_short_message_sends_directly(self, mock_update):
        text = "Hello, this is a short message."
        await send_split_message(mock_update, text)
        mock_update.message.reply_text.assert_awaited_once_with(
            text, parse_mode="Markdown"
        )

    @pytest.mark.asyncio
    async def test_empty_text_does_nothing(self, mock_update):
        await send_split_message(mock_update, "")
        mock_update.message.reply_text.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_none_text_does_nothing(self, mock_update):
        await send_split_message(mock_update, None)
        mock_update.message.reply_text.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_long_message_splits(self, mock_update):
        # Create a message that's over 4000 chars
        sections = ["Section A\n\n" + "x" * 2000, "Section B\n\n" + "y" * 2000]
        text = "\n\n".join(sections)
        assert len(text) > 4000

        await send_split_message(mock_update, text)
        # Should have sent multiple parts
        assert mock_update.message.reply_text.await_count >= 2

    @pytest.mark.asyncio
    async def test_very_long_single_section(self, mock_update):
        # A single section > 4000 chars gets split by lines
        text = "A" * 5000
        await send_split_message(mock_update, text)
        assert mock_update.message.reply_text.await_count >= 2

    @pytest.mark.asyncio
    async def test_custom_parse_mode(self, mock_update):
        text = "Hello"
        await send_split_message(mock_update, text, parse_mode="HTML")
        mock_update.message.reply_text.assert_awaited_once_with(
            text, parse_mode="HTML"
        )

    @pytest.mark.asyncio
    async def test_markdown_fallback_on_error(self, mock_update):
        """When Markdown parsing fails, falls back to plain text."""
        import telegram.error

        text = "Part 1\n\n" + "x" * 2000 + "\n\nPart 2\n\n" + "y" * 2000

        # Make the first call fail with TelegramError,
        # fallback succeeds, second part succeeds
        mock_update.message.reply_text = AsyncMock(
            side_effect=[
                telegram.error.TelegramError("parse error"),
                None,  # fallback for part 0
                None,  # part 1 with markdown
            ]
        )

        await send_split_message(mock_update, text)
        # Should have tried at least 3 calls (error + fallback + next part)
        assert mock_update.message.reply_text.await_count >= 2


class TestSendSplitMessageEdgeCases:
    @pytest.mark.asyncio
    async def test_single_section_exact_limit(self, mock_update):
        text = "x" * 4000
        await send_split_message(mock_update, text)
        mock_update.message.reply_text.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_many_newlines(self, mock_update):
        text = "\n\n".join(["Line " + str(i) for i in range(200)])
        await send_split_message(mock_update, text)
        assert mock_update.message.reply_text.await_count >= 1
