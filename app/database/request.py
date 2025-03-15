from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.dialects.postgresql import insert

from app.database.models import async_session
from app.database.models import User, Context, ChatModel

"""
This module contains functions to interact with the database.
"""

async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def add_history(tg_id: int, role: str, message_text: str) -> None:
    async with async_session() as session:
        new_record = Context(
            user_id=tg_id, role=role, content=message_text, timestamp=datetime.utcnow()
        )
        session.add(new_record)
        await session.commit()


async def get_history(tg_id: int) -> None:
    async with async_session() as session:
        result = await session.scalars(
            select(Context).where(Context.user_id == tg_id).order_by(Context.timestamp)
        )
        history = result.all()
        return history


async def update_state(tg_id: int, state: str) -> None:
    async with async_session() as session:
        await session.execute(
            update(ChatModel).where(ChatModel.user_id == tg_id).values(model=state)
        )
        await session.commit()


async def update_system(tg_id: int, system: str) -> None:
    async with async_session() as session:
        await session.execute(
            update(ChatModel)
            .where(ChatModel.user_id == tg_id)
            .values(system_msg=system)
        )
        await session.commit()


async def get_state(tg_id: int):
    async with async_session() as session:
        result = await session.scalars(
            select(ChatModel).where(ChatModel.user_id == tg_id)
        )
        row = result.first()
        return (row.model, row.system_msg) if row else None


async def default_chat_model(tg_id: int) -> None:
    async with async_session() as session:
        stmt = insert(ChatModel).values(
            user_id=tg_id, model="deepseek", system_msg="default"
        )
        stmt = stmt.on_conflict_do_nothing(index_elements=["user_id"])
        await session.execute(stmt)
        await session.commit()
