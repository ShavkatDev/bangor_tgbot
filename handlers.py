from aiogram import Dispatcher, types, F, Router
from aiogram.filters import Command
from keyboard import main_menu_kb, group_choice_kb

from timetable import load_cached_schedule, update_schedule_for_group
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
    if schedule == "⚠️ Расписание ещё не загружено.":
        schedule = await callback.message.answer("Обновляем расписание...")
        await update_schedule_for_group(group_id)

    await schedule.edit_text(f"<b>📅 Расписание для группы {group_id}:</b>\n\n{schedule[:4000]}")
