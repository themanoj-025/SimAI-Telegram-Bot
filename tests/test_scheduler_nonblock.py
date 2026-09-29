from unittest.mock import MagicMock, patch

import pytest

from services.scheduler import SchedulerService


class TestSchedulerNonBlock:
    """Verify refresh work is offloaded off the bot loop (to_thread)."""

    @patch("asyncio.to_thread")
    @patch("asyncio.get_running_loop", side_effect=RuntimeError("no loop"))
    def test_run_refresh_now_runs_work_in_thread(self, mock_get_loop, mock_to_thread):
        """run_refresh_now() must hand the long work to asyncio.to_thread."""
        mock_to_thread.side_effect = RuntimeError("blocking work")
        refresh_cb = MagicMock()
        svc = SchedulerService(refresh_cb)
        svc.run_refresh_now()
        mock_to_thread.assert_called_once()

    @patch("asyncio.to_thread")
    @patch("asyncio.get_running_loop", side_effect=RuntimeError("no loop"))
    def test_run_refresh_now_offloads_without_blocking_loop(self, mock_get_loop, mock_to_thread):
        """to_thread must be used so the bot's event loop stays responsive."""
        mock_to_thread.side_effect = RuntimeError("blocking work")
        refresh_cb = MagicMock()
        svc = SchedulerService(refresh_cb)
        svc.run_refresh_now()
        mock_to_thread.assert_called_once()

    @patch("asyncio.to_thread")
    def test_run_refresh_now_no_running_loop_falls_back(self, mock_to_thread):
        """When no event loop is running, asyncio.run() is used instead."""
        mock_get_loop = MagicMock(side_effect=RuntimeError("no loop"))
        with patch("asyncio.get_running_loop", mock_get_loop), patch(
            "asyncio.run"
        ) as mock_run:
            refresh_cb = MagicMock()
            svc = SchedulerService(refresh_cb)
            svc.run_refresh_now()
            mock_get_loop.assert_called_once()
            mock_run.assert_called_once()
