from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.lexicon.lexicon import LEXICON_BUTTONS


class TextFromLexicon(BaseFilter):
    def __init__(self, key: str):
        self.key = key

    async def __call__(self, message: Message) -> bool:
        return message.text in LEXICON_BUTTONS.get(self.key, {}).values()