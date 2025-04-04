from aiogram import BaseMiddleware
from aiogram.types import Message

class IgnoreGroupChatsMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if event.chat.type in ("group", "supergroup"):
            return
        return await handler(event, data)