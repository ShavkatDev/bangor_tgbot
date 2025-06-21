from app.utils.inline import simple_keyboard

from app.config import get_button


@simple_keyboard
def delete_keyboard(lang: str):
    return [
        [str(get_button("delete_approve", lang)), "delete_approve"],
        [str(get_button("delete_decline", lang)), "delete_decline"],
    ]
