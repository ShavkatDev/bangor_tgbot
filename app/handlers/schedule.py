from aiogram import Router, types
from app.db.crud.user import get_user_language, get_user_credentials
from app.utils.text_from_lexicon import TextFromLexicon
from app.keyboards.reply import inet_schedule_keyboard
from app.utils.schedule import get_token, fetch_schedule_data, format_schedule
from datetime import date, timedelta

schedule_router = Router()

async def get_schedule_text(telegram_id: int, days_ahead: int = 1) -> str:
    creds = await get_user_credentials(telegram_id)
    if not creds:
        return "❌ Пользователь не найден."

    login, password = creds
    token = await get_token(login, password)

    if not token:
        return "❌ Ошибка авторизации в INET."

    start = date.today()
    end = start + timedelta(days=days_ahead)
    data = await fetch_schedule_data(token, start, end)
    return format_schedule(data)

@schedule_router.message(TextFromLexicon("schedule_tomorrow_view"))
async def show_tomorrow_schedule(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    text = await get_schedule_text(message.from_user.id, days_ahead=1)
    await message.answer(text, reply_markup=inet_schedule_keyboard(lang))


@schedule_router.message(TextFromLexicon("schedule_week_view"))
async def show_week_schedule(message: types.Message):
    lang = await get_user_language(message.from_user.id)
    text = await get_schedule_text(message.from_user.id, days_ahead=7)
    await message.answer(text, reply_markup=inet_schedule_keyboard(lang))
