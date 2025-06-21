from functools import wraps
from typing import Callable, Sequence, Union

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_inline_keyboard(
    buttons: Sequence[Union[list[str, str], dict]], width: int = 1
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for button in buttons:
        if isinstance(button, list):
            text, callback_data = button
            builder.button(text=text, callback_data=callback_data)
        elif isinstance(button, dict):
            builder.button(**button)
        else:
            raise ValueError(f"Unknown button type: {button}")

    builder.adjust(width)
    return builder.as_markup()


def simple_keyboard(
    func: Callable[..., Sequence[Union[list[str], dict]]],
) -> Callable[..., InlineKeyboardMarkup]:
    @wraps(func)
    def wrapper(*args, **kwargs) -> InlineKeyboardMarkup:
        buttons = func(*args, **kwargs)
        return create_inline_keyboard(buttons)

    return wrapper


def eager(func):
    return func()
