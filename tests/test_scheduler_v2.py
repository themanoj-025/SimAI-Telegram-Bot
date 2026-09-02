from unittest.mock import MagicMock, patch

import pytest

from services.scheduler import SchedulerService

pytestmark = pytest.mark.unit

"""Tests for scheduler service."""




class TestSchedulerService:
    """Tests for SchedulerService."""

    def test_init(self) -> None:
        callback = MagicMock()
        scheduler = SchedulerService(callback)
        assert scheduler.refresh_callback == callback
        assert scheduler.daily_report_callback is None

    def test_init_with_daily_report(self) -> None:
        callback = MagicMock()
        daily = MagicMock()
        scheduler = SchedulerService(callback, daily_report_callback=daily)
        assert scheduler.daily_report_callback == daily

    @patch("services.scheduler.BackgroundScheduler")
    def test_start(self, mock_sched_cls) -> None:
        callback = MagicMock()
        scheduler = SchedulerService(callback)
        scheduler.start()
        mock_sched_cls.return_value.add_job.assert_called_once()
        mock_sched_cls.return_value.start.assert_called_once()

    @patch("services.scheduler.BackgroundScheduler")
    def test_stop(self, mock_sched_cls) -> None:
        callback = MagicMock()
        scheduler = SchedulerService(callback)
        scheduler.start()
        scheduler.stop()
        mock_sched_cls.return_value.shutdown.assert_called_once()

    @patch("services.scheduler.BackgroundScheduler")
    def test_run_refresh_now(self, mock_sched_cls) -> None:
        callback = MagicMock()
        scheduler = SchedulerService(callback)
        scheduler.run_refresh_now()
        callback.assert_called_once()
