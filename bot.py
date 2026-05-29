import asyncio
import logging
from zoneinfo import ZoneInfo

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from envsetup import Credentials
from handlers import user_handlers
from support.scheduler import take_daily_snapshots

logging.basicConfig(level=logging.INFO)

KYIV_TZ = ZoneInfo("Europe/Kyiv")


async def main():
    bot = Bot(token=Credentials.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(user_handlers.router)

    scheduler = AsyncIOScheduler(timezone=KYIV_TZ)
    scheduler.add_job(take_daily_snapshots, CronTrigger(hour=0, minute=0, timezone=KYIV_TZ))
    scheduler.start()

    # Робимо снепшот при старті для тих, у кого ще немає сьогоднішнього
    await take_daily_snapshots()

    await bot.delete_webhook(drop_pending_updates=False)
    await dp.start_polling(bot, allowed_updates=[])


if __name__ == '__main__':
    asyncio.run(main())
