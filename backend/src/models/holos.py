from datetime import date, datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel, ConfigDict, field_serializer
from sqlalchemy import (
    JSON,
    Column,
    Date,
    DateTime,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from src.db.session import Base


class HoloTable(Base):
    """This table stores the holo configuration and is linked to all holo_dailies for a user"""

    __tablename__ = "holo"
    __table_args__ = (UniqueConstraint("user_id"),)

    holo_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(
        String,
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )  # FK to users.user_id in DB
    questions = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class HoloDailiesTable(Base):
    """This table stores the holo_dailies for a user"""

    __tablename__ = "holo_dailies"
    __table_args__ = (UniqueConstraint("holo_id", "entry_date"),)

    holo_daily_id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid4())
    )
    holo_id = Column(
        String,
        ForeignKey("holo.holo_id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    entry_date = Column(Date, nullable=False)  # just date, not timestamp
    score = Column(Integer, nullable=False)
    answers = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class Holo(BaseModel):
    holo_id: str
    user_id: str
    questions: list[str]


class HoloCreate(BaseModel):
    user_id: str
    questions: list[str]


class HoloUpdate(BaseModel):
    questions: list[str]


class HoloDaily(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    holo_daily_id: str
    holo_id: str
    entry_date: date
    score: int
    answers: dict[str, str | int | bool]

    @field_serializer("entry_date")
    def serialize_date(self, v: date, _info):
        return v.isoformat()  # automatically convert to string on export


class HoloDailyCreate(BaseModel):
    entry_date: str  # Accept ISO date string from frontend
    score: int
    answers: dict[str, str | int | bool]
