from aiogram import Router, types
from aiogram import F
from app.keyboards.reply import main_menu_keyboard, settings_keyboard, mailing_keyboard
from app.keyboards.language_keyboard import language_keyboard
from app.lexicon.lexicon import LEXICON_MSG
from app.utils.text_from_lexicon import TextFromLexicon
from app.db.crud.user import get_user_language, update_user_language

settings_router = Router()

@settings_router.message(TextFromLexicon("settings"))
async def open_settings(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["settings_menu"][lang],
        reply_markup=settings_keyboard(lang)
    )

@settings_router.message(TextFromLexicon("mailing_settings"))
async def mailing_settings(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["choose_mailing"][lang],
        reply_markup=mailing_keyboard(lang)
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

@settings_router.callback_query(F.data.startswith("set_lang_"))
async def process_language_change(callback: types.CallbackQuery):
    lang_code = callback.data.split("_")[-1]
    await update_user_language(callback.from_user.id, lang_code)

    await callback.answer(
        text=LEXICON_MSG["language_changed_messages"][lang_code]
    )

    await callback.message.answer(
    text=LEXICON_MSG["main_menu_title"][lang_code],
    reply_markup=main_menu_keyboard(lang_code)
)