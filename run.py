import asyncio
import logging
from datetime import datetime

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from keyboard import main_menu_kb, group_choice_kb

from config import TOKEN
from lexicon import LEXICON
from timetable import load_cached_schedule
from scheduler import schedule_loop

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

# 🚀 Команда /start — главное меню
@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer("Привет! Чем могу помочь?", reply_markup=main_menu_kb)

# 📌 Кнопка "📅 Расписание" → выбор группы
@dp.callback_query(F.data == "choose_schedule_group")
async def choose_schedule(callback: types.CallbackQuery):
    await callback.message.edit_text("Выберите группу:", reply_markup=group_choice_kb)

# 🗓 Вывод расписания по группе
@dp.callback_query(F.data.startswith("group_"))
async def send_schedule(callback: types.CallbackQuery):
    group_id = int(callback.data.split("_")[1])
    schedule = load_cached_schedule(group_id)
    await callback.message.edit_text(f"<b>📅 Расписание для группы {group_id}:</b>\n\n{schedule[:4000]}")

# 🔁 Запуск бота
async def main():
    bot = Bot(TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    
    # ⏰ Запуск фоновой задачи с проверкой понедельника
    asyncio.create_task(schedule_loop())

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен!")
