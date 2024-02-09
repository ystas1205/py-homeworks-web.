from sqlalchemy import DateTime, String, create_engine, func, UUID, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, \
    sessionmaker,relationship

import datetime
import os
import uuid
import atexit

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "ystas")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5430")

PG_DSN = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
          f"{POSTGRES_PORT}/{POSTGRES_DB}")
# PG_DSN = "postgresql://postgres:8490866@localhost:5432/flask"
engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)
atexit.register(engine.dispose)


class Base(DeclarativeBase):
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
            "token": self.token,
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
    # user_id: Mapped[int] = mapped_column(ForeignKey("token.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("token.id", ondelete="CASCADE"))
    user: Mapped[Token] = relationship(Token,lazy="joined")

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_of_creation": self.date_of_creation.isoformat(),
            "user_id": self.user_id,

        }

# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
