from aiogram.filters import BaseFilter
from aiogram.types import Message
from app.lexicon.lexicon import LEXICON_BUTTONS


class TextFromLexicon(BaseFilter):
    def __init__(self, *keys: str):
        self.keys = keys

    async def __call__(self, message: Message) -> bool:
        for key in self.keys:
            if message.text in LEXICON_BUTTONS.get(key, {}).values():
                return True
        return False
