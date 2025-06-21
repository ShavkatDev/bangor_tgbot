import logging
from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import FSInputFile

from app.db.crud.user import get_all_users
from app.db.crud.stats import (
    get_total_users,
    get_new_users,
    get_users_with_today_digest,
    get_users_with_daily_digest,
    get_users_by_language,
)
from app.keyboards.admin_keyboard import admin_keyboard, confirm_broadcast_keyboard

logger = logging.getLogger(__name__)
admin_router = Router()


class BroadcastState(StatesGroup):
    waiting_for_message = State()
    waiting_for_confirmation = State()


@admin_router.message(F.text == "👨🏻‍💻 Админ-панель")
async def admin_panel(message: types.Message, is_admin: bool):
    if not is_admin:
        return
    telegram_id = message.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} opened admin panel")

    await message.answer("Добро пожаловать в админ-панель", reply_markup=admin_keyboard)


@admin_router.callback_query(F.data == "admin_broadcast")
async def ask_for_broadcast_text(
    callback: types.CallbackQuery, state: FSMContext, is_admin: bool
):
    if not is_admin:
        return
    await callback.answer()
    telegram_id = callback.message.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} initiated a broadcast")

    await callback.message.answer(
        "Отправьте сообщение, которое хотите разослать всем пользователям."
    )
    await state.set_state(BroadcastState.waiting_for_message)


@admin_router.callback_query(F.data == "admin_stats")
async def ask_for_stats(callback: types.CallbackQuery, is_admin: bool):
    if not is_admin:
        return
    await callback.answer()

    telegram_id = callback.message.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} initiated a stats request")

    try:
        total_users = await get_total_users()
        new_users_7d = await get_new_users(7)
        new_users_1d = await get_new_users(1)
        with_today_digest = await get_users_with_today_digest()
        with_daily_digest = await get_users_with_daily_digest()
        lang_distribution = await get_users_by_language()

        lang_text = "\n".join(
            [f"• {lang.upper()}: {count}" for lang, count in lang_distribution.items()]
        )

        text = (
            "<b>📊 Статистика</b>\n\n"
            f"👥 Всего пользователей: <b>{total_users}</b>\n"
            f"🆕 Новых за 7 дней: <b>{new_users_7d}</b>\n"
            f"🆕 Новых за 24ч: <b>{new_users_1d}</b>\n\n"
            f"📬 С включённой ежедневной рассылкой: <b>{with_daily_digest}</b>\n"
            f"📅 С включённой рассылкой расписания: <b>{with_today_digest}</b>\n\n"
            f"🌐 Языки интерфейса:\n{lang_text}"
        )

        await callback.message.answer(text)

    except Exception as e:
        logger.error(
            f"[Admin] Failed to fetch stats for admin {telegram_id}: {str(e)}",
            exc_info=True,
        )
        await callback.message.answer("⚠️ Ошибка при получении статистики.")


@admin_router.callback_query(F.data == "admin_logs")
async def ask_for_logs(callback: types.CallbackQuery, is_admin: bool):
    if not is_admin:
        return

    telegram_id = callback.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} requested log file")

    try:
        input_file = FSInputFile("logs/bot.log")
        await callback.message.answer_document(
            document=input_file, caption="📂 Лог-файл"
        )
    except FileNotFoundError:
        logger.warning(f"[Admin] Log file not found for admin {telegram_id}")
        await callback.message.answer("⚠️ Лог-файл не найден.")
    except Exception as e:
        logger.error(
            f"[Admin] Failed to send log file to admin {telegram_id}: {str(e)}",
            exc_info=True,
        )
        await callback.message.answer("❌ Ошибка при отправке логов.")

    await callback.answer()


@admin_router.callback_query(F.data == "admin_settings")
async def ask_for_stats(callback: types.CallbackQuery, is_admin: bool):
    if not is_admin:
        return
    await callback.answer("В разработке...")


@admin_router.message(BroadcastState.waiting_for_message)
async def ask_to_confirm_broadcast(
    message: types.Message, state: FSMContext, is_admin: bool
):
    if not is_admin:
        return

    telegram_id = message.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} submitted a message for preview")

    await state.update_data(message_id=message.message_id, text=message.html_text)

    await message.answer("Here’s how the broadcast will look:")

    try:
        if message.photo:
            await message.bot.send_photo(
                chat_id=message.chat.id,
                photo=message.photo[-1].file_id,
                caption=message.caption or "",
                parse_mode="HTML",
            )
        elif message.text:
            await message.bot.send_message(
                chat_id=message.chat.id, text=message.html_text, parse_mode="HTML"
            )
        else:
            await message.answer("⚠️ This message type is not supported for preview.")
    except Exception as e:
        logger.error(
            f"[Admin] Error sending preview to admin {telegram_id}: {str(e)}",
            exc_info=True,
        )

    await message.answer(
        "Are you sure you want to send this message to all users?",
        reply_markup=confirm_broadcast_keyboard,
    )

    await state.set_state(BroadcastState.waiting_for_confirmation)


@admin_router.callback_query(F.data == "confirm_broadcast")
async def confirm_broadcast(
    callback: types.CallbackQuery, state: FSMContext, is_admin: bool
):
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
                chat_id=user, text=broadcast_text, parse_mode="HTML"
            )
            success += 1
        except Exception as ex:
            failed += 1
            logger.warning(f"[Admin] Failed to send message to {user}: {str(ex)}")

    logger.info(
        f"[Admin] Broadcast finished by admin {telegram_id}: {success} sent, {failed} failed"
    )

    await callback.message.answer(
        f"Рассылка завершена.\n✅ Отправлено: {success}\n❌ Ошибок: {failed}"
    )
    await state.clear()
    await callback.answer()


@admin_router.callback_query(F.data == "cancel_broadcast")
async def cancel_broadcast(
    callback: types.CallbackQuery, state: FSMContext, is_admin: bool
):
    if not is_admin:
        return

    telegram_id = callback.from_user.id
    logger.info(f"[Admin] Admin {telegram_id} cancelled broadcast")

    await callback.message.edit_text("Рассылка отменена.")
    await state.clear()
    await callback.answer()
