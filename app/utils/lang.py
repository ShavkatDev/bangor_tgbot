from app.lexicon.lexicon import LEXICON_BUTTONS


def get_text(key: str, lang: str = "en") -> str:
    return LEXICON_BUTTONS.get(key, {}).get(lang, f"⚠️ [{key}]")
