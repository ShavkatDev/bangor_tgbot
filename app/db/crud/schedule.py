from collections import defaultdict
import json
from datetime import date, datetime
from typing import Optional
from sqlalchemy import select, update
from app.db.database import async_session_maker
from app.db.models import ScheduleCache, User, UserSettings
from app.utils.schedule import get_week_start


async def get_cached_schedule(group_id: str, target_date: datetime.date) -> Optional[str]:
    week_start = get_week_start(target_date)

    async with async_session_maker() as session:
        result = await session.execute(
            select(ScheduleCache)
            .where(ScheduleCache.group_id == group_id)
            .where(ScheduleCache.week_start == week_start)
        )
        cache = result.scalars().first()

        if not cache:
            return None
        
        return cache


async def save_schedule_to_cache(group_id: str, target_date: datetime.date, data: str):
    week_start = get_week_start(target_date)

    async with async_session_maker() as session:
        result = await session.execute(
            select(ScheduleCache)
            .where(ScheduleCache.group_id == group_id)
            .where(ScheduleCache.week_start == week_start)
        )
        existing = result.scalars().first()

        if existing:
            await session.execute(
                update(ScheduleCache)
                .where(ScheduleCache.id == existing.id)
                .values(data=data, updated_at=datetime.utcnow())
            )
        else:
            new_cache = ScheduleCache(
                group_id=group_id,
                week_start=week_start,
                data=data
            )
            session.add(new_cache)

        await session.commit()

async def get_user_group_id(telegram_id: int) -> Optional[int]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User.group_id).where(User.telegram_id == telegram_id)
        )
        group_id = result.scalar()
        if group_id is None:
            return None
        
        return group_id

async def get_users_with_today_digest() -> list[tuple[int, int, str]]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User.telegram_id, User.group_id, UserSettings.language)
            .join(UserSettings, User.id == UserSettings.user_id)
            .where(UserSettings.today_schedule_digest == True)
        )
        return result.all()

async def get_students_by_group_with_digest(group_id: int) -> list[int]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User.telegram_id)
            .join(UserSettings, User.id == UserSettings.user_id)
            .where(User.group_id == group_id)
            .where(UserSettings.daily_digest == True)
        )
        return result.scalars().all()

async def get_all_group_schedules_today(target_date: date) -> dict[int, list[dict]]:
    async with async_session_maker() as session:
        result = await session.execute(select(ScheduleCache))
        rows = result.scalars().all()

    grouped = defaultdict(list)

    for row in rows:
        try:
            lessons = json.loads(row.data)
            for lesson in lessons:
                raw_date = lesson.get("scheduleDate", "")[:10]
                lesson_date = datetime.fromisoformat(raw_date).date()
                if lesson_date == target_date:
                    grouped[row.group_id].append(lesson)
        except Exception:
            continue

    return grouped