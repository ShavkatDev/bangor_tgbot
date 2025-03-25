from aiogram import Router, types, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboard import main_menu_kb, group_choice_kb, back_to_main_kb
from timetable import load_cached_schedule, update_schedule_for_group
from weather import get_weather
from deadlines_storage import add_deadline, get_user_deadlines, remove_deadline
import asyncio
from datetime import datetime, timedelta

main_router = Router()

# Состояния для FSM (Finite State Machine)
class DeadlineStates(StatesGroup):
    waiting_for_deadline = State()

# Команда /start — показывает главное меню
@main_router.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Чем могу помочь?", reply_markup=main_menu_kb)

# Кнопка "📅 Расписание универа" → выбор группы
@main_router.callback_query(F.data == "choose_schedule_group")
async def choose_schedule(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите группу:", reply_markup=group_choice_kb)

# Вывод расписания для выбранной группы
@main_router.callback_query(F.data.startswith("group_"))
async def send_schedule(callback: types.CallbackQuery):
    group_id = int(callback.data.split("_")[1])
    
    # Проверяем, является ли группа 232
    if group_id == 232:
        schedule = load_cached_schedule(group_id)
        if schedule == "⚠️ Расписание ещё не загружено.":
            await callback.message.edit_text("Обновляем расписание...", reply_markup=back_to_main_kb)
            update_schedule_for_group(group_id)
            schedule = load_cached_schedule(group_id)
        await callback.message.edit_text(
            f"<b>📅 Расписание для группы {group_id}:</b>\n\n{schedule[:4000]}",
            reply_markup=back_to_main_kb
        )
    else:
        await callback.message.edit_text(
            "⚠️ Эта функция временно недоступна для данной группы.",
            reply_markup=back_to_main_kb
        )

# Кнопка "🌤️ Погода на сегодня"
@main_router.callback_query(F.data == "weather_today")
async def weather_today(callback: types.CallbackQuery):
    temp, description, city = get_weather(city="Tashkent")
    
    if temp is None:
        await callback.message.edit_text(description, reply_markup=back_to_main_kb)
        return
    
    # Базовое сообщение с погодой
    weather_message = f"🌤️ <b>Погода в {city}:</b>\nТемпература: {temp}°C\nОписание: {description}\n\n"
    
    # Шуточные комментарии в зависимости от погоды
    if "солнечно" in description.lower():
        weather_message += "Сегодня солнечно, поэтому надеваем шлёпки и берём крем от загара! ☀️"
    elif "дождь" in description.lower() or "дождливо" in description.lower():
        weather_message += "Ждём дождик, берём зонтик! ☔"
    elif "облачно" in description.lower():
        weather_message += "Облачно, но не унываем — идеальная погода для учёбы! ☁️"
    elif "снег" in description.lower():
        weather_message += "Снежок идёт! Лепим снеговика и пьём горячий чай! ❄️"
    elif "туман" in description.lower():
        weather_message += "Туман на улице, как в фильме ужасов! Идём осторожно! 🌫️"
    else:
        weather_message += "Погода какая-то странная, но мы справимся! 😄"
    
    await callback.message.edit_text(
        weather_message,
        reply_markup=back_to_main_kb,
        parse_mode="HTML"
    )

# Кнопка "🗺️ Карта универа"
@main_router.callback_query(F.data == "university_map")
async def university_map(callback: types.CallbackQuery):
    map_url = "https://www.google.com/maps/place/41.2694196305786,69.20319149945648"
    map_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🗺️ Открыть карту", url=map_url)],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]
    )
    await callback.message.edit_text(
        "📍 Карта кампуса MDIS Tashkent:",
        reply_markup=map_kb
    )

# Кнопка "📚 Blackboard"
@main_router.callback_query(F.data == "blackboard")
async def blackboard(callback: types.CallbackQuery):
    blackboard_url = "https://inet.mdis.uz"
    blackboard_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📚 Открыть Blackboard", url=blackboard_url)],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]
    )
    await callback.message.edit_text(
        "📚 Доступ к Blackboard MDIS Tashkent:",
        reply_markup=blackboard_kb
    )

# Кнопка "📰 Новости универа"
@main_router.callback_query(F.data == "university_news")
async def university_news(callback: types.CallbackQuery):
    news_url = "https://mdis.uz/news"
    news_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📰 Читать новости", url=news_url)],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]
    )
    await callback.message.edit_text(
        "📰 Последние новости MDIS Tashkent доступны на сайте:",
        reply_markup=news_kb
    )

