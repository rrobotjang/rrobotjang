"""APScheduler job: Amadeus API -> PostgreSQL upsert."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler


async def sync_amadeus_offers():
    # TODO: call Amadeus SDK, normalize payload and upsert flight_offers.
    return


def start_scheduler():
    scheduler = AsyncIOScheduler()
    scheduler.add_job(sync_amadeus_offers, "cron", minute="*/30")
    scheduler.start()
