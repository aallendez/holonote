from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Integer
from uuid import uuid4
from src.db.session import Base
from typing import Optional

class EntryTable(Base):
    __tablename__ = "entries"

    entry_id = Column(String, primary_key=True, index=True, default=lambda: str(uuid4()))
    user_id = Column(String, nullable=False, index=True)
    entry_date = Column(DateTime, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)
    

class Entry(BaseModel):
    entry_id: str
    user_id: str
    entry_date: datetime
    title: str
    content: str
    score: int
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None
    
class EntryCreate(BaseModel):
    user_id: str
    entry_date: datetime
    title: str
    content: str
    score: int

class EntryUpdate(BaseModel):
    title: str
    content: str
    score: int

class EntryDelete(BaseModel):
    deleted_at: datetime