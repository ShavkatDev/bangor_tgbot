from pydantic_settings import BaseSettings
from typing import List

from app.lexicon.lexicon import LEXICON_BUTTONS


class Settings(BaseSettings):
    TOKEN: str
    DATABASE_URL: str
    FERNET_KEY: str
    ADMINS: List[int] = []

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()


async def is_admin(id: int) -> bool:
    if id in settings.ADMINS:
        return True
    return False


def get_button(key: str, lang: str = "en") -> str:
    return LEXICON_BUTTONS.get(key, {}).get(lang, f"[{key}]")


TIMETABLE_HEADERS = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "Authorization": "Basic c3ByaW5nLXNlY3VyaXR5LW9hdXRoMi1yZWFkLWNsaWVudDpzcHJpbmctc2VjdXJpdHktb2F1dGgyLXJlYWQtY2xpZW50LXBhc3N3b3JkMTIzNA==",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Content-type": "application/x-www-form-urlencoded",
    "Origin": "https://inet.mdis.uz",
    "Pragma": "no-cache",
    "Referer": "https://inet.mdis.uz/auth/login",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-origin",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "X-KL-kfa-Ajax-Request": "Ajax_Request",
    "sec-ch-ua": '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
}
