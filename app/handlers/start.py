from aiogram import Router, types
from aiogram.filters import CommandStart
from app.db.crud.user import get_user_by_telegram_id

from app.keyboards.reply import main_menu_keyboard
from app.db.crud.user import get_user_language

start_router = Router()

@start_router.message(CommandStart())
async def start_command(message: types.Message):
    telegram_id = message.from_user.id
    lang = await get_user_language(message.from_user.id)
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        await message.answer("👋 Привет!", reply_markup=main_menu_keyboard(lang))
    else:
        await message.answer("👋 Привет! Чтобы продолжить, пожалуйста, авторизуйтесь командой /login")
