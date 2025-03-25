import asyncio
import logging
from datetime import datetime
from timetable import update_schedule_for_group

GROUPS = [231, 232, 233]  # Оставляем все группы

async def update_all_groups():
    for group_id in GROUPS:
        if group_id == 232:  # Обновляем только для группы 232
            result = update_schedule_for_group(group_id)
            logging.info(result)
        else:
            logging.info(f"Обновление расписания для группы {group_id} временно недоступно.")

async def schedule_loop():
    while True:
        now = datetime.now()
        if now.weekday() == 0 and now.hour == 6:
            await update_all_groups()
        await asyncio.sleep(3600)