# Кнопка "⏰ Уведомления о дедлайнах"
@main_router.callback_query(F.data == "deadlines_notifications")
async def deadlines_notifications(callback: types.CallbackQuery, state: FSMContext):
    deadlines = get_user_deadlines(callback.from_user.id)
    if not deadlines:
        await callback.message.edit_text(
            "⏰ У вас пока нет сохранённых дедлайнов.\n"
            "Хотите добавить новый дедлайн?",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Добавить дедлайн", callback_data="add_deadline")],
                    [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
                ]
            )
        )
    else:
        # Показываем список дедлайнов
        deadlines_text = "⏰ <b>Ваши дедлайны:</b>\n\n"
        for idx, deadline in enumerate(deadlines):
            deadlines_text += f"{idx + 1}. {deadline['name']} — {deadline['datetime']}\n"
        await callback.message.edit_text(
            deadlines_text + "\nВыберите действие:",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="➕ Добавить дедлайн", callback_data="add_deadline")],
                    [InlineKeyboardButton(text="🗑️ Удалить дедлайн", callback_data="remove_deadline")],
                    [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
                ]
            ),
            parse_mode="HTML"
        )

# Кнопка "➕ Добавить дедлайн"
@main_router.callback_query(F.data == "add_deadline")
async def add_deadline_start(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Введите дедлайн в формате: Название, Дата, Время\n"
        "Пример: Сдать проект по Python, 2025-04-01, 15:00",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="deadlines_notifications")]
            ]
        )
    )
    await state.set_state(DeadlineStates.waiting_for_deadline)

# Кнопка "🔄 Ввести ещё раз"
@main_router.callback_query(F.data == "retry_deadline")
async def retry_deadline(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Введите дедлайн в формате: Название, Дата, Время\n"
        "Пример: Сдать проект по Python, 2025-04-01, 15:00",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="deadlines_notifications")]
            ]
        )
    )
    await state.set_state(DeadlineStates.waiting_for_deadline)

# Обработчик ввода дедлайна
@main_router.message(StateFilter(DeadlineStates.waiting_for_deadline))
async def process_deadline_input(message: types.Message, state: FSMContext):
    try:
        # Разделяем ввод на части: название, дата, время
        parts = message.text.split(",")
        if len(parts) != 3:
            raise ValueError("Неверный формат. Используйте: Название, Дата, Время")
        
        name = parts[0].strip()
        date_str = parts[1].strip()
        time_str = parts[2].strip()
        
        # Парсим дату и время
        deadline_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        
        # Проверяем, что дедлайн в будущем
        if deadline_datetime <= datetime.now():
            raise ValueError("Дедлайн должен быть в будущем!")
        
        # Сохраняем дедлайн
        add_deadline(message.from_user.id, name, deadline_datetime)
        
        await message.answer(
            f"✅ Дедлайн '{name}' на {deadline_datetime.strftime('%Y-%m-%d %H:%M')} успешно добавлен!\n"
            "Я напомню вам за день до дедлайна.",
            reply_markup=back_to_main_kb
        )
    except ValueError as e:
        await message.answer(
            f"⚠️ Ошибка: {str(e)}\n"
            "Попробуйте снова. Формат: Название, Дата, Время (например, Сдать проект по Python, 2025-04-01, 15:00)",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(text="🔄 Ввести ещё раз", callback_data="retry_deadline")],
                    [InlineKeyboardButton(text="⬅️ Назад", callback_data="deadlines_notifications")]
                ]
            )
        )
    finally:
        await state.clear()

# Кнопка "🗑️ Удалить дедлайн"
@main_router.callback_query(F.data == "remove_deadline")
async def remove_deadline_start(callback: types.CallbackQuery):
    deadlines = get_user_deadlines(callback.from_user.id)
    if not deadlines:
        await callback.message.edit_text(
            "⏰ У вас нет дедлайнов для удаления.",
            reply_markup=back_to_main_kb
        )
        return
    
    # Создаём кнопки для удаления
    buttons = []
    for idx, deadline in enumerate(deadlines):
        buttons.append([InlineKeyboardButton(
            text=f"Удалить: {deadline['name']} ({deadline['datetime']})",
            callback_data=f"delete_deadline_{idx}"
        )])
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="deadlines_notifications")])
    
    await callback.message.edit_text(
        "⏰ Выберите дедлайн для удаления:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons)
    )

# Обработчик удаления дедлайна
@main_router.callback_query(F.data.startswith("delete_deadline_"))
async def process_remove_deadline(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[2])
    remove_deadline(callback.from_user.id, index)
    await callback.message.edit_text(
        "✅ Дедлайн успешно удалён!",
        reply_markup=back_to_main_kb
    )

# Обработчик для кнопки "⬅️ Назад"
@main_router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: types.CallbackQuery):
    await callback.message.edit_text("Привет! Чем могу помочь?", reply_markup=main_menu_kb)