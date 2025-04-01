import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config import TOKEN
from app.routers import setup_routers
from app.scheduler import schedule_loop
from app.middleware.admin_filter import AdminFilterMiddleware

async def main():
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    setup_routers(dp)
    asyncio.create_task(schedule_loop())

    dp.message.middleware(AdminFilterMiddleware())
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
