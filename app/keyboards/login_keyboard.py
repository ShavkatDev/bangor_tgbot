from app.utils.inline import eager, simple_keyboard

@eager
@simple_keyboard
def inline_login():
    return [
        ["Login", "start_login"]
    ]
