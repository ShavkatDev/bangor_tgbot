import json
import logging
from aiogram import Router, types
from app.db.crud.schedule import get_cached_schedule, get_user_group_id, save_schedule_to_cache
from app.db.crud.user import get_user_credentials
from app.lexicon.lexicon import LEXICON_MSG
from app.utils.text_from_lexicon import TextFromLexicon
from app.keyboards.reply_keyboard import inet_schedule_keyboard
from app.utils.schedule import fetch_attendance_data, format_attendance, get_token, fetch_schedule_data, format_schedule, get_week_start, sanitize_schedule_data
from datetime import date, datetime, timedelta

logger = logging.getLogger(__name__)
schedule_router = Router()

async def get_schedule_text(telegram_id: int, lang: str, mode: str) -> str:
    today = date.today()
    username = "Unknown"  # We'll get the username from the message context

    if mode == "tomorrow":
        target_day = today
    elif mode == "week":
        target_day = today if today.weekday() < 6 else today + timedelta(days=1)
    else:
        target_day = today - timedelta(days=1)

    monday = get_week_start(target_day)
    sunday = monday + timedelta(days=6)

    logger.info(f"Getting schedule for user {telegram_id}, mode={mode}, target_day={target_day}")

    group_id = await get_user_group_id(telegram_id)
    if group_id is None:
        logger.warning(f"Group ID not found for user {telegram_id}")
        return LEXICON_MSG["user_not_found"][lang]

    cached = None
    cache = await get_cached_schedule(group_id, monday)
    if cache and (datetime.utcnow() - cache.updated_at) < timedelta(hours=9):
        logger.info(f"Using cached schedule for group_id={group_id}, updated_at={cache.updated_at}")
        cached = json.loads(cache.data)
    
    if cached:
        cleaned_data = cached
    else:
        logger.info(f"Cache miss for group_id={group_id}, fetching fresh data")
        creds = await get_user_credentials(telegram_id)
        if not creds:
            logger.warning(f"Credentials not found for user {telegram_id}")
            return LEXICON_MSG["user_not_found"][lang]

        login, password = creds
        token = await get_token(login, password)
        if not token:
            logger.warning(f"Failed to get token for user {telegram_id}")
            return LEXICON_MSG["inet_auth_failed"][lang]

        weekly_data = await fetch_schedule_data(token, monday, sunday)
        if not weekly_data:
            logger.error(f"Failed to fetch schedule data for user {telegram_id}")
            return LEXICON_MSG["unexpected_error"][lang]

        cleaned_data = sanitize_schedule_data(weekly_data)
        await save_schedule_to_cache(group_id, monday, json.dumps(cleaned_data))
        logger.info(f"Saved new schedule to cache for group_id={group_id}")

    if mode == "week":
        return await format_schedule(cleaned_data, lang)
    else:
        filtered = [
            item for item in cleaned_data
            if datetime.fromisoformat(item["scheduleDate"].replace('+0000', '+00:00')).date() == target_day
        ]
        return await format_schedule(filtered, lang)


@schedule_router.message(TextFromLexicon("schedule_today_view"))
async def show_today_schedule(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) requested today's schedule")
    
    try:
        text = await get_schedule_text(telegram_id, lang, mode="today")
        await message.answer(text, reply_markup=inet_schedule_keyboard(lang))
    except Exception as e:
        logger.error(f"Error showing today's schedule for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(LEXICON_MSG['error'][lang])

@schedule_router.message(TextFromLexicon("schedule_tomorrow_view"))
async def show_tomorrow_schedule(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) requested tomorrow's schedule")
    
    try:
        text = await get_schedule_text(telegram_id, lang, mode="tomorrow")
        await message.answer(text, reply_markup=inet_schedule_keyboard(lang))
    except Exception as e:
        logger.error(f"Error showing tomorrow's schedule for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(LEXICON_MSG['error'][lang])

@schedule_router.message(TextFromLexicon("schedule_week_view"))
async def show_week_schedule(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) requested week schedule")
    
    try:
        text = await get_schedule_text(telegram_id, lang, mode="week")
        await message.answer(text, reply_markup=inet_schedule_keyboard(lang))
    except Exception as e:
        logger.error(f"Error showing week schedule for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(LEXICON_MSG['error'][lang])

@schedule_router.message(TextFromLexicon("attendance"))
async def show_attendance(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) requested attendance")
    
    try:
        creds = await get_user_credentials(telegram_id)
        if not creds:
            logger.warning(f"Credentials not found for user {telegram_id}")
            await message.answer(LEXICON_MSG["user_not_found"][lang])
            return

        login, password = creds
        token = await get_token(login, password)
        if not token:
            logger.warning(f"Failed to get token for user {telegram_id}")
            await message.answer(LEXICON_MSG["inet_auth_failed"][lang])
            return
        
        attendance_data = await fetch_attendance_data(telegram_id, token)
        text = format_attendance(attendance_data, lang)
        await message.answer(text)
    except Exception as e:
        logger.error(f"Error showing attendance for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(LEXICON_MSG['error'][lang])
