from app.utils.inline import eager
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@eager
def nav_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Outlook", url="https://outlook.office365.com/mail/"
                ),
                InlineKeyboardButton(
                    text="BlackBoard",
                    url="https://elearning.mdis.edu.sg/",
                ),
            ],
            [
                InlineKeyboardButton(text="Inet", url="https://inet.mdis.uz/"),
            ],
        ]
    )
