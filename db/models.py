from datetime import datetime
from enum import Enum as StrEnum  # to avoid conflict with Python versions

from sqlalchemy import (
    Column,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship


BaseModel = declarative_base()


class Status(str, StrEnum):
    in_progress = "in_progress"
    learned = "learned"

    def __str__(self):
        return self.value


class Users(BaseModel):
    __tablename__ = "users"

    telegram_id = Column(Integer(), primary_key=True)

    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(
        DateTime(), default=datetime.now, onupdate=datetime.now
    )

    cards = relationship("Cards", back_populates="user")


class Cards(BaseModel):
    __tablename__ = "cards"

    id = Column(Integer(), primary_key=True)
    telegram_id = Column(
        Integer(),
        ForeignKey("users.telegram_id"),
        nullable=False,
    )
    word = Column(String(), nullable=False)
    phase = Column(Integer(), default=1)
    next_repetition_on = Column(Date(), default=datetime.now)
    status = Column(Enum(Status), default=Status.in_progress)

    created_at = Column(DateTime(), default=datetime.now)
    updated_at = Column(
        DateTime(), default=datetime.now, onupdate=datetime.now
    )

    user = relationship("Users", back_populates="cards")
