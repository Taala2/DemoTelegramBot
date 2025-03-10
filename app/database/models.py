import os
from datetime import datetime
from sqlalchemy import BigInteger, String, ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(url=os.getenv('SQLALCHEMY'))

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    tg_id = mapped_column(BigInteger, primary_key=True)

    context = relationship("Context", back_populates="user", cascade="all, delete")
    model = relationship('ChatModel', back_populates='user', cascade='all, delete')

class Context(Base):
    __tablename__ = 'context'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger, ForeignKey('users.tg_id'))
    role: Mapped[str] = mapped_column(String, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow())

    user = relationship("User", back_populates="context")

class ChatModel(Base):
    __tablename__ = 'models'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger, ForeignKey('users.tg_id'), unique = True)
    model: Mapped[str] = mapped_column(String, nullable=False)
    system_msg: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship('User', back_populates='model')



async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)