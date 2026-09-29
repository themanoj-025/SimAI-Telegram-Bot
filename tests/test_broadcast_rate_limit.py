import asyncio

import pytest

from utils.telegram_utils import _rate_limited


@pytest.fixture
def mock_loop(monkeypatch):
    """Swap in a controllable event loop whose `time()` we can freeze."""
    loop = asyncio.new_event_loop()
    monkeypatch.setattr(asyncio, "get_event_loop", lambda: loop)
    monkeypatch.setattr(asyncio, "get_event_loop_policy", lambda: None)
    return loop


class TestBroadcastRateLimit:
    """Verify the per-chat cooldown prevents burst sends."""

    def test_first_send_allowed(self, mock_loop):
        chat_id = "12345"
        mock_loop.time = lambda: 100.0
        assert _rate_limited(chat_id) is False

    def test_second_send_within_window_blocked(self, mock_loop):
        chat_id = "12345"
        mock_loop.time = lambda: 100.0
        # Prime the cooldown
        _rate_limited(chat_id)
        # Backdate so we are inside the 3s window
        mock_loop.time = lambda: 101.0
        assert _rate_limited(chat_id) is True

    def test_send_after_window_allowed(self, mock_loop):
        chat_id = "67890"
        mock_loop.time = lambda: 200.0
        _rate_limited(chat_id)
        mock_loop.time = lambda: 204.0  # > 3s window
        assert _rate_limited(chat_id) is False
