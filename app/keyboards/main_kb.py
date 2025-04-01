from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Главное меню (/start)
main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📅 Расписание", callback_data="choose_schedule_group")]
    ]
)

# Клавиатура с выбором группы
group_choice_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Группа 231", callback_data="group_231")],
        [InlineKeyboardButton(text="Группа 232", callback_data="group_232")],
        [InlineKeyboardButton(text="Группа 233", callback_data="group_233")],
    ]
)
