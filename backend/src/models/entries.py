from datetime import datetime
from typing import Optional
from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String
from src.db.session import Base


class EntryTable(Base):
    __tablename__ = "entries"

    entry_id = Column(
        String, primary_key=True, index=True, default=lambda: str(uuid4())
    )
    user_id = Column(String, nullable=False, index=True)
    entry_date = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class Entry(BaseModel):
    entry_id: str
    user_id: str
    entry_date: datetime
    title: str
    content: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class EntryCreateRequest(BaseModel):
    entry_date: datetime
    title: str
    content: str


class EntryCreate(BaseModel):
    user_id: str
    entry_date: datetime
    title: str
    content: str


class EntryUpdate(BaseModel):
    title: str
    content: str


class EntryDelete(BaseModel):
    deleted_at: datetime
