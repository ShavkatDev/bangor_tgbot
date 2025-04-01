from aiogram import Router, types
from aiogram.filters import CommandStart
from sqlalchemy import select
from app.database import async_session_maker
from app.models import User
from app.config import ADMIN_IDS

start_router = Router()

@start_router.message(CommandStart())
async def start_command(message: types.Message):
    telegram_id = message.from_user.id

    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

    # if telegram_id in ADMIN_IDS:
    #     await message.answer("👋 Привет, админ! Готов к работе.")
    #     return

    if user:
        await message.answer("👋 Привет! Вы уже зарегистрированы. Используйте /help для списка команд.")
    else:
        await message.answer(
            "👋 Привет! Добро пожаловать. Чтобы продолжить, пожалуйста, авторизуйтесь командой /login"
        )
