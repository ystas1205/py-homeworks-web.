from sqlalchemy import DateTime, String, create_engine, func
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker,
)

import atexit
import datetime
import os

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "app")
POSTGRES_DB = os.getenv("POSTGRES_DB", "app")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")

PG_DSN = (f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:"
          f"{POSTGRES_PORT}/{POSTGRES_DB}")

engine = create_engine(PG_DSN)
Session = sessionmaker(bind=engine)
atexit.register(engine.dispose)


class Base(DeclarativeBase):
    pass


class Announcement(Base):
    __tablename__ = "app_ads"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(300), nullable=False)
    date_of_creation: Mapped[datetime.datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
    user: Mapped[str] = mapped_column(String(100), unique=True, index=True,
                                      nullable=False)

    @property
    def dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date_of_creation": self.date_of_creation.isoformat(),
            "user": self.user,
        }


Base.metadata.create_all(bind=engine)
