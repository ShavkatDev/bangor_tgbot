from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any

from config import settings

class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable,
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.from_user.id in settings.ADMINS:
            return await handler(event, data)