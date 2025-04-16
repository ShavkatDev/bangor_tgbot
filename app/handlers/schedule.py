import json
from aiogram import Router, types
from app.db.crud.schedule import get_cached_schedule, get_user_group_id, save_schedule_to_cache
from app.db.crud.user import get_user_credentials
from app.lexicon.lexicon import LEXICON_MSG
from app.utils.text_from_lexicon import TextFromLexicon
from app.keyboards.reply import inet_schedule_keyboard
from app.utils.schedule import fetch_attendance_data, format_attendance, get_token, fetch_schedule_data, format_schedule, get_week_start, sanitize_schedule_data
from datetime import date, datetime, timedelta

schedule_router = Router()

async def get_schedule_text(telegram_id: int, lang: str, mode: str) -> str:
    today = date.today()

    if mode == "tomorrow":
        target_day = today
    elif mode == "week":
        target_day = today if today.weekday() < 6 else today + timedelta(days=1)
    else:
        target_day = today - timedelta(days=1)

    monday = get_week_start(target_day)
    sunday = monday + timedelta(days=6)

    group_id = await get_user_group_id(telegram_id)
    if group_id is None:
        return LEXICON_MSG["user_not_found"][lang]

    cached = await get_cached_schedule(group_id, monday)
    if cached:
        cleaned_data = cached
    else:
        creds = await get_user_credentials(telegram_id)
        if not creds:
            return LEXICON_MSG["user_not_found"][lang]

        login, password = creds
        token = await get_token(login, password)
        if not token:
            return LEXICON_MSG["inet_auth_failed"][lang]

        weekly_data = await fetch_schedule_data(token, monday, sunday)
        if not weekly_data:
            return LEXICON_MSG["unexpected_error"][lang]

        cleaned_data = sanitize_schedule_data(weekly_data)
        await save_schedule_to_cache(group_id, monday, json.dumps(cleaned_data))

    if mode == "week":
        return await format_schedule(cleaned_data, lang)
    else:
        filtered = [
            item for item in cleaned_data
            if datetime.fromisoformat(item["scheduleDate"]).date() == target_day
        ]
        return await format_schedule(filtered, lang)


@schedule_router.message(TextFromLexicon("schedule_today_view"))
async def show_today_schedule(message: types.Message, lang: str):
    text = await get_schedule_text(message.from_user.id, lang, mode="today")
    await message.answer(text, reply_markup=inet_schedule_keyboard(lang))

@schedule_router.message(TextFromLexicon("schedule_tomorrow_view"))
async def show_tomorrow_schedule(message: types.Message, lang: str):
    text = await get_schedule_text(message.from_user.id, lang, mode="tomorrow")
    await message.answer(text, reply_markup=inet_schedule_keyboard(lang))

@schedule_router.message(TextFromLexicon("schedule_week_view"))
async def show_week_schedule(message: types.Message, lang: str):
    text = await get_schedule_text(message.from_user.id, lang, mode="week")
    await message.answer(text, reply_markup=inet_schedule_keyboard(lang))

@schedule_router.message(TextFromLexicon("attendance"))
async def show_attendance(message: types.Message, lang: str):
    telegram_id = message.from_user.id

    creds = await get_user_credentials(telegram_id)
    login, password = creds
    token = await get_token(login, password)
    
    attendance_data = await fetch_attendance_data(telegram_id, token)
    text = format_attendance(attendance_data, lang)

    await message.answer(text)
