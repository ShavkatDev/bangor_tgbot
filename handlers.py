from aiogram import Dispatcher, types, F, Router
from aiogram.filters import Command
from keyboard import main_menu_kb, group_choice_kb

from timetable import load_cached_schedule
from admin import AdminMiddleware

admin_router = Router()
admin_router.message.middleware(AdminMiddleware())

@admin_router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Чем могу помочь?", reply_markup=main_menu_kb)

# 📌 Кнопка "📅 Расписание" → выбор группы
@admin_router.callback_query(F.data == "choose_schedule_group")
async def choose_schedule(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите группу:", reply_markup=group_choice_kb)

# 🗓 Вывод расписания по группе
@admin_router.callback_query(F.data.startswith("group_"))
async def send_schedule(callback: types.CallbackQuery):
    group_id = int(callback.data.split("_")[1])
    schedule = load_cached_schedule(group_id)
    await callback.message.edit_text(f"<b>📅 Расписание для группы {group_id}:</b>\n\n{schedule[:4000]}")

@admin_router.message(Command("get_id"))
async def get_admin_id(message: types.Message):
    await message.answer(str(message.from_user.id))
    admin_id = message.from_user.id