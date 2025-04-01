from aiogram import types, Router, F
from datetime import datetime
from aiogram import Bot
from app.lexicon.lexicon_en import LEXICON

chat_router = Router()

@chat_router.message(F.content_type.in_({'new_chat_members'}))
async def salutations_process(message: types.Message, bot: Bot):
    for new_member in message.new_chat_members:
        if new_member.is_bot or new_member.id == message.bot.id:
            continue
        await message.answer(LEXICON['/salutate'].format(str(new_member.first_name)))
        await bot.send_message(
            chat_id=7396564931,
            text=LEXICON["/new_member"].format(
                str(new_member.username),
                str(new_member.first_name),
                str(datetime.now()),
                str(new_member.id)
            )
        )

@chat_router.message(F.content_type.in_({'left_chat_member'}))
async def left_member_process(message: types.Message, bot: Bot):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
