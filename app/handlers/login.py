from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.states import LoginState
from app.utils.auth import verify_credentials
from app.db.crud.user import get_user_language, is_user_registered, create_user_with_settings

from app.keyboards.reply import main_menu_keyboard
from app.lexicon.lexicon import LEXICON_MSG

from datetime import date
from app.utils.schedule import fetch_schedule_data, fetch_user_data

login_router = Router()

@login_router.message(Command("login"))
async def login_command(message: types.Message, state: FSMContext, lang: str):
    msg = await message.answer(
        text=LEXICON_MSG["enter_login"][lang]
    )

    await state.update_data(msg=msg, lang=lang)
    await state.set_state(LoginState.waiting_for_login)


@login_router.message(LoginState.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext, lang: str):
    try:
        await message.delete()
    except:
        pass

    user_data = await state.get_data()
    msg: types.Message = user_data["msg"]

    await state.update_data(student_id=message.text)
    await msg.edit_text(
        text=LEXICON_MSG["enter_password"][lang]
    )
    await state.set_state(LoginState.waiting_for_password)

@login_router.message(LoginState.waiting_for_password)
async def process_password(message: types.Message, state: FSMContext, lang: str):
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

    msg = await message.answer(
        text=LEXICON_MSG["checking_credentials"][lang]
    )

    success, token, inet_id = await verify_credentials(student_id, password)

    if not success:
        await message.answer(
            text=LEXICON_MSG["invalid_credentials"][lang]
        )
        await msg.delete()
        await state.clear()
        return


    user_data = await fetch_user_data(token, inet_id)

    group_name = user_data[0].get("groupName")
    inet_id = user_data[0].get("id")
    semester_id = user_data[0].get("semesterId")

    if not group_name:
        await message.answer(
            text=LEXICON_MSG["group_not_found"][lang]
        )
        await state.clear()
        return
    
    try:
        group_id = int(''.join(filter(str.isdigit, group_name)))
    except ValueError:
        group_id = None

    if await is_user_registered(telegram_id):
        await message.answer(
            text=LEXICON_MSG["already_registered"][lang]
        )
    else:
        await create_user_with_settings(
            telegram_id=telegram_id,
            student_id=student_id,
            password=password,
            group_id=group_id,
            inet_id=inet_id,
            semester_id=semester_id,
            lang="en"
        )

        await message.answer(
            text=LEXICON_MSG["auth_success"][lang],
            reply_markup=main_menu_keyboard(lang)
        )
        
    await msg.delete()
    await state.clear()
