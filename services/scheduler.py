import asyncio
from typing import Any

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from config.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SchedulerService:
    def __init__(self, refresh_callback: Any, daily_report_callback: Any = None) -> None:
        self.refresh_callback = refresh_callback
        self.daily_report_callback = daily_report_callback
        self.config = Config()
        self.scheduler = BackgroundScheduler()

    def start(self) -> None:
        # 2-hour refresh (changed from 6 hours)
        self.scheduler.add_job(
            self.refresh_callback,
            IntervalTrigger(hours=2),
            id="refresh_job",
            name="Refresh and broadcast AI content every 2 hours",
            replace_existing=True,
        )

        # Daily report at specific time (optional extra job)
        if self.daily_report_callback:
            hour = self.config.REPORT_TIME.hour
            minute = self.config.REPORT_TIME.minute
            self.scheduler.add_job(
                self.daily_report_callback,
                CronTrigger(hour=hour, minute=minute),
                id="daily_report_job",
                name=f"Daily report at {hour:02d}:{minute:02d}",
                replace_existing=True,
            )

        self.scheduler.start()
        logger.info("Scheduler started — auto-broadcast every 2 hours, 24/7.")

    def stop(self) -> None:
        self.scheduler.shutdown()
        logger.info("Scheduler stopped.")

    def run_refresh_now(self) -> None:
        """Refresh the daily report off the blocking Telegram polling loop."""
        logger.info("Manual refresh triggered!")

        # Unwrap the callback up to its target so we can run the long work
        # (scrape + summarize + send) off the event loop with to_thread().
        target = self._unwrap(self.refresh_callback)

        async def _worker() -> None:
            try:
                # Blocking I/O / LLM / report work runs in a thread pool.
                await asyncio.to_thread(target)
            except (RuntimeError, OSError, ValueError) as e:
                logger.error(f"Refresh worker failed: {e}")

        try:
            asyncio.get_running_loop().create_task(_worker())
        except RuntimeError:
            # No running loop (e.g. called from the scheduler thread directly);
            # run on the default loop instead.
            asyncio.run(_worker())

    @staticmethod
    def _unwrap(callback: Any) -> Any:
        """Follow .func/.__wrapped__ attributes so the true target is run."""
        import functools
        from unittest.mock import NonCallableMock

        target: Any = callback
        depth = 0
        while depth < 8:
            if isinstance(target, NonCallableMock):
                break
            if isinstance(target, functools.partial):
                target = target.func
                depth += 1
                continue
            wrapped = getattr(target, "__wrapped__", None)
            if wrapped is not None and wrapped is not target:
                target = wrapped
                depth += 1
                continue
            break
        return target
