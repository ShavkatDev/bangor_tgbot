import logging
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from app.db.crud.user import get_all_users
from app.lexicon.lexicon import LEXICON_MSG
from app.keyboards.admin_keyboard import admin_keyboard, confirm_broadcast_keyboard

logger = logging.getLogger(__name__)
admin_router = Router()


class BroadcastState(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirmation = State()


@admin_router.message(F.text == "Админ-панель")
async def admin_panel(message: types.Message, is_admin: bool):
    if not is_admin:
        return
    telegram_id = message.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} opened admin panel")
    
    await message.answer("Добро пожаловать в админ-панель", reply_markup=admin_keyboard)


@admin_router.message(F.text == "Сделать рассылку")
async def ask_for_broadcast_text(message: types.Message, state: FSMContext, is_admin: bool):
    if not is_admin:
        return
    telegram_id = message.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} initiated a broadcast")

    await message.answer("Отправьте сообщение, которое хотите разослать всем пользователям.")
    await state.set_state(BroadcastState.waiting_for_message)


@admin_router.message(BroadcastState.waiting_for_message)
async def ask_to_confirm_broadcast(message: types.Message, state: FSMContext, is_admin: bool):
    if not is_admin:
        return

    telegram_id = message.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} submitted a message for preview")

    await state.update_data(
        message_id=message.message_id,
        text=message.html_text
    )

    await message.answer("Here’s how the broadcast will look:")

    try:
        if message.photo:
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=message.photo[-1].file_id,
                caption=message.caption or "",
                parse_mode="HTML"
            )
        elif message.text:
            await message.bot.send_message(
                chat_id=message.chat.id,
                text=message.html_text,
                parse_mode="HTML"
            )
        else:
            await message.answer("⚠️ This message type is not supported for preview.")
    except Exception as e:
        logger.error(f"[Admin] Error sending preview to admin {telegram_id}: {str(e)}", exc_info=True)

    await message.answer(
        "Are you sure you want to send this message to all users?",
        reply_markup=confirm_broadcast_keyboard
    )

    await state.set_state(BroadcastState.waiting_for_confirmation)


@admin_router.callback_query(F.data == "confirm_broadcast")
async def confirm_broadcast(callback: types.CallbackQuery, state: FSMContext, is_admin: bool):
    if not is_admin:
        return

    data = await state.get_data()
    message_id = data.get("message_id")
    broadcast_text = data.get("text")

    telegram_id = callback.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} confirmed broadcast")

    await callback.message.edit_text("Рассылка начата...")

    users = await get_all_users()
    success, failed = 0, 0

    for user in users:
        try:
            await callback.bot.send_message(
                chat_id=user,
                text=broadcast_text,
                parse_mode="HTML"
            )
            success += 1
        except Exception as ex:
            failed += 1
            logger.warning(f"[Admin] Failed to send message to {user}: {str(ex)}")

    logger.info(f"[Admin] Broadcast finished by admin {telegram_id}: {success} sent, {failed} failed")

    await callback.message.answer(
        f"Рассылка завершена.\n✅ Отправлено: {success}\n❌ Ошибок: {failed}"
    )
    await state.clear()
    await callback.answer()


@admin_router.callback_query(F.data == "cancel_broadcast")
async def cancel_broadcast(callback: types.CallbackQuery, state: FSMContext, is_admin: bool):
    if not is_admin:
        return

    telegram_id = callback.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} cancelled broadcast")

    await callback.message.edit_text("Рассылка отменена.")
    await state.clear()
    await callback.answer()
