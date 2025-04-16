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
from app.middleware.language import LanguageMiddleware
from app.utils.lesson_check import start_lesson_check_task


async def main():
    bot = Bot(settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    await bot(DeleteWebhook(drop_pending_updates=True))
    asyncio.create_task(start_lesson_check_task(bot))
    
    setup_routers(dp)

    dp.message.middleware(IgnoreGroupChatsMiddleware())
    dp.message.middleware(RegistrationCheckMiddleware())
    dp.message.middleware(LanguageMiddleware())

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
