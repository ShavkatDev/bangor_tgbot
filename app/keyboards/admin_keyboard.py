from app.utils.inline import eager, simple_keyboard

@eager
@simple_keyboard
def admin_keyboard():
    return [
        [
            "📊 Статистика",
            "admin_stats"
        ],
        [
            "📬 Сделать рассылку",
            "admin_broadcast"
        ],
        [
            "📂 Логи",
            "admin_logs"
        ],
        [
            "🛠 Настройки",
            "admin_settings"
        ]
    ]
    
@eager
@simple_keyboard
def confirm_broadcast_keyboard():
    return [
        [
            "✅ Подтвердить",
            "confirm_broadcast"
        ],
        [
            "❌ Отменить",
            "cancel_broadcast"
        ]
    ]
