import pytest

pytestmark = pytest.mark.unit

"""Tests for SchedulerService — APScheduler wrapper."""

from unittest.mock import MagicMock, patch

from services.scheduler import SchedulerService


class TestSchedulerService:
    def setup_method(self) -> None:
        self.refresh_cb = MagicMock()
        self.daily_cb = MagicMock()

    def test_init(self) -> None:
        svc = SchedulerService(self.refresh_cb)
        assert svc.refresh_callback is self.refresh_cb
        assert svc.daily_report_callback is None

    def test_init_with_daily_callback(self) -> None:
        svc = SchedulerService(self.refresh_cb, daily_report_callback=self.daily_cb)
        assert svc.daily_report_callback is self.daily_cb

    @patch("services.scheduler.BackgroundScheduler")
    def test_start_adds_refresh_job(self, mock_sched_cls) -> None:
        mock_sched = MagicMock()
        mock_sched_cls.return_value = mock_sched

        svc = SchedulerService(self.refresh_cb)
        svc.start()

        # Should have added at least one job (the refresh job)
        assert mock_sched.add_job.call_count >= 1
        mock_sched.start.assert_called_once()

    @patch("services.scheduler.BackgroundScheduler")
    def test_start_with_daily_callback_adds_two_jobs(self, mock_sched_cls) -> None:
        mock_sched = MagicMock()
        mock_sched_cls.return_value = mock_sched

        svc = SchedulerService(self.refresh_cb, daily_report_callback=self.daily_cb)
        svc.start()

        assert mock_sched.add_job.call_count == 2
        mock_sched.start.assert_called_once()

    @patch("services.scheduler.BackgroundScheduler")
    def test_stop_shuts_down(self, mock_sched_cls) -> None:
        mock_sched = MagicMock()
        mock_sched_cls.return_value = mock_sched

        svc = SchedulerService(self.refresh_cb)
        svc.start()
        svc.stop()

        mock_sched.shutdown.assert_called_once()

    @patch("services.scheduler.BackgroundScheduler")
    def test_run_refresh_now_calls_callback(self, mock_sched_cls) -> None:
        svc = SchedulerService(self.refresh_cb)
        svc.run_refresh_now()
        self.refresh_cb.assert_called_once()

    @patch("services.scheduler.BackgroundScheduler")
    def test_refresh_job_has_correct_id(self, mock_sched_cls) -> None:
        """Verify the refresh job uses the expected job ID."""
        mock_sched = MagicMock()
        mock_sched_cls.return_value = mock_sched

        svc = SchedulerService(self.refresh_cb)
        svc.start()

        # Check the first call has the refresh_job id
        call_args = mock_sched.add_job.call_args_list[0]
        assert call_args[1].get("id") == "refresh_job"
