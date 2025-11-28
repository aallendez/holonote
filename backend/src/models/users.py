from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, DateTime, String
from src.db.session import Base


class UserTable(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    user_email = Column(String, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    deleted_at = Column(DateTime, nullable=True)


class User(BaseModel):
    user_id: str
    user_name: str
    user_email: str
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class UserCreate(BaseModel):
    user_id: str
    user_name: str
    user_email: str


class UserUpdate(BaseModel):
    user_name: Optional[str] = None
    user_email: Optional[str] = None
