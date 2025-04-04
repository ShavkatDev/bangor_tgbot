from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def language_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang_ru"),
                InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang_uz"),
                InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang_en"),
            ]
        ]
    )