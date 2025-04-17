from datetime import datetime
import logging
from sqlalchemy import select, update

from app.db.models import SupportRequest
from app.db.database import async_session_maker

async def save_ticket(user_id: int, question_message_id: int):
    async with async_session_maker() as session:
        ticket = SupportRequest(
            user_id=user_id,
            question_message_id=question_message_id,
            status="open"
        )
        session.add(ticket)
        await session.commit()
        logging.info(f"[Support] New ticket from user_id={user_id}, message_id={question_message_id}")

async def get_open_ticket_by_question_message_id(question_message_id: int):
    async with async_session_maker() as session:
        result = await session.execute(
            select(SupportRequest)
            .where(SupportRequest.question_message_id == question_message_id)
            .where(SupportRequest.status == "open")
        )
        logging.info(f"[Support] Fetched open ticket for message_id={question_message_id}")
        return result.scalars().first()

async def close_ticket(user_id: int, admin_id: int):
    async with async_session_maker() as session:
        await session.execute(
            update(SupportRequest)
            .where(SupportRequest.user_id == user_id)
            .where(SupportRequest.status == "open")
            .values(
                status="closed",
                admin_id=admin_id,
                closed_at=datetime.utcnow()
            )
        )
        logging.info(f"[Support] Ticket closed by admin_id={admin_id} for user_id={user_id}")
        await session.commit()
