from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.entries import Entry, EntryCreate, EntryUpdate
from pydantic import BaseModel
from src.db.entries import get_entries, create_entry, update_entry, delete_entry
from src.db.session import get_db
from src.api.routes.auth import get_current_user

router = APIRouter(prefix="/entries", tags=["entries"])

@router.get("/", response_model=List[Entry])
def get_entries_route(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Get all entries for a user"""
    return get_entries(user["uid"], db)

@router.post("/", response_model=Entry)
def create_entry_route(entry: EntryCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Create a new entry"""
    # Set the user_id from the authenticated user
    entry.user_id = user["uid"]
    return create_entry(entry, db)

@router.put("/{id}", response_model=Entry)
def update_entry_route(id: str, entry: EntryUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Update an existing entry"""
    return update_entry(id, entry, db)

@router.delete("/{id}")
def delete_entry_route(id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Delete an existing entry"""
    return delete_entry(id, db)


# @router.get("/", response_model=List[Entry])
# def get_entries_route(db: Session = Depends(get_db)):
#     """Get all entries for a user"""
#     # For testing without auth, use a default user_id
#     test_user_id = "juan"
#     return get_entries(test_user_id, db)

# class EntryCreatePayload(BaseModel):
#     entry_date: datetime
#     title: str
#     content: str
#     score: int


# @router.post("/", response_model=Entry)
# def create_entry_route(entry: EntryCreatePayload, db: Session = Depends(get_db)):
#     """Create a new entry"""
#     # For testing without auth, set a default user_id
#     entry_with_user = EntryCreate(
#         user_id="juan",
#         entry_date=entry.entry_date,
#         title=entry.title,
#         content=entry.content,
#         score=entry.score,
#     )
#     return create_entry(entry_with_user, db)

# @router.put("/{id}", response_model=Entry)
# def update_entry_route(id: str, entry: EntryUpdate, db: Session = Depends(get_db)):
#     """Update an existing entry"""
#     return update_entry(id, entry, db)

# @router.delete("/{id}")
# def delete_entry_route(id: str, db: Session = Depends(get_db)):
#     """Delete an existing entry"""
#     return delete_entry(id, db)
