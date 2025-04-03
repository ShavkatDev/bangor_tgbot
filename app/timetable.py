import os
import requests
import httpx
import json
from collections import defaultdict
from datetime import date, timedelta

from app.config import TIMETABLE_HEADERS
from app.utils.date_utils import get_day_name

API_URL = "https://inet.mdis.uz/api/v1/education/student/view/schedules"

async def get_token_async(login: str, password: str) -> str | None:
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
    
# def fetch_schedule_data(token: str, start: date, end: date):
#     headers = TIMETABLE_HEADERS.copy()
#     headers["Authorization"] = f"Bearer {token}"
#     response = requests.get(
#         f"{API_URL}?from={start}&to={end}",
#         headers=headers
#     )
#     if response.status_code == 200:
#         return response.json().get("data", [])
#     return []

# def format_schedule(data: list) -> str:
#     if not data:
#         return "На этой неделе занятий нет 🎉"

#     data.sort(key=lambda x: (x["scheduleDate"], x["startTime"]))
#     grouped = defaultdict(list)

#     for lesson in data:
#         day_name = get_day_name(lesson["scheduleDate"])
#         time = f"{lesson['startTime'][:-3]}–{lesson['endTime'][:-3]}"
#         subject = lesson["moduleName"]
#         venue = lesson["venueName"]
#         lecturer = lesson["lecturerName"]
#         lesson_type = lesson["lessonTypeName"]

#         lesson_text = (
#             f"🕐 {time} — {subject} ({lesson_type})\n"
#             f"🏫 Classroom: {venue}\n"
#             f"👨‍🏫 Teacher: {lecturer}\n"
#         )
#         grouped[day_name].append(lesson_text)

#     final_lines = []
#     for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
#         if day in grouped:
#             final_lines.append(f"📅 <b>{day}</b>")
#             final_lines.extend(grouped[day])
#             final_lines.append("")

#     return "\n".join(final_lines)

# def cache_schedule(group_id: int, text: str):
#     os.makedirs("schedule_cache", exist_ok=True)
#     with open(f"schedule_cache/group_{group_id}.json", "w", encoding="utf-8") as f:
#         json.dump({"text": text}, f, ensure_ascii=False, indent=2)

# def load_cached_schedule(group_id: int) -> str:
#     try:
#         with open(f"schedule_cache/group_{group_id}.json", "r", encoding="utf-8") as f:
#             return json.load(f)["text"]
#     except FileNotFoundError:
#         return "⚠️ Расписание ещё не загружено."

# def update_schedule_for_group(group_id: int):
#     """Main function to update schedule for a given group ID."""
#     token = get_token_for_group(group_id)
#     if not token:
#         return "❌ Не удалось получить токен."

#     today = date.today()
#     monday = today - timedelta(days=today.weekday())
#     sunday = monday + timedelta(days=6)

#     data = fetch_schedule_data(token, monday.isoformat(), sunday.isoformat())

#     formatted = format_schedule(data)
#     cache_schedule(group_id, formatted)
#     return f"✅ Расписание для группы {group_id} обновлено."


