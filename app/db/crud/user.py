import logging
from typing import Optional
from sqlalchemy import select, update, delete
from app.db.models import User, UserSettings
from app.db.database import async_session_maker
from app.utils.encryption import encrypt, decrypt
    

async def get_all_users() -> Optional[User]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User.telegram_id)
        )
        logging.info(f"[User] Fetching all users")
        return result.scalars().all()

async def get_user_by_telegram_id(telegram_id: int) -> Optional[User]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        logging.info(f"[User] Fetching user for telegram_id={telegram_id}")
        return result.scalars().first()

async def get_user_language(telegram_id: int) -> str:
    async with async_session_maker() as session:
        result = await session.execute(
            select(UserSettings.language)
            .join(User)
            .where(User.telegram_id == telegram_id)
        )
        lang = result.scalar()
        logging.info(f"[User] Getting language for telegram_id={telegram_id} → {lang or 'en'}")
        return lang or "en"

async def get_attendance_data(telegram_id: int) -> tuple[int, int]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User.inet_id, User.semester_id)
            .where(User.telegram_id == telegram_id)
        )
        row = result.one_or_none()
        
        
        logging.info(f"[User] Attendance data for telegram_id={telegram_id}")
        if row:
            inet_id, semester_id = row
            return inet_id or 0, semester_id or 0
        else:
            return 0, 0

async def is_user_registered(telegram_id: int) -> bool:
    async with async_session_maker() as session:
        result = await session.execute(select(User).where(User.telegram_id == telegram_id))
        logging.info(f"[User] Check registration status for telegram_id={telegram_id}")
        return result.scalars().first() is not None


async def create_user_with_settings(
        telegram_id: int, student_id: str, password: str, 
        group_id: int, inet_id: int, semester_id: int, lang: str = "ru"
    ):

    enc_login = encrypt(student_id)
    enc_password = encrypt(password)

    async with async_session_maker() as session:
        new_user = User(
            telegram_id=telegram_id,
            student_id=enc_login,
            password_inet=enc_password,
            group_id=group_id,
            inet_id=inet_id,
            semester_id=semester_id,
            university_id=None
        )
        session.add(new_user)
        await session.flush()

        settings = UserSettings(
            user_id=new_user.id,
            language=lang
        )
        session.add(settings)
        logging.info(f"[User] Created user telegram_id={telegram_id}, group_id={group_id}")
        await session.commit()
    
async def get_user_credentials(telegram_id: int) -> Optional[tuple[str, str]]:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

        if not user:
            return None

        login = decrypt(user.student_id)
        password = decrypt(user.password_inet)
        logging.info(f"[User] Credentials decrypted for telegram_id={telegram_id}")
        return login, password
    
async def update_user_language(telegram_id: int, lang: str) -> None:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

        if not user:
            return

        await session.execute(
            update(UserSettings)
            .where(UserSettings.user_id == user.id)
            .values(language=lang)
        )

        logging.info(f"[User] Updated language to '{lang}' for telegram_id={telegram_id}")
        await session.commit()

async def delete_user_completely(telegram_id: int) -> bool:
    async with async_session_maker() as session:
        result = await session.execute(
            select(User).where(User.telegram_id == telegram_id)
        )
        user = result.scalars().first()

        if not user:
            logging.warning(f"[User] Tried to delete non-existent user telegram_id={telegram_id}")
            return False

        await session.execute(
            delete(UserSettings).where(UserSettings.user_id == user.id)
        )

        await session.execute(
            delete(User).where(User.id == user.id)
        )

        await session.commit()
        logging.info(f"[User] Deleted user and settings for telegram_id={telegram_id}")
        return True