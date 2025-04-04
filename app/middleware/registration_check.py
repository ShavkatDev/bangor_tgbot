from aiogram import BaseMiddleware
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from app.db.crud.user import get_user_by_telegram_id, get_user_language
from app.states import LoginState

from app.lexicon.lexicon import LEXICON_MSG

class RegistrationCheckMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        state: FSMContext = data.get('state')
        if state:
            current_state = await state.get_state()
            if current_state in [LoginState.waiting_for_login, LoginState.waiting_for_password]:
                # Если пользователь находится в процессе регистрации — пропускаем проверку
                return await handler(event, data)

        if event.text and event.text.startswith(('/start', '/login')):
            return await handler(event, data)
        
        lang: str = await get_user_language(event.from_user.id)

        user = await get_user_by_telegram_id(event.from_user.id)
        if not user:
            await event.answer(
                text=LEXICON_MSG["registration_required"][lang]
            )
            return

        return await handler(event, data)
