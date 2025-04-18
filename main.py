import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram.client.default import DefaultBotProperties

from app.config import settings
from app.logging_config import setup_logging
from app.middleware.admin_check import AdminMiddleware
from app.routers import setup_routers
from app.middleware.registration_check import RegistrationCheckMiddleware
from app.middleware.ignore_groups import IgnoreGroupChatsMiddleware
from app.middleware.language import LanguageMiddleware
from app.utils.lesson_check import setup_lesson_check_scheduler
from app.utils.schedule_check import setup_digest_scheduler

logger = logging.getLogger(__name__)

async def main():
    logger.info("Starting bot initialization...")
    
    bot = Bot(settings.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    
    try:
        logger.info("Deleting webhook and setting up bot...")
        await bot(DeleteWebhook(drop_pending_updates=True))
        
        logger.info("Setting up schedulers...")
        setup_lesson_check_scheduler(bot)
        setup_digest_scheduler(bot)
        
        logger.info("Setting up routers and middleware...")
        setup_routers(dp)
        dp.message.middleware(IgnoreGroupChatsMiddleware())
        dp.message.middleware(RegistrationCheckMiddleware())
        dp.message.middleware(AdminMiddleware())
        dp.callback_query.middleware(AdminMiddleware())
        dp.message.middleware(LanguageMiddleware())
        dp.callback_query.middleware(LanguageMiddleware())
        
        logger.info("Bot is ready to start polling...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Error during bot operation: {str(e)}", exc_info=True)
        raise
    finally:
        logger.info("Shutting down bot...")
        await bot.session.close()

if __name__ == "__main__":
    setup_logging()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
