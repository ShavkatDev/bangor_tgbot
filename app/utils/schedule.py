from datetime import date
from collections import defaultdict
import httpx
from app.config import TIMETABLE_HEADERS
from app.utils.date_utils import get_day_name


async def get_token(login: str, password: str) -> str | None:
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
            return response.json().get("access_token")
        return None


async def fetch_schedule_data(token: str, start: date, end: date) -> list:
    headers = TIMETABLE_HEADERS.copy()
    headers["Authorization"] = f"Bearer {token}"
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://inet.mdis.uz/api/v1/education/student/view/schedules?from={start}&to={end}",
            headers=headers
        )
        if response.status_code == 200:
            return response.json().get("data", [])
        return []


def format_schedule(data: list) -> str:
    if not data:
        return "📭 На указанный период занятий нет."

    data.sort(key=lambda x: (x["scheduleDate"], x["startTime"]))
    grouped = defaultdict(list)

    for lesson in data:
        day_name = get_day_name(lesson["scheduleDate"])
        time = f"{lesson['startTime'][:-3]}–{lesson['endTime'][:-3]}"
        subject = lesson["moduleName"]
        venue = lesson["venueName"]
        lecturer = lesson["lecturerName"]
        lesson_type = lesson["lessonTypeName"]

        lesson_text = (
            f"🕐 {time} — {subject} ({lesson_type})\n"
            f"🏫 Кабинет: {venue}\n"
            f"👨‍🏫 Преподаватель: {lecturer}\n"
        )
        grouped[day_name].append(lesson_text)

    final_lines = []
    for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
        if day in grouped:
            final_lines.append(f"📅 <b>{day}</b>")
            final_lines.extend(grouped[day])
            final_lines.append("")

    return "\n".join(final_lines)
