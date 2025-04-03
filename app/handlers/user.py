from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from sqlalchemy import select
from app.db.models import User, UserSettings
from app.db.database import async_session_maker
from app.states import LoginState
from app.utils.auth import verify_credentials
from app.utils.encryption import encrypt

login_router = Router()

@login_router.message(Command("login"))
async def login_command(message: types.Message, state: FSMContext):
    msg = await message.answer("🔐 Введите ваш логин от INET:")
    await state.update_data(msg=msg)
    await state.set_state(LoginState.waiting_for_login)


@login_router.message(LoginState.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext):
    try:
        await message.delete()
    except:
        pass

    user_data = await state.get_data()
    msg: types.Message = user_data["msg"]

    await state.update_data(student_id=message.text)
    await msg.edit_text("🔐 Теперь введите пароль:")
    await state.set_state(LoginState.waiting_for_password)


@login_router.message(LoginState.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext):
    user_data = await state.get_data()
    msg: types.Message = user_data["msg"]
    student_id = user_data["student_id"]
    password = message.text
    telegram_id = message.from_user.id

    try:
        await message.delete()
        await msg.delete()
    except:
        pass

    msg = await message.answer("⏳ Проверяю логин и пароль...")

    success, token = await verify_credentials(student_id, password)

    if not success:
        await message.answer("❌ Неверный логин или пароль. Попробуйте снова через /login")
        await state.clear()
        await msg.delete()
        return

    enc_login = encrypt(student_id)
    enc_password = encrypt(password)

    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        existing_user = result.scalars().first()

        if existing_user:
            await message.answer("❗️Вы уже зарегистрированы.")
        else:
            new_user = User(
                telegram_id=telegram_id,
                student_id=enc_login,
                password_inet=enc_password,
                university_id=None
            )
            session.add(new_user)
            await session.flush()

            settings = UserSettings(
                user_id=new_user.id,
                daily_digest=True,
                reminders=False,
                language='ru'
            )
            session.add(settings)
            await session.commit()

    await message.answer("✅ Авторизация прошла успешно!")
    await msg.delete()
    await state.clear()
