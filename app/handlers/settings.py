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

settings_router = Router()

@settings_router.message(TextFromLexicon("settings"))
async def open_settings(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["settings_menu"][lang],
        reply_markup=settings_keyboard(lang)
    )

@settings_router.callback_query(F.data == "back_to_settings_menu")
async def open_settings(callback: types.CallbackQuery):
    lang = await get_user_language(callback.from_user.id)

    await callback.message.delete()

    await callback.message.answer(
        text=LEXICON_MSG["settings_menu"][lang],
        reply_markup=settings_keyboard(lang)
    )


@settings_router.message(TextFromLexicon("language_settings"))
async def language_settings(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["choose_language"][lang],
        reply_markup=language_keyboard()
    )

@settings_router.message(TextFromLexicon("back_to_main"))
async def back_to_main_menu(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["main_menu_title"][lang],
        reply_markup=main_menu_keyboard(lang)
    )

@settings_router.message(TextFromLexicon("language_settings"))
async def language_settings(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["choose_language"][lang],
        reply_markup=language_keyboard()
    )

@settings_router.message(TextFromLexicon("delete_user"))
async def delete_userdata(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["confirm_data_deletion"][lang],
        reply_markup=delete_keyboard(lang)
    )

@settings_router.callback_query(F.data.startswith("delete_"))
async def confirm_delete(callback: types.CallbackQuery):
    lang = await get_user_language(callback.from_user.id)
    await callback.answer()
    await callback.message.delete()
    if callback.data == 'delete_approve':
        await delete_user_completely(callback.from_user.id)
        await callback.message.answer(
            text=LEXICON_MSG["data_deleted"][lang],
            reply_markup=ReplyKeyboardRemove()
        )
    elif callback.data == 'delete_decline':
        await callback.message.answer(
            text=LEXICON_MSG["process_cancelled"][lang],
            reply_markup=main_menu_keyboard(lang)
        )

@settings_router.callback_query(F.data.startswith("set_lang_"))
async def process_language_change(callback: types.CallbackQuery):
    lang_code = callback.data.split("_")[-1]
    await update_user_language(callback.from_user.id, lang_code)

    await callback.answer(
        text=LEXICON_MSG["language_changed_messages"][lang_code]
    )

    await callback.message.delete()

    await callback.message.answer(
        text=LEXICON_MSG["main_menu_title"][lang_code],
        reply_markup=main_menu_keyboard(lang_code)
    )
    
@settings_router.message(TextFromLexicon("mailing_settings"))
async def mailing_settings(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    settings = await get_user_settings(message.from_user.id)

    await message.answer(
        text=LEXICON_MSG["choose_mailing"][lang],
        reply_markup=mailing_settings_keyboard(
            daily_digest=settings.daily_digest,
            today_schedule_digest=settings.today_schedule_digest,
            lang=lang
        )
    )
@settings_router.callback_query(F.data == "toggle_daily_digest")
async def toggle_daily_digest_handler(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    lang = await get_user_language(telegram_id)

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

@settings_router.callback_query(F.data == "toggle_today_schedule_digest")
async def toggle_today_schedule_digest_handler(callback: types.CallbackQuery):
    telegram_id = callback.from_user.id
    lang = await get_user_language(telegram_id)

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