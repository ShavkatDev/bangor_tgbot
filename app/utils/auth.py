import httpx
from typing import Tuple, Optional
from app.config import TIMETABLE_HEADERS

async def verify_credentials(login: str, password: str) -> Tuple[bool, Optional[str], Optional[int]]:
    token = None
    inet_id = None

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://inet.mdis.uz/oauth/tocken",
                headers=TIMETABLE_HEADERS,
                data={
                    "username": login,
                    "password": password,
                    "grant_type": "password"
                },
                timeout=10
            )

        if response.status_code == 200:
            try:
                res = response.json()
                token = res.get("access_token")
                user_info = res.get("user", {})
                if isinstance(user_info, dict):
                    inet_id = user_info.get("id")
            except Exception:
                return False, None, None

            return True, token, inet_id

        else:
            return False, None, None

    except httpx.RequestError:
        return False, None, None

    except Exception:
        return False, None, None