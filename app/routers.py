from aiogram import Dispatcher

from app.handlers.chat_events import chat_router
from app.handlers.start import start_router
from app.handlers.login import login_router
from app.handlers.main_menu import main_menu_router
from app.handlers.schedule import schedule_router
from app.handlers.settings import settings_router
from app.handlers.support import support_router
from app.handlers.privacy import privacy_router
from app.handlers.navigation import navigation_router
from app.admin.admin import admin_router


def setup_routers(dp: Dispatcher):
    dp.include_router(chat_router)
    dp.include_router(start_router)
    dp.include_router(privacy_router)
    dp.include_router(login_router)
    dp.include_router(main_menu_router)
    dp.include_router(schedule_router)
    dp.include_router(settings_router)
    dp.include_router(support_router)
    dp.include_router(navigation_router)
    dp.include_router(admin_router)
