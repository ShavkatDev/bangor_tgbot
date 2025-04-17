from app.lexicon.lexicon import LEXICON_MSG


def get_privacy_keyboard(lang: str = "en") -> dict:
    return {
        "inline_keyboard": [
            [
                {"text": LEXICON_MSG["view_privacy_policy"][lang], "url": "https://telegra.ph/PRIVACY-POLICY-04-17-70"},
                {"text": LEXICON_MSG["view_terms"][lang], "url": "https://telegra.ph/TERMS-of-SERVICE-04-17-5"}
            ],
            [
                {"text": LEXICON_MSG["privacy_policy_accept"][lang], "callback_data": "accept_privacy"},
                {"text": LEXICON_MSG["privacy_policy_decline"][lang], "callback_data": "decline_privacy"}
            ]
        ]
    } 