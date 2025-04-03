from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.states import LoginState
from app.utils.auth import verify_credentials
from app.db.crud.user import is_user_registered, create_user_with_settings

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

    success = await verify_credentials(student_id, password)

    if not success:
        await message.answer("❌ Неверный логин или пароль. Попробуйте снова через /login")
        await msg.delete()
        await state.clear()
        return

    if await is_user_registered(telegram_id):
        await message.answer("❗️Вы уже зарегистрированы.")
    else:
        await create_user_with_settings(
            telegram_id=telegram_id,
            student_id=student_id,
            password=password,
            lang="en"
        )
        await message.answer("✅ Авторизация прошла успешно!")

    await msg.delete()
    await state.clear()
