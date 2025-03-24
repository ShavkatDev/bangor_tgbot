import asyncio
import logging
from datetime import datetime
from timetable import update_schedule_for_group

GROUPS=[232]

async def update_all_groups():
    for group_id in GROUPS:  # позже будет [1, 2, 3]
        result = update_schedule_for_group(group_id)
        logging.info(result)

async def schedule_loop():
    while True:
        now = datetime.now()  # <-- исправлено
        if now.weekday() == 0 and now.hour == 6:
            await update_all_groups()
        await asyncio.sleep(3600)

