from aiogram import Router, types
from aiogram.filters import CommandStart
from app.db.crud.user import get_user_by_telegram_id

from app.keyboards.reply import main_menu_keyboard
from app.db.crud.user import get_user_language
from app.lexicon.lexicon import LEXICON_MSG
from app.config import is_admin

start_router = Router()

@start_router.message(CommandStart())
async def start_command(message: types.Message):
    telegram_id = message.from_user.id
    lang = await get_user_language(message.from_user.id)
    user = await get_user_by_telegram_id(telegram_id)
    print(type(telegram_id))

    if user:
        await message.answer(text=LEXICON_MSG['greet'][lang], reply_markup=main_menu_keyboard(lang))
    # elif user and is_ad
    else:
        await message.answer(text=LEXICON_MSG['greet_login'][lang])
