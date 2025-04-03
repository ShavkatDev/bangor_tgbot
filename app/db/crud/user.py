from sqlalchemy import select
from app.db.models import User, UserSettings
from app.db.database import async_session_maker
from app.utils.encryption import encrypt, decrypt
    

async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()


async def get_user_language(telegram_id: int) -> str:
    async with async_session_maker() as session:
        result = await session.execute(
            select(UserSettings.language)
            .join(User)
            .where(User.telegram_id == telegram_id)
        )
        lang = result.scalar()
        return lang or "ru"


async def is_user_registered(telegram_id: int) -> bool:
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalars().first() is not None


async def create_user_with_settings(telegram_id: int, student_id: str, password: str, lang: str = "ru"):
    enc_login = encrypt(student_id)
    enc_password = encrypt(password)

    async with async_session_maker() as session:
        new_user = User(
            telegram_id=telegram_id,
            student_id=enc_login,
            password_inet=enc_password,
            university_id=None
        )
        session.add(new_user)
        await session.flush()

        settings = UserSettings(
            user_id=new_user.id,
            daily_digest=True,
            reminders=False,
            language=lang
        )
        session.add(settings)
        await session.commit()
    
async def get_user_by_telegram_id(telegram_id: int) -> User | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        return result.scalars().first()
    
async def get_user_credentials(telegram_id: int) -> tuple[str, str] | None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

        if not user:
            return None

        login = decrypt(user.student_id)
        password = decrypt(user.password_inet)
        return login, password