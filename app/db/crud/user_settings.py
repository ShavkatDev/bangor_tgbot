from app.db.models import UserSettings
from sqlalchemy import select, update
from app.db.models import User, UserSettings
from app.db.database import async_session_maker

async def get_user_settings(telegram_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(UserSettings)
            .join(User)
            .where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()

async def toggle_daily_digest(telegram_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(UserSettings)
            .join(User)
            .where(User.telegram_id == telegram_id)
        )
        settings = result.scalars().first()
        if settings:
            settings.daily_digest = not settings.daily_digest
            await session.commit()

async def toggle_today_schedule_digest(telegram_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(UserSettings)
            .join(User)
            .where(User.telegram_id == telegram_id)
        )
        settings = result.scalars().first()
        if settings:
            settings.today_schedule_digest = not settings.today_schedule_digest
            await session.commit()