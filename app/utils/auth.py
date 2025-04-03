from app.config import TIMETABLE_HEADERS
import httpx

async def verify_credentials(login: str, password: str) -> tuple[bool, str | None]:
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://inet.mdis.uz/oauth/tocken",
            headers=TIMETABLE_HEADERS,
            data={
                "username": login,
                "password": password,
                "grant_type": "password"
            }
        )
        if response.status_code == 200:
            return True
        return False