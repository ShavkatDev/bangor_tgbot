from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📅 INET (Расписание)", callback_data="inet_menu")],
        [InlineKeyboardButton(text="⚙️ Настройки", callback_data="settings_menu")],
        [InlineKeyboardButton(text="📞 Поддержка", callback_data="support_menu")]
    ]
)

# Клавиатура для "INET (Расписание)"
inet_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📆 Расписание", callback_data="schedule")],
        [InlineKeyboardButton(text="🔔 Уведомления", callback_data="notifications")],
        [InlineKeyboardButton(text="📅 Рассылка на завтра", callback_data="schedule_tomorrow")],
        [InlineKeyboardButton(text="📅 Рассылка на неделю", callback_data="schedule_week")],
        [InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_to_main")]
    ]
)

# Клавиатура для "Расписание"
schedule_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📅 Расписание на завтра", callback_data="schedule_tomorrow_view")],
        [InlineKeyboardButton(text="📅 Расписание на неделю", callback_data="schedule_week_view")],
        [InlineKeyboardButton(text="🔙 Назад в INET", callback_data="inet_menu")]
    ]
)

# Клавиатура для "Уведомления"
notifications_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Включить уведомления", callback_data="enable_notifications")],
        [InlineKeyboardButton(text="🔔 Отключить уведомления", callback_data="disable_notifications")],
        [InlineKeyboardButton(text="🔙 Назад в INET", callback_data="inet_menu")]
    ]
)

# Клавиатура для "Настройки"
settings_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📬 Рассылки", callback_data="mailing_settings")],
        [InlineKeyboardButton(text="🌐 Язык", callback_data="language_settings")],
        [InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_to_main")]
    ]
)

# Клавиатура для "Рассылки" (в настройках)
mailing_settings_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📅 Рассылка на завтра", callback_data="mailing_tomorrow")],
        [InlineKeyboardButton(text="📅 Рассылка на неделю", callback_data="mailing_week")],
        [InlineKeyboardButton(text="🔙 Назад в настройки", callback_data="settings_menu")]
    ]
)

# Клавиатура для "Язык" (в настройках)
language_settings_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="lang_english")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="lang_russian")],
        [InlineKeyboardButton(text="🇺🇿 Oʻzbek", callback_data="lang_uzbek")],
        [InlineKeyboardButton(text="🔙 Назад в настройки", callback_data="settings_menu")]
    ]
)


# Клавиатура для "Поддержка"
support_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="📞 Написать в поддержку", callback_data="contact_support")],
        [InlineKeyboardButton(text="🔙 Назад в главное меню", callback_data="back_to_main")]
    ]
)