import json
from datetime import datetime, timedelta
from sqlalchemy import select, update
from app.db.database import async_session_maker
from app.db.models import ScheduleCache, User
from app.utils.schedule import get_week_start

async def get_cached_schedule(group_id: str, target_date: datetime.date) -> str | None:
    week_start = get_week_start(target_date)

    async with async_session_maker() as session:
        result = await session.execute(
            select(ScheduleCache)
            .where(ScheduleCache.group_id == group_id)
            .where(ScheduleCache.week_start == week_start)
        )
        cache = result.scalars().first()

        if cache and (datetime.utcnow() - cache.updated_at) < timedelta(hours=9):
            return json.loads(cache.data)
        return None


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

async def get_user_group_id(telegram_id: int) -> int | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User.group_id).where(User.telegram_id == telegram_id)
        )
        group_id = result.scalar()
        if group_id is None:
            return None
        
        return group_id