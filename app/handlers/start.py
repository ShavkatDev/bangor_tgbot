from aiogram import Router, types
from aiogram.filters import CommandStart
from app.db.crud.user import get_user_by_telegram_id

from app.keyboards.reply import main_menu_keyboard
from app.lexicon.lexicon import LEXICON_MSG

start_router = Router()

@start_router.message(CommandStart())
async def start_command(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    user = await get_user_by_telegram_id(telegram_id)

    if user:
        await message.answer(text=LEXICON_MSG['greet'][lang], reply_markup=main_menu_keyboard(lang))
    else:
        await message.answer(text=LEXICON_MSG['greet_login'][lang])
