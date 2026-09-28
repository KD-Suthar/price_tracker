from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
from price_tracker.config import settings


def run_forever(job_fn, symbols: list[str]) -> None:
    scheduler = BlockingScheduler()
    scheduler.add_job(
        job_fn,
        "interval",
        seconds=settings.poll_interval_seconds,
        args=[symbols],
        next_run_time=datetime.now(),  # fire once right away, then on the interval
    )
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("Stopped.")