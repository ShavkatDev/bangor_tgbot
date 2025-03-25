import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command

from config import TOKEN
from lexicon import LEXICON
from scheduler import schedule_loop, update_all_groups
from handlers import admin_router

dp = Dispatcher()

# 💬 Приветствие нового участника
@dp.message(F.content_type.in_({'new_chat_members'}))
async def salutations_process(message: types.Message, bot: Bot):
    for new_member in message.new_chat_members:
        if new_member.is_bot or new_member.id == message.bot.id:
            continue

        salutate_message = await message.answer(LEXICON['/salutate'].format(str(new_member.first_name)))
        await bot.send_message(
            chat_id=7396564931,
            text=LEXICON["/new_member"].format(
                str(new_member.username),
                str(new_member.first_name),
                str(datetime.now()),
                str(new_member.id)
            )
        )

# 🛑 Удаление сообщения, если участник вышел
@dp.message(F.content_type.in_({'left_chat_member'}))
async def left_member_process(message: types.Message, bot: Bot):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

@dp.message(Command("get_id"))
async def get_admin_id(message: types.Message):
    await message.answer(str(message.from_user.id))
    print(str(message.from_user.id))

# 🔁 Запуск бота
async def main():
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_router(admin_router)
    
    asyncio.create_task(schedule_loop())

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
