from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger

from config.config import Config
from utils.logger import setup_logger

logger = setup_logger(__name__)


class SchedulerService:
    def __init__(self, refresh_callback, daily_report_callback=None) -> None:
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
        logger.info("Manual refresh triggered!")
        self.refresh_callback()
