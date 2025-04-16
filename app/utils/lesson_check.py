import asyncio
from aiogram import Bot
from datetime import datetime, timedelta, date, time
from app.db.crud.schedule import get_students_by_group_with_digest, get_all_group_schedules_today

notified_set: set[tuple[int, str, str]] = set()

REMINDER_TIMES = [
    (time(9, 35), "entry"),
    (time(10, 55), "exit"),
    (time(10, 55), "entry"),
    (time(12, 25), "exit"),
    (time(12, 35), "entry"),
    (time(13, 55), "exit"),
    (time(13, 55), "entry"),
    (time(15, 25), "exit"),
    (time(15, 35), "entry"),
    (time(16, 55), "exit"),
    (time(17, 05), "entry"),
    (time(18, 25), "exit"),
]

def parse_time(t: str) -> time:
    return datetime.strptime(t, "%H:%M:%S").time()

async def get_lessons_to_check(schedule_data: list[dict], current_time: datetime) -> list[dict]:

    result = []
    now = current_time.time()
    today_str = current_time.date().isoformat()

    for lesson in schedule_data:
        if lesson.get("scheduleStatus") != "ACTIVE":
            continue
        
        if lesson.get("scheduleDate") != today_str:
            continue

        group_id = lesson.get("groupId")
        if group_id is None:
            continue

        students = await get_students_by_group_with_digest(group_id)
        if not students:
            continue

        if not lesson.get("checkIn") and lesson.get("checkinEnd"):
            checkin_end = parse_time(lesson["checkinEnd"])
            window_start = (datetime.combine(date.today(), checkin_end) - timedelta(minutes=5)).time()
            if window_start <= now <= checkin_end:
                result.append({"lesson": lesson, "type": "entry", "students": students})

        if not lesson.get("checkOut") and lesson.get("checkoutEnd"):
            checkout_end = parse_time(lesson["checkoutEnd"])
            window_start = (datetime.combine(date.today(), checkout_end) - timedelta(minutes=5)).time()
            if window_start <= now <= checkout_end:
                result.append({"lesson": lesson, "type": "exit", "students": students})
    
    return result


async def check_lesson_marks(bot: Bot):
    now = datetime.now()
    today = date.today()

    group_schedules = await get_all_group_schedules_today(today)

    for group_id, schedule_data in group_schedules.items():
        lessons_to_check = await get_lessons_to_check(schedule_data, now)

        for entry in lessons_to_check:
            lesson = entry["lesson"]
            students = entry["students"]
            action_type = entry["type"]

            for user_id in students:
                key = (user_id, lesson["moduleName"], action_type)
                if key in notified_set:
                    continue

                if action_type == "entry":
                    text = f"⚠️ Не забудьте пробить карту при входе на пару: {lesson['moduleName']} ({lesson['startTime'][:-3]})"
                else:
                    text = f"⚠️ Не забудьте пробить карту при выходе с пары: {lesson['moduleName']} ({lesson['endTime'][:-3]})"

                try:
                    await bot.send_message(user_id, text)
                    notified_set.add(key)
                except Exception:
                    continue

async def start_lesson_check_task(bot: Bot):
    while True:
        now = datetime.now()

        if now.weekday() < 6:
            for scheduled_time, _ in REMINDER_TIMES:
                if abs((datetime.combine(now.date(), scheduled_time) - now).total_seconds()) < 60:
                    await check_lesson_marks(bot)

        await asyncio.sleep(30)