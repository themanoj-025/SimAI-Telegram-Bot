import asyncio

from unittest.mock import AsyncMock, MagicMock

import pytest

from utils.telegram_utils import _msg, MAX_MESSAGE_LENGTH, send_split_message


@pytest.fixture
def mock_loop(monkeypatch):
    """Swap in a controllable event loop whose `time()` we can freeze."""
    loop = asyncio.new_event_loop()
    monkeypatch.setattr(asyncio, "get_event_loop", lambda: loop)
    monkeypatch.setattr(asyncio, "get_event_loop_policy", lambda: None)
    return loop


@pytest.fixture
def mock_update() -> MagicMock:
    """Build a mocked Update whose message supports async reply."""
    update = MagicMock()
    update.message = AsyncMock()
    update.message.reply_text = AsyncMock()
    return update


class TestMessageLengthGuard:
    def test_exact_limit_uses_direct_path(self, mock_update):
        mock_update.message.reply_text = AsyncMock()
        text = "x" * MAX_MESSAGE_LENGTH
        asyncio.run(send_split_message(mock_update, text))
        mock_update.message.reply_text.assert_awaited_once()

    def test_over_limit_truncates_and_logs_warning(self, mock_update, caplog):
        mock_loop.time = lambda: 100.0
        with caplog.at_level("WARNING"):
            text = "x" * (MAX_MESSAGE_LENGTH + 100)
            asyncio.run(send_split_message(mock_update, text))
        assert any("silently truncated" in r.message for r in caplog.records)
        assert len(mock_update.message.reply_text.call_args[0][0]) <= MAX_MESSAGE_LENGTH

    def test_under_limit_no_warning(self, mock_update, caplog):
        mock_loop.time = lambda: 100.0
        with caplog.at_level("WARNING"):
            text = "x" * (MAX_MESSAGE_LENGTH - 100)
            asyncio.run(send_split_message(mock_update, text))
        assert not any("silently truncated" in r.message for r in caplog.records)

    def test_empty_does_nothing(self, mock_update):
        mock_loop.time = lambda: 100.0
        asyncio.run(send_split_message(mock_update, ""))
        asyncio.run(send_split_message(mock_update, None))
        mock_update.message.reply_text.assert_not_awaited()
