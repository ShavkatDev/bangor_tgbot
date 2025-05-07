import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from app.states import LoginState
from app.utils.auth import verify_credentials
from app.db.crud.user import is_user_registered, create_user_with_settings

from app.keyboards.reply_keyboard import main_menu_keyboard
from app.lexicon.lexicon import LEXICON_MSG
from app.keyboards.privacy_keyboard import get_privacy_keyboard

from app.utils.schedule import fetch_user_data

logger = logging.getLogger(__name__)
login_router = Router()

@login_router.message(LoginState.waiting_for_privacy)
async def login_command(message: types.Message, state: FSMContext, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) started login process")
    
    try:
        user_data = await state.get_data()
        if not user_data.get("privacy_accepted"):
            await message.answer(
                text=LEXICON_MSG["privacy_policy_required"][lang],
                reply_markup=get_privacy_keyboard(lang)
            )
            return

        msg = await message.answer(
            text=LEXICON_MSG["enter_login"][lang]
        )

        await state.update_data(msg=msg, lang=lang)
        await state.set_state(LoginState.waiting_for_login)
    except Exception as e:
        logger.error(f"Error in login command for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])


@login_router.message(LoginState.waiting_for_login)
async def process_login(message: types.Message, state: FSMContext, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) entered login")
    
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
async def process_password(message: types.Message, state: FSMContext, lang: str, is_admin: bool):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) entered password")
    
    user_data = await state.get_data()
    msg: types.Message = user_data["msg"]
    student_id = user_data["student_id"]
    password = message.text

    try:
        await message.delete()
        await msg.delete()
    except:
        pass

    msg = await message.answer(
        text=LEXICON_MSG["checking_credentials"][lang]
    )

    try:
        success, token, inet_id = await verify_credentials(student_id, password)

        if not success:
            logger.warning(f"Invalid credentials for user {telegram_id} (@{username})")
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
            logger.warning(f"Group not found for user {telegram_id} (@{username})")
            await message.answer(
                text=LEXICON_MSG["group_not_found"][lang]
            )
            await state.clear()
            return
        
        try:
            group_id = int(''.join(filter(str.isdigit, group_name)))
        except ValueError:
            logger.warning(f"Invalid group name format for user {telegram_id} (@{username}): {group_name}")
            group_id = None

        if await is_user_registered(telegram_id):
            logger.info(f"User {telegram_id} (@{username}) already registered")
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
            logger.info(f"User {telegram_id} (@{username}) successfully registered with group_id={group_id}")

            await message.answer(
                text=LEXICON_MSG["auth_success"][lang],
                reply_markup=main_menu_keyboard(lang, is_admin)
            )
            
        await msg.delete()
        await state.clear()
    except Exception as e:
        logger.error(f"Error in password processing for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])
        await state.clear()
