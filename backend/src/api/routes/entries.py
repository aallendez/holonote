from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session

from src.models.entries import Entry, EntryCreate, EntryUpdate
from src.db.entries import get_entries, create_entry, update_entry, delete_entry
from src.db.session import get_db
from src.api.routes.auth import get_current_user

router = APIRouter(prefix="/entries", tags=["entries"])

@router.get("/", response_model=List[Entry])
def get_entries_route(db: Session = Depends(get_db)):
    """Get all entries for a user"""
    # For testing without auth, use a default user_id
    test_user_id = "juan"
    return get_entries(test_user_id, db)

@router.post("/", response_model=Entry)
def create_entry_route(entry: EntryCreate, db: Session = Depends(get_db)):
    """Create a new entry"""
    # For testing without auth, set a default user_id
    entry.user_id = "juan"
    return create_entry(entry, db)

@router.put("/{id}", response_model=Entry)
def update_entry_route(id: str, entry: EntryUpdate, db: Session = Depends(get_db)):
    """Update an existing entry"""
    return update_entry(id, entry, db)

@router.delete("/{id}")
def delete_entry_route(id: str, db: Session = Depends(get_db)):
    """Delete an existing entry"""
    return delete_entry(id, db)
