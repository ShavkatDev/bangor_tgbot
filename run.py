import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import TOKEN
from lexicon import LEXICON
router = Router()

@router.message(F.content_type.in_({'new_chat_members'}))
async def salutations_process(message: types.Message, bot: Bot):
    salutate_message = await message.answer(LEXICON['/salutate'].format(str(message.from_user.first_name)))
    await bot.send_message(chat_id=7396564931, text=LEXICON["/new_member"].format(str(message.from_user.username), str(message.from_user.first_name), str(datetime.now()), str(message.from_user.id) ))

@router.message(F.content_type.in_({'left_chat_member'}))
async def left_member_process(message: types.Message, bot: Bot):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

async def main():
    token = TOKEN
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
