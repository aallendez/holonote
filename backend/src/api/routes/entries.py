from fastapi import APIRouter, HTTPException, Depends
from typing import List
from uuid import uuid4
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from pydantic import ValidationError

from src.models.entries import Entry, EntryCreate, EntryCreateRequest, EntryUpdate
from pydantic import BaseModel
from src.db.entries import get_entries, create_entry, update_entry, delete_entry
from src.db.session import get_db
from src.api.routes.auth import get_current_user

router = APIRouter(prefix="/entries", tags=["entries"])

@router.get("/", response_model=List[Entry])
def get_entries_route(db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Get all entries for a user"""
    try:
        return get_entries(user["uid"], db)
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error while fetching entries: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while fetching entries: {str(e)}")


@router.post("/", response_model=Entry)
def create_entry_route(entry: EntryCreateRequest, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Create a new entry"""
    try:
        # Construct full create model with user id from auth
        entry_with_user = EntryCreate(
            user_id=user["uid"],
            entry_date=entry.entry_date,
            title=entry.title,
            content=entry.content,
        )
        return create_entry(entry_with_user, db)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail=f"Data integrity error: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error while creating entry: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while creating entry: {str(e)}")


@router.put("/{id}", response_model=Entry)
def update_entry_route(id: str, entry: EntryUpdate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Update an existing entry"""
    try:
        result = update_entry(id, entry, db)
        if result is None:
            raise HTTPException(status_code=404, detail="Entry not found")
        return result
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=f"Validation error: {str(e)}")
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error while updating entry: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while updating entry: {str(e)}")


@router.delete("/{id}")
def delete_entry_route(id: str, db: Session = Depends(get_db), user=Depends(get_current_user)):
    """Delete an existing entry"""
    try:
        result = delete_entry(id, db)
        if result is None:
            raise HTTPException(status_code=404, detail="Entry not found")
        return {"message": "Entry deleted successfully"}
    except HTTPException:
        raise  # Re-raise HTTPException as-is
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error while deleting entry: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error while deleting entry: {str(e)}")
