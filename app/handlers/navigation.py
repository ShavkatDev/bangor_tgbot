import logging
from aiogram import Router, types
from app.keyboards.navigation_keyboard import nav_keyboard
from app.lexicon.lexicon import LEXICON_MSG
from app.utils.text_from_lexicon import TextFromLexicon

logger = logging.getLogger(__name__)
navigation_router = Router()

@navigation_router.message(TextFromLexicon("navigation"))
async def send_navigation(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) ask for navigation")
    
    try:
        await message.answer(
            text=LEXICON_MSG["navigation_text"][lang],
            reply_markup=nav_keyboard()
        )
    except Exception as e:
        logger.error(f"Error opening navigation menu for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])
