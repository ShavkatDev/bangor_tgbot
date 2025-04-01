from aiogram import Dispatcher
from app.handlers.chat_events import chat_router
from app.handlers.start import start_router
from app.handlers.user import user_router

def setup_routers(dp: Dispatcher):
    dp.include_router(chat_router)
    dp.include_router(start_router)
    dp.include_router(user_router)
