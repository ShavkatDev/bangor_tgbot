from app.utils.inline import simple_keyboard, eager


@eager
@simple_keyboard
def language_keyboard():
    return [
        ["🇷🇺 Русский", "set_lang_ru"],
        ["🇺🇿 O'zbekcha", "set_lang_uz"],
        ["🇬🇧 English", "set_lang_en"]
    ]
