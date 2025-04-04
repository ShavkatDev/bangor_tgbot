from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.lexicon.lexicon import LEXICON_BUTTONS


def get_button(key: str, lang: str = "en") -> str:
    return LEXICON_BUTTONS.get(key, {}).get(lang, f"[{key}]")


def main_menu_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button("inet_schedule", lang))],
            [KeyboardButton(text=get_button("settings", lang)), KeyboardButton(text=get_button("support", lang))]
        ],
        resize_keyboard=True
    )


def inet_schedule_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button("schedule_tomorrow_view", lang)), KeyboardButton(text=get_button("schedule_week_view", lang))],
            [KeyboardButton(text=get_button("attendance", lang))],
            [KeyboardButton(text=get_button("back_to_main", lang))]
        ],
        resize_keyboard=True
    )


def settings_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button("mailing_settings", lang))],
            [KeyboardButton(text=get_button("language_settings", lang))],
            [KeyboardButton(text=get_button("back_to_main", lang))]
        ],
        resize_keyboard=True
)


def mailing_keyboard(lang: str, notifications_enabled: bool) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(
                text=get_button(
                    "disable_notifications" if notifications_enabled else "enable_notifications", lang
                )
            )],
            [KeyboardButton(text=get_button("back_to_settings", lang))]
        ],
        resize_keyboard=True
    )
