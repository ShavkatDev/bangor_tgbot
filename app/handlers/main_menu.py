import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.keyboards.reply_keyboard import main_menu_keyboard, inet_schedule_keyboard
from app.lexicon.lexicon import LEXICON_MSG
from app.utils.text_from_lexicon import TextFromLexicon

logger = logging.getLogger(__name__)
main_menu_router = Router()


@main_menu_router.message(Command("menu"))
async def show_main_menu(message: Message, lang: str, is_admin: bool):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) requested main menu")

    try:
        await message.answer(
            text=LEXICON_MSG["main_menu_title"][lang],
            reply_markup=main_menu_keyboard(lang, is_admin),
        )
    except Exception as e:
        logger.error(
            f"Error showing main menu for user {telegram_id}: {str(e)}", exc_info=True
        )
        await message.answer(text=LEXICON_MSG["error"][lang])


@main_menu_router.message(TextFromLexicon("inet_schedule"))
async def open_inet_schedule_menu(message: Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) opened inet schedule menu")

    try:
        await message.answer(
            text=LEXICON_MSG["choose_schedule"][lang],
            reply_markup=inet_schedule_keyboard(lang),
        )
    except Exception as e:
        logger.error(
            f"Error opening inet schedule menu for user {telegram_id}: {str(e)}",
            exc_info=True,
        )
        await message.answer(text=LEXICON_MSG["error"][lang])


@main_menu_router.message(TextFromLexicon("back_to_main"))
async def back_to_main_menu(message: Message, lang: str, is_admin: bool):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) returned to main menu")

    try:
        await message.answer(
            text=LEXICON_MSG["main_menu_title"][lang],
            reply_markup=main_menu_keyboard(lang, is_admin),
        )
    except Exception as e:
        logger.error(
            f"Error returning to main menu for user {telegram_id}: {str(e)}",
            exc_info=True,
        )
        await message.answer(text=LEXICON_MSG["error"][lang])
