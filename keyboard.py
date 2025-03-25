from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню (/start)
main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📅 Расписание универа", callback_data="choose_schedule_group")],
        [InlineKeyboardButton(text="🌤️ Погода на сегодня", callback_data="weather_today")],
        [InlineKeyboardButton(text="🗺️ Карта универа", callback_data="university_map")],
        [InlineKeyboardButton(text="📚 Blackboard", callback_data="blackboard")],
        [InlineKeyboardButton(text="📰 Новости универа", callback_data="university_news")],
        [InlineKeyboardButton(text="⏰ Уведомления о дедлайнах", callback_data="deadlines_notifications")],  # Новая кнопка
    ]
)

# Клавиатура с выбором группы
group_choice_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Группа 231", callback_data="group_231")],
        [InlineKeyboardButton(text="Группа 232", callback_data="group_232")],
        [InlineKeyboardButton(text="Группа 233", callback_data="group_233")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")],
    ]
)

# Клавиатура с кнопкой "Назад"
back_to_main_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
    ]
)