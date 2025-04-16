import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.routers import setup_routers
from app.middleware.registration_check import RegistrationCheckMiddleware
from app.middleware.ignore_groups import IgnoreGroupChatsMiddleware


async def main():
    bot = Bot(settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    await bot(DeleteWebhook(drop_pending_updates=True))
    
    setup_routers(dp)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
