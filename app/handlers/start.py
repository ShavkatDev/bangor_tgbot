import logging
from aiogram import Router, types
from aiogram.filters import CommandStart
from app.db.crud.user import get_user_by_telegram_id

from app.keyboards.login_keyboard import inline_login
from app.keyboards.reply_keyboard import main_menu_keyboard
from app.lexicon.lexicon import LEXICON_MSG

logger = logging.getLogger(__name__)
start_router = Router()


@start_router.message(CommandStart())
async def start_command(message: types.Message, lang: str, is_admin: bool):
    await message.answer(text=LEXICON_MSG["bot_intro"][lang])

    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(
        f"User {telegram_id} (@{username}) started the bot with language {lang}"
    )

    try:
        user = await get_user_by_telegram_id(telegram_id)

        if user:
            logger.info(
                f"User {telegram_id} (@{username}) is registered, showing main menu"
            )
            await message.answer(
                text=LEXICON_MSG["greet"][lang],
                reply_markup=main_menu_keyboard(lang, is_admin),
            )
        else:
            logger.info(
                f"User {telegram_id} (@{username}) is not registered, showing login prompt"
            )
            await message.answer(
                text=LEXICON_MSG["greet_login"][lang], reply_markup=inline_login
            )
    except Exception as e:
        logger.error(
            f"Error in start command for user {telegram_id}: {str(e)}", exc_info=True
        )
        await message.answer(text=LEXICON_MSG["error"][lang])
