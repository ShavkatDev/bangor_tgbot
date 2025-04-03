from aiogram import Router, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from app.db.models import User, UserSettings
from app.db.database import async_session_maker
from app.states import LoginState
from app.utils.auth import verify_credentials
from app.utils.encryption import encrypt

start_router = Router()

@start_router.message(CommandStart())
async def start_command(message: types.Message):
    telegram_id = message.from_user.id

    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

    if user:
        await message.answer("👋 Привет! Вы уже зарегистрированы.")
    else:
        await message.answer("👋 Привет! Чтобы продолжить, пожалуйста, авторизуйтесь командой /login")
