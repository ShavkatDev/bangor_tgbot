from app.utils.inline import simple_keyboard
from app.config import get_button

@simple_keyboard
def mailing_settings_keyboard(
    daily_digest: bool, today_schedule_digest: bool, lang: str
):
    def status_text(enabled: bool) -> str:
        return "✅" if enabled else "❌"
    return [
        [
            f"{status_text(daily_digest)} {get_button('checkin_checkout_mailing', lang)}",
            "toggle_daily_digest"
        ],
        [
            f"{status_text(today_schedule_digest)} {get_button('schedule_today_mailing', lang)}",
            "toggle_today_schedule_digest"
        ],
        [
            get_button("back_to_settings", lang),
            "back_to_settings_menu"
        ]
    ]
