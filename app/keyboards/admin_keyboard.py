from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

admin_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📊 Статистика", callback_data="admin_stats")],
    [InlineKeyboardButton(text="📬 Сделать рассылку", callback_data="admin_broadcast")],
    [InlineKeyboardButton(text="📂 Логи", callback_data="admin_logs")],
    [InlineKeyboardButton(text="🛠 Настройки", callback_data="admin_settings")],
])

confirm_broadcast_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_broadcast")],
    [InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_broadcast")]
])