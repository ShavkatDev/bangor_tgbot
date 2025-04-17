import logging
from aiogram import Router, types
from aiogram import F
from aiogram.types import ReplyKeyboardRemove
from app.keyboards.reply import main_menu_keyboard, settings_keyboard
from app.keyboards.language_keyboard import language_keyboard
from app.keyboards.mailing_keyboard import mailing_settings_keyboard
from app.keyboards.delete_keyboard import delete_keyboard
from app.lexicon.lexicon import LEXICON_MSG
from app.utils.text_from_lexicon import TextFromLexicon
from app.db.crud.user import delete_user_completely, get_user_language, update_user_language
from app.db.crud.user_settings import get_user_settings, toggle_daily_digest, toggle_today_schedule_digest

logger = logging.getLogger(__name__)
settings_router = Router()

@settings_router.message(TextFromLexicon("settings"))
async def open_settings(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) opened settings menu")
    
    try:
        await message.answer(
            text=LEXICON_MSG["settings_menu"][lang],
            reply_markup=settings_keyboard(lang)
        )
    except Exception as e:
        logger.error(f"Error opening settings menu for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])

@settings_router.callback_query(F.data == "back_to_settings_menu")
async def open_settings(callback: types.CallbackQuery, lang: str):
    telegram_id = callback.from_user.id
    username = callback.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) returned to settings menu")
    
    try:
        lang = await get_user_language(telegram_id)
        await callback.message.delete()
        await callback.message.answer(
            text=LEXICON_MSG["settings_menu"][lang],
            reply_markup=settings_keyboard(lang)
        )
    except Exception as e:
        logger.error(f"Error returning to settings menu for user {telegram_id}: {str(e)}", exc_info=True)
        await callback.message.answer(text=LEXICON_MSG['error'][lang])

@settings_router.message(TextFromLexicon("language_settings"))
async def language_settings(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) opened language settings")
    
    try:
        await message.answer(
            text=LEXICON_MSG["choose_language"][lang],
            reply_markup=language_keyboard()
        )
    except Exception as e:
        logger.error(f"Error opening language settings for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])

@settings_router.message(TextFromLexicon("back_to_main"))
async def back_to_main_menu(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) returned to main menu from settings")
    
    try:
        await message.answer(
            text=LEXICON_MSG["main_menu_title"][lang],
            reply_markup=main_menu_keyboard(lang)
        )
    except Exception as e:
        logger.error(f"Error returning to main menu for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])

@settings_router.message(TextFromLexicon("delete_user"))
async def delete_userdata(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) requested account deletion")
    
    try:
        await message.answer(
            text=LEXICON_MSG["confirm_data_deletion"][lang],
            reply_markup=delete_keyboard(lang)
        )
    except Exception as e:
        logger.error(f"Error showing delete confirmation for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])

@settings_router.callback_query(F.data.startswith("delete_"))
async def confirm_delete(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    username = callback.from_user.username or "No username"
    action = callback.data
    
    try:
        lang = await get_user_language(telegram_id)
        await callback.answer()
        await callback.message.delete()
        
        if action == 'delete_approve':
            logger.info(f"User {telegram_id} (@{username}) confirmed account deletion")
            await delete_user_completely(telegram_id)
            await callback.message.answer(
                text=LEXICON_MSG["data_deleted"][lang],
                reply_markup=ReplyKeyboardRemove()
            )
        elif action == 'delete_decline':
            logger.info(f"User {telegram_id} (@{username}) cancelled account deletion")
            await callback.message.answer(
                text=LEXICON_MSG["process_cancelled"][lang],
                reply_markup=main_menu_keyboard(lang)
            )
    except Exception as e:
        logger.error(f"Error processing delete action for user {telegram_id}: {str(e)}", exc_info=True)
        await callback.message.answer(text=LEXICON_MSG['error'][lang])

@settings_router.callback_query(F.data.startswith("set_lang_"))
async def process_language_change(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    username = callback.from_user.username or "No username"
    lang_code = callback.data.split("_")[-1]
    
    try:
        logger.info(f"User {telegram_id} (@{username}) changed language to {lang_code}")
        await update_user_language(telegram_id, lang_code)
        await callback.answer(text=LEXICON_MSG["language_changed_messages"][lang_code])
        await callback.message.delete()
        await callback.message.answer(
            text=LEXICON_MSG["main_menu_title"][lang_code],
            reply_markup=main_menu_keyboard(lang_code)
        )
    except Exception as e:
        logger.error(f"Error changing language for user {telegram_id}: {str(e)}", exc_info=True)
        await callback.message.answer(text=LEXICON_MSG['error'][lang_code])
    
@settings_router.message(TextFromLexicon("mailing_settings"))
async def mailing_settings(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) opened mailing settings")
    
    try:
        settings = await get_user_settings(telegram_id)
        await message.answer(
            text=LEXICON_MSG["choose_mailing"][lang],
            reply_markup=mailing_settings_keyboard(
                daily_digest=settings.daily_digest,
                today_schedule_digest=settings.today_schedule_digest,
                lang=lang
            )
        )
    except Exception as e:
        logger.error(f"Error opening mailing settings for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])

@settings_router.callback_query(F.data == "toggle_daily_digest")
async def toggle_daily_digest_handler(callback: types.CallbackQuery, lang: str):
    telegram_id = callback.from_user.id
    username = callback.from_user.username or "No username"
    
    try:
        logger.info(f"User {telegram_id} (@{username}) toggled daily digest")
        await toggle_daily_digest(telegram_id)
        settings = await get_user_settings(telegram_id)

        await callback.message.edit_reply_markup(
            reply_markup=mailing_settings_keyboard(
                daily_digest=settings.daily_digest,
                today_schedule_digest=settings.today_schedule_digest,
                lang=lang
            )
        )
        await callback.answer(LEXICON_MSG["settings_updated"][lang])
    except Exception as e:
        logger.error(f"Error toggling daily digest for user {telegram_id}: {str(e)}", exc_info=True)
        await callback.message.answer(text=LEXICON_MSG['error'][lang])

@settings_router.callback_query(F.data == "toggle_today_schedule_digest")
async def toggle_today_schedule_digest_handler(callback: types.CallbackQuery, lang: str):
    telegram_id = callback.from_user.id
    username = callback.from_user.username or "No username"
    
    try:
        logger.info(f"User {telegram_id} (@{username}) toggled today schedule digest")
        await toggle_today_schedule_digest(telegram_id)
        settings = await get_user_settings(telegram_id)

        await callback.message.edit_reply_markup(
            reply_markup=mailing_settings_keyboard(
                daily_digest=settings.daily_digest,
                today_schedule_digest=settings.today_schedule_digest,
                lang=lang
            )
        )
        await callback.answer(LEXICON_MSG["settings_updated"][lang])
    except Exception as e:
        logger.error(f"Error toggling today schedule digest for user {telegram_id}: {str(e)}", exc_info=True)
        await callback.message.answer(text=LEXICON_MSG['error'][lang])