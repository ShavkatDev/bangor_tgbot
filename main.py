import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.routers import setup_routers
from app.middleware.admin_filter import AdminFilterMiddleware
from app.middleware.registration_check import RegistrationCheckMiddleware
from app.middleware.ignore_groups import IgnoreGroupChatsMiddleware


async def main():
    bot = Bot(settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    setup_routers(dp)

    dp.message.middleware(AdminFilterMiddleware())
    dp.message.middleware(RegistrationCheckMiddleware())
    dp.message.middleware(IgnoreGroupChatsMiddleware())
    
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
