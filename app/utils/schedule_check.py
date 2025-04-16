from datetime import datetime, timedelta, date
from app.db.crud.user import get_user_credentials
from app.db.crud.schedule import get_users_with_today_digest, get_cached_schedule, save_schedule_to_cache
from app.utils.schedule import fetch_schedule_data, get_token, format_schedule, sanitize_schedule_data

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from aiogram import Bot
import json

async def send_today_schedule_digest(bot: Bot):
    today = date.today() - timedelta(days=1)
    monday = today - timedelta(days=today.weekday())
    sunday = monday + timedelta(days=6)

    users = await get_users_with_today_digest()

    group_map = {}
    for telegram_id, group_id, lang in users:
        group_map.setdefault(group_id, []).append((telegram_id, lang))
        

    for group_id, student_list in group_map.items():
        cached = await get_cached_schedule(group_id, monday)

        if not cached or (datetime.utcnow() - cached.updated_at) > timedelta(hours=9):
            first_telegram_id = student_list[0][0]
            creds = await get_user_credentials(first_telegram_id)
            if not creds:
                continue
            login, password = creds
            token = await get_token(login, password)
            if not token:
                continue
            data = await fetch_schedule_data(token, monday, sunday)
            if not data:
                continue
            cleaned = sanitize_schedule_data(data)
            await save_schedule_to_cache(group_id, monday, json.dumps(cleaned))
        else:
            cleaned = json.loads(cached.data)

        today_data = [
            item for item in cleaned
            if datetime.fromisoformat(item["scheduleDate"].replace('+0000', '+00:00')).date() == today
        ]
        if not today_data:
            continue

        for telegram_id, lang in student_list:
            try:
                text = await format_schedule(today_data, lang)
                #testing
                if not telegram_id not in 845102332:
                    continue
                await bot.send_message(telegram_id, text)
            except Exception:
                continue

def setup_digest_scheduler(bot: Bot):
    scheduler = AsyncIOScheduler(timezone="UTC")
    scheduler.add_job(
        send_today_schedule_digest,
        CronTrigger(hour=8, minute=50),
        args=[bot],
        id="daily_schedule_digest",
        replace_existing=True
    )
    scheduler.start()


        
