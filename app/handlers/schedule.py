from aiogram import Router, types
from app.db.crud.user import get_user_language, get_user_credentials
from app.lexicon.lexicon import LEXICON_MSG
from app.utils.text_from_lexicon import TextFromLexicon
from app.keyboards.reply import inet_schedule_keyboard
from app.utils.schedule import fetch_attendance_data, format_attendance, get_token, fetch_schedule_data, format_schedule
from datetime import date, timedelta

schedule_router = Router()

async def get_schedule_text(telegram_id: int, mode: str = "tomorrow") -> str:
    creds = await get_user_credentials(telegram_id)

    lang = await get_user_language(telegram_id)
    if not creds:
        return LEXICON_MSG['user_not_found'][lang]

    login, password = creds
    token = await get_token(login, password)

    if not token:
        return LEXICON_MSG['inet_auth_failed'][lang]

    today = date.today()

    if mode == "tomorrow":
        start = today + timedelta(days=1)
        end = start

    elif mode == "week":
        if today.weekday() == 6:
            monday = today + timedelta(days=1)
            sunday = monday + timedelta(days=6)
        else:
            monday = today - timedelta(days=today.weekday())
            sunday = monday + timedelta(days=6)

        start = monday
        end = sunday

    else:
        start = today + timedelta(days=1)
        end = start

    data = await fetch_schedule_data(token, start, end)

    return await format_schedule(data, lang)

@schedule_router.message(TextFromLexicon("schedule_tomorrow_view"))
async def show_tomorrow_schedule(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    text = await get_schedule_text(message.from_user.id, mode="tomorrow")
    await message.answer(text, reply_markup=inet_schedule_keyboard(lang))

@schedule_router.message(TextFromLexicon("schedule_week_view"))
async def show_week_schedule(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    text = await get_schedule_text(message.from_user.id, mode="week")
    await message.answer(text, reply_markup=inet_schedule_keyboard(lang))

@schedule_router.message(TextFromLexicon("attendance"))
async def show_attendance(message: types.Message):
    telegram_id = message.from_user.id
    lang = await get_user_language(telegram_id)

    creds = await get_user_credentials(telegram_id)
    login, password = creds
    token = await get_token(login, password)
    
    attendance_data = await fetch_attendance_data(telegram_id, token)
    text = format_attendance(attendance_data, lang)

    await message.answer(text)
