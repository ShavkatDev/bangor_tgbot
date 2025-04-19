from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from app.lexicon.lexicon import LEXICON_BUTTONS

def get_button(key: str, lang: str = "en") -> str:
    return LEXICON_BUTTONS.get(key, {}).get(lang, f"[{key}]")

def main_menu_keyboard(lang: str, is_admin: bool = False) -> ReplyKeyboardMarkup:
    buttons = [
        [KeyboardButton(text=get_button("inet_schedule", lang))],
        [KeyboardButton(text=get_button("settings", lang)), KeyboardButton(text=get_button("support", lang))]
    ]
    if is_admin:
        buttons.append([KeyboardButton(text="👨🏻‍💻 Админ-панель")])

    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


def inet_schedule_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button("schedule_today_view", lang)), KeyboardButton(text=get_button("schedule_tomorrow_view", lang))],
            [KeyboardButton(text=get_button("schedule_week_view", lang))],
            [KeyboardButton(text=get_button("attendance", lang))],
            [KeyboardButton(text=get_button("back_to_main", lang))]
        ],
        resize_keyboard=True
    )


def settings_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button("mailing_settings", lang)), KeyboardButton(text=get_button("language_settings", lang))],
            [KeyboardButton(text=get_button("delete_user", lang))],
            [KeyboardButton(text=get_button("back_to_main", lang))]
        ],
        resize_keyboard=True
)


def mailing_keyboard(lang: str) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=get_button("checkin_checkout_mailing", lang))],
            [KeyboardButton(text=get_button("schedule_today_mailing", lang))],
            [KeyboardButton(text=get_button("back_to_main", lang))]
        ],
        resize_keyboard=True
    )