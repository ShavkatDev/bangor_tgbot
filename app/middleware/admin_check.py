from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Awaitable, Callable, Dict, Any

from app.config import settings


class AdminMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        data["is_admin"] = event.from_user.id in settings.ADMINS
        return await handler(event, data)
