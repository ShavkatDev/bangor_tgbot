import logging
from aiogram import types, Router, F
from aiogram import Bot
from app.lexicon.lexicon import LEXICON_EVENTS

logger = logging.getLogger(__name__)
chat_router = Router()


@chat_router.message(F.content_type.in_({"new_chat_members"}))
async def salutations_process(message: types.Message, bot: Bot):
    try:
        for new_member in message.new_chat_members:
            if new_member.is_bot or new_member.id == message.bot.id:
                continue
            logger.info(
                f"New member joined: {new_member.first_name} (@{new_member.username or 'No username'}, id={new_member.id}) in chat_id={message.chat.id}"
            )
            await message.answer(
                LEXICON_EVENTS["salutate"]["en"].format(str(new_member.first_name))
            )
    except Exception as e:
        logger.error(
            f"Error processing new chat member in chat_id={message.chat.id}: {str(e)}",
            exc_info=True,
        )


@chat_router.message(F.content_type.in_({"left_chat_member"}))
async def left_member_process(message: types.Message, bot: Bot):
    try:
        logger.info(
            f"Member left chat_id={message.chat.id}, user_id={message.left_chat_member.id}, username={message.left_chat_member.username or 'No username'}"
        )
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    except Exception as e:
        logger.error(
            f"Error processing left chat member in chat_id={message.chat.id}: {str(e)}",
            exc_info=True,
        )
