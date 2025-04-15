from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from app.config import get_button

def delete_keyboard(lang: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{get_button('delete_approve', lang)} ", callback_data="delete_approve"),
                InlineKeyboardButton(text=f"{get_button('delete_decline', lang)}", callback_data="delete_decline")
            ]
        ]
    )