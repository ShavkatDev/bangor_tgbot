from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.db.crud.user import get_user_language
from app.keyboards.reply import main_menu_keyboard, inet_schedule_keyboard
from app.lexicon.lexicon import LEXICON_MSG
from app.utils.text_from_lexicon import TextFromLexicon

main_menu_router = Router()

@main_menu_router.message(Command("menu"))
async def show_main_menu(message: Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["main_menu_title"][lang],
        reply_markup=main_menu_keyboard(lang)
    )

@main_menu_router.message(TextFromLexicon('inet_schedule'))
async def open_inet_schedule_menu(message: Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["choose_schedule"][lang],
        reply_markup=inet_schedule_keyboard(lang)
    )

@main_menu_router.message(TextFromLexicon('back_to_main'))
async def back_to_main_menu(message: Message):
    lang = await get_user_language(message.from_user.id)
    await message.answer(
        text=LEXICON_MSG["main_menu_title"][lang],
        reply_markup=main_menu_keyboard(lang)
    )