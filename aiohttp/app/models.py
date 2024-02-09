from sqlalchemy import DateTime, String, func, ForeignKey, UUID
from sqlalchemy.ext.asyncio import (AsyncAttrs, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

import datetime
import uuid
from config import PG_DSN

engine = create_async_engine(PG_DSN)  # пул для подключения к базе
Session = async_sessionmaker(engine, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class Token(Base):
    __tablename__ = "token"
    id: Mapped[int] = mapped_column(primary_key=True)
    token: Mapped[uuid.UUID] = mapped_column(
        UUID, server_default=func.gen_random_uuid(), unique=True
    )
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    email: Mapped[str] = mapped_column(String(80), unique=True,
                                       nullable=False)
    user: Mapped[str] = mapped_column(String(100), index=True,
                                      nullable=False)

    @property
    def dict(self):
        return {

            "id": self.id,
            "token": str(self.token),
            "password": self.password,
            "email": self.email,
            "user": self.user

        }


class Announcement(Base):
    __tablename__ = "app_ads"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now())
    user_id: Mapped[int] = mapped_column(
        ForeignKey("token.id", ondelete="CASCADE"))
    user: Mapped[Token] = relationship(Token, lazy="joined")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "registration_time": int(self.date_of_creation.timestamp()),
            "user_id": self.user_id,

        }


async def init_orm():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
