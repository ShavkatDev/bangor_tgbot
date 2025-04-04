from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.lexicon.lexicon import LEXICON_BUTTONS

def get_button(key: str, lang: str = "en") -> str:
    return LEXICON_BUTTONS.get(key, {}).get(lang, f"[{key}]")

def mailing_settings_keyboard(daily_digest: bool, today_schedule_digest: bool, lang: str) -> InlineKeyboardMarkup:
    def status_text(enabled: bool) -> str:
        return "✅" if enabled else "❌"

    keyboard = [
        [
            InlineKeyboardButton(
                text=f"{status_text(daily_digest)} {get_button('checkin_checkout_mailing', lang)}",
                callback_data="toggle_daily_digest"
            )
        ],
        [
            InlineKeyboardButton(
                text=f"{status_text(today_schedule_digest)} {get_button('schedule_today_mailing', lang)}",
                callback_data="toggle_today_schedule_digest"
            )
        ],
        [
            InlineKeyboardButton(
                text=get_button('back_to_settings', lang),
                callback_data="back_to_settings_menu"
            )
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)