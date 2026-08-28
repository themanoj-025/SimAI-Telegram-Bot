"""Tests for scheduler service."""

from unittest.mock import MagicMock, patch

from services.scheduler import SchedulerService


class TestSchedulerService:
    """Tests for SchedulerService."""

    def test_init(self):
        callback = MagicMock()
        scheduler = SchedulerService(callback)
        assert scheduler.refresh_callback == callback
        assert scheduler.daily_report_callback is None

    def test_init_with_daily_report(self):
        callback = MagicMock()
        daily = MagicMock()
        scheduler = SchedulerService(callback, daily_report_callback=daily)
        assert scheduler.daily_report_callback == daily

    @patch("services.scheduler.BackgroundScheduler")
    def test_start(self, mock_sched_cls):
        callback = MagicMock()
        scheduler = SchedulerService(callback)
        scheduler.start()
        mock_sched_cls.return_value.add_job.assert_called_once()
        mock_sched_cls.return_value.start.assert_called_once()

    @patch("services.scheduler.BackgroundScheduler")
    def test_stop(self, mock_sched_cls):
        callback = MagicMock()
        scheduler = SchedulerService(callback)
        scheduler.start()
        scheduler.stop()
        mock_sched_cls.return_value.shutdown.assert_called_once()

    @patch("services.scheduler.BackgroundScheduler")
    def test_run_refresh_now(self, mock_sched_cls):
        callback = MagicMock()
        scheduler = SchedulerService(callback)
        scheduler.run_refresh_now()
        callback.assert_called_once()
