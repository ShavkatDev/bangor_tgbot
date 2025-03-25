from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable

import os
from dotenv import load_dotenv

load_dotenv()
ADMINS = os.getenv("ADMIN_IDS").split(",")

class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if str(event.from_user.id) not in ADMINS:
            await event.answer("❌ У вас нет доступа.")
            return
        return await handler(event, data)
