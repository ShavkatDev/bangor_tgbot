import logging
from sqlalchemy import select, func
from datetime import datetime, timedelta

from app.db.models import User, UserSettings
from app.db.database import async_session_maker

logger = logging.getLogger(__name__)


async def get_total_users() -> int:
    async with async_session_maker() as session:
        result = await session.execute(select(func.count()).select_from(User))
        total = result.scalar_one()
        logger.info(f"[Stats] Total users: {total}")
        return total


async def get_new_users(days: int = 7) -> int:
    since_date = datetime.utcnow() - timedelta(days=days)
    async with async_session_maker() as session:
        result = await session.execute(
            select(func.count()).select_from(User).where(User.created_at >= since_date)
        )
        count = result.scalar_one()
        logger.info(f"[Stats] New users in last {days} days: {count}")
        return count


async def get_users_with_today_digest() -> int:
    async with async_session_maker() as session:
        result = await session.execute(
            select(func.count()).select_from(UserSettings).where(UserSettings.today_schedule_digest.is_(True))
        )
        count = result.scalar_one()
        logger.info(f"[Stats] Users with today's digest: {count}")
        return count


async def get_users_with_daily_digest() -> int:
    async with async_session_maker() as session:
        result = await session.execute(
            select(func.count()).select_from(UserSettings).where(UserSettings.daily_digest.is_(True))
        )
        count = result.scalar_one()
        logger.info(f"[Stats] Users with daily digest: {count}")
        return count


async def get_users_by_language() -> dict[str, int]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(UserSettings.language, func.count()).group_by(UserSettings.language)
        )
        lang_counts = dict(result.all())
        logger.info(f"[Stats] User language distribution: {lang_counts}")
        return lang_counts