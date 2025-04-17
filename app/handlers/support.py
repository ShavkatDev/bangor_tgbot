import logging
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext

from app.config import settings
from app.db.crud.support import get_open_ticket_by_question_message_id, save_ticket, close_ticket
from app.lexicon.lexicon import LEXICON_MSG
from app.keyboards.reply import main_menu_keyboard
from app.states import SupportState
from app.utils.text_from_lexicon import TextFromLexicon

logger = logging.getLogger(__name__)
support_router = Router()

@support_router.message(TextFromLexicon('support'))
async def support_command(message: types.Message, lang: str, state: FSMContext):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    logger.info(f"User {telegram_id} (@{username}) started support conversation")
    
    try:
        await message.answer(LEXICON_MSG["support_start"][lang], reply_markup=types.ReplyKeyboardRemove())
        await state.set_state(SupportState.waiting_for_question)
    except Exception as e:
        logger.error(f"Error starting support conversation for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])

@support_router.message(SupportState.waiting_for_question, F.content_type.in_({"text", "photo"}))
async def handle_question(message: types.Message, lang: str, state: FSMContext):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    content_type = "text" if message.text else "photo"
    logger.info(f"User {telegram_id} (@{username}) sent {content_type} support question")
    
    try:
        await state.clear()
        user_id = message.from_user.id

        for admin_id in settings.ADMINS:
            if message.text:
                sent = await message.bot.send_message(
                    admin_id,
                    LEXICON_MSG["support_user_question"][lang].format(
                        full_name=message.from_user.full_name,
                        user_id=message.from_user.id,
                        text=message.text
                    )
                )
            else:
                sent = await message.bot.send_photo(
                    admin_id,
                    message.photo[-1].file_id,
                    caption=LEXICON_MSG["support_user_question"][lang].format(
                        full_name=message.from_user.full_name,
                        user_id=message.from_user.id,
                        text=message.caption
                    )
                )

            if admin_id == settings.ADMINS[0]:
                await save_ticket(user_id=user_id, question_message_id=sent.message_id)
                logger.info(f"Support ticket created for user {telegram_id} (@{username})")

        await message.answer(LEXICON_MSG["support_sent"][lang], reply_markup=main_menu_keyboard(lang))
    except Exception as e:
        logger.error(f"Error processing support question from user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])

@support_router.message(SupportState.waiting_for_question)
async def unsupported_type(message: types.Message, lang: str):
    telegram_id = message.from_user.id
    username = message.from_user.username or "No username"
    content_type = message.content_type
    logger.warning(f"User {telegram_id} (@{username}) sent unsupported content type: {content_type}")
    
    try:
        await message.answer(LEXICON_MSG["support_unsupported_type"][lang])
    except Exception as e:
        logger.error(f"Error handling unsupported content type for user {telegram_id}: {str(e)}", exc_info=True)
        await message.answer(text=LEXICON_MSG['error'][lang])
    
@support_router.message(F.reply_to_message, F.from_user.id.in_(settings.ADMINS))
async def admin_reply(message: types.Message, lang: str):
    admin_id = message.from_user.id
    admin_username = message.from_user.username or "No username"
    replied = message.reply_to_message
    question_message_id = replied.message_id
    content_type = "text" if message.text else "photo" if message.photo else "other"
    
    try:
        logger.info(f"Admin {admin_id} (@{admin_username}) replied to support ticket with {content_type}")
        
        ticket = await get_open_ticket_by_question_message_id(question_message_id)
        if not ticket or ticket.status == "closed":
            logger.warning(f"Admin {admin_id} tried to reply to closed/non-existent ticket")
            await message.answer(LEXICON_MSG["support_admin_closed"][lang])
            return

        user_id = ticket.user_id

        if message.text:
            await message.bot.send_message(
                user_id,
                LEXICON_MSG["support_admin_reply"][lang].format(
                    text=message.text
                )
            )
        elif message.photo:
            await message.bot.send_photo(
                user_id,
                message.photo[-1].file_id,
                caption=LEXICON_MSG["support_admin_reply_caption"][lang]
            )
        else:
            logger.warning(f"Admin {admin_id} sent unsupported content type: {content_type}")
            await message.answer(LEXICON_MSG["support_admin_invalid_type"][lang])
            return

        await close_ticket(user_id, admin_id)
        logger.info(f"Admin {admin_id} closed support ticket for user {user_id}")
        await message.answer(LEXICON_MSG["support_admin_confirm"][lang])

    except Exception as e:
        logger.error(f"Error processing admin reply from {admin_id}: {str(e)}", exc_info=True)
        await message.answer(LEXICON_MSG["support_admin_send_error"][lang])
