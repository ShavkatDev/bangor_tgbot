import logging
from aiogram import Bot
from datetime import datetime, timedelta, date, time

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.db.crud.schedule import get_students_by_group_with_digest, get_all_group_schedules_today
from app.lexicon.lexicon import LEXICON_MSG
from app.db.crud.user import get_user_language

logger = logging.getLogger(__name__)

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
    (time(17, 5), "entry"),
    (time(18, 25), "exit"),
]

def parse_time(t: str) -> time:
    try:
        return datetime.strptime(t, "%H:%M:%S").time()
    except ValueError as e:
        logger.error(f"Failed to parse time {t}: {e}")
        return None

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
            logger.warning(f"Lesson {lesson.get('moduleName')} has no group_id")
            continue

        students = await get_students_by_group_with_digest(group_id)
        if not students:
            logger.debug(f"No students with digest enabled for group_id={group_id}")
            continue

        if not lesson.get("checkIn") and lesson.get("checkinEnd"):
            checkin_end = parse_time(lesson["checkinEnd"])
            if checkin_end is None:
                continue
            window_start = (datetime.combine(date.today(), checkin_end) - timedelta(minutes=5)).time()
            if window_start <= now <= checkin_end:
                result.append({"lesson": lesson, "type": "entry", "students": students})
                logger.debug(f"Added entry check for {lesson['moduleName']} at {checkin_end}")

        if not lesson.get("checkOut") and lesson.get("checkoutEnd"):
            checkout_end = parse_time(lesson["checkoutEnd"])
            if checkout_end is None:
                continue
            window_start = (datetime.combine(date.today(), checkout_end) - timedelta(minutes=5)).time()
            if window_start <= now <= checkout_end:
                result.append({"lesson": lesson, "type": "exit", "students": students})
                logger.debug(f"Added exit check for {lesson['moduleName']} at {checkout_end}")
    
    return result

async def check_lesson_marks(bot: Bot):
    try:
        now = datetime.now()
        today = date.today()
        logger.info(f"Starting lesson check at {now}")

        # Test message for admin
        try:
            admin_lang = await get_user_language(845102332) or "en"
            await bot.send_message(
                845102332,
                LEXICON_MSG["lesson_check_test_start"][admin_lang].format(
                    now.strftime('%H:%M:%S'),
                    today
                )
            )
        except Exception as e:
            logger.error(f"Failed to send test message: {str(e)}", exc_info=True)

        group_schedules = await get_all_group_schedules_today(today)
        if not group_schedules:
            logger.warning(f"No schedules found for {today}")
            return

        for group_id, schedule_data in group_schedules.items():
            lessons_to_check = await get_lessons_to_check(schedule_data, now)
            logger.info(f"Found {len(lessons_to_check)} lessons to check for group_id={group_id}")

            # Test message with found lessons
            try:
                admin_lang = await get_user_language(845102332) or "en"
                await bot.send_message(
                    845102332,
                    LEXICON_MSG["lesson_check_test_found"][admin_lang].format(
                        len(lessons_to_check),
                        group_id
                    )
                )
            except Exception as e:
                logger.error(f"Failed to send test message: {str(e)}", exc_info=True)

            for entry in lessons_to_check:
                lesson = entry["lesson"]
                students = entry["students"]
                action_type = entry["type"]

                for user_id in students:
                    key = (user_id, lesson["moduleName"], action_type)
                    if key in notified_set:
                        logger.debug(f"Already notified user {user_id} for {lesson['moduleName']} {action_type}")
                        continue

                    # Get user's language preference
                    user_lang = await get_user_language(user_id) or "en"
                    
                    if action_type == "entry":
                        text = LEXICON_MSG["lesson_check_entry"][user_lang].format(
                            lesson['moduleName'],
                            lesson['startTime'][:-3]
                        )
                    else:
                        text = LEXICON_MSG["lesson_check_exit"][user_lang].format(
                            lesson['moduleName'],
                            lesson['endTime'][:-3]
                        )

                    try:
                        await bot.send_message(user_id, text)
                        logger.info(f"Sent notification to user {user_id}: {text}")
                        notified_set.add(key)
                    except Exception as e:
                        logger.error(f"Failed to send notification to user {user_id}: {str(e)}", exc_info=True)
                        continue

    except Exception as e:
        logger.error(f"Error in check_lesson_marks: {str(e)}", exc_info=True)

def setup_lesson_check_scheduler(bot: Bot):
    try:
        scheduler = AsyncIOScheduler(timezone="UTC")
        logger.info("Setting up lesson check scheduler")

        for t, label in REMINDER_TIMES:
            scheduler.add_job(
                check_lesson_marks,
                trigger=CronTrigger(hour=t.hour, minute=t.minute, day_of_week='mon-sat'),
                args=[bot],
                id=f"lesson_check_{t.hour}_{t.minute}_{label}",
                replace_existing=True
            )
            logger.info(f"Added job for {t.hour}:{t.minute} ({label})")

        scheduler.start()
        logger.info("Lesson check scheduler started successfully")
    except Exception as e:
        logger.error(f"Failed to setup lesson check scheduler: {str(e)}", exc_info=True)
        raise