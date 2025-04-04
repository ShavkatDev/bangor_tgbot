from aiogram import Dispatcher

from app.handlers.chat_events import chat_router
from app.handlers.start import start_router
from app.handlers.login import login_router
from app.handlers.main_menu import main_menu_router
from app.handlers.schedule import schedule_router
from app.handlers.settings import settings_router

def setup_routers(dp: Dispatcher):
    dp.include_router(chat_router)
    dp.include_router(start_router)
    dp.include_router(login_router)
    dp.include_router(main_menu_router)
    dp.include_router(schedule_router)
    dp.include_router(settings_router)