import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import settings
from handlers import start_router, help_router
from middlewares import ThrottlingMiddleware
from database import init_db, get_connection

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

scheduler = AsyncIOScheduler()


async def send_reminders(bot: Bot):
    with get_connection() as conn:
        bookings = conn.execute("""
            SELECT b.user_id, b.day, b.time, b.id
            FROM bookings b
            WHERE b.reminded = 0
        """).fetchall()

    for b in bookings:
        try:
            await bot.send_message(
                b["user_id"],
                f"⏰ Напоминание!\nВы записаны: 📅 <b>{b['day']}</b> в <b>{b['time']}</b>\n\nЖдём вас! 🦷"
            )
            with get_connection() as conn:
                conn.execute("UPDATE bookings SET reminded = 1 WHERE id = ?", (b["id"],))
                conn.commit()
        except Exception:
            pass


async def on_startup(bot: Bot):
    init_db()
    scheduler.add_job(send_reminders, "interval", hours=1, args=[bot])
    scheduler.start()
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить"),
    ])

async def main():
    bot = Bot(
        token=settings.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.message.middleware(ThrottlingMiddleware(settings.RATE_LIMIT))
    dp.include_router(start_router)
    dp.include_router(help_router)
    dp.startup.register(on_startup)
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())