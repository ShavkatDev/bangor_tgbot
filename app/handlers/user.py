from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from app.database import async_session_maker
from app.models import User, UserSettings
from app.utils.crypto import encrypt
from sqlalchemy import select
from app.config import ADMIN_IDS

user_router = Router()

# Состояния FSM
class LoginState(StatesGroup):
    login = State()
    password = State()

@user_router.message(Command("login"))
async def start_login(message: types.Message, state: FSMContext):
    await message.answer("Введите ваш логин INET:")
    await state.set_state(LoginState.login)

@user_router.message(LoginState.login)
async def process_login(message: types.Message, state: FSMContext):
    await state.update_data(login=message.text.strip())
    await message.answer("Введите ваш пароль INET:")
    await state.set_state(LoginState.password)
    await message.delete()

@user_router.message(LoginState.password)
async def process_password(message: types.Message, state: FSMContext):
    data = await state.get_data()
    login = data["login"]
    password = message.text.strip()


    telegram_id = message.from_user.id
    enc_login = encrypt(login)
    enc_password = encrypt(password)

    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        user = result.scalars().first()

        if user:
            await message.answer("Вы уже зарегистрированы.")
        else:
            new_user = User(
                telegram_id=telegram_id,
                login_enc=enc_login,
                password_enc=enc_password,
                university_id=1  # пока один университет
            )
            session.add(new_user)
            await session.flush()  # получить user.id

            settings = UserSettings(
                user_id=new_user.id
            )
            session.add(settings)
            await session.commit()
            await message.answer("✅ Регистрация прошла успешно!")

    await state.clear()
    await message.delete()
