from app.database.models import async_session
from app.database.models import User, Context, Model
from sqlalchemy import select
from datetime import datetime

from sqlalchemy.dialects.postgresql import insert


async def set_user(tg_id: int) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id = tg_id))
            await session.commit()

async def add_history(tg_id: int, role: str, message_text: str) -> None:
    async with async_session() as session:
        new_record = Context(
            user_id = tg_id,
            role = role,
            content = message_text,
            timestamp = datetime.utcnow()
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

async def upate_state(tg_id: int, state: str) -> None:
    async with async_session() as session:
        stmt = insert(Model).values(user_id=tg_id, model=state)
        stmt = stmt.on_conflict_do_update(index_elements=['user_id'], set_={'model': state})
        await session.execute(stmt)
        await session.commit()

async def get_state(tg_id: int) -> None:
    async with async_session() as session:
        result = await session.scalar(
            select(Model.model).where(Model.user_id == tg_id)
        )
        return result