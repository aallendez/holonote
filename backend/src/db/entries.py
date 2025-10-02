from datetime import datetime
from uuid import uuid4
from sqlalchemy.orm import Session

from src.models.entries import EntryTable, EntryCreate, EntryUpdate, EntryDelete

    
def get_entries(user_id: str, db: Session):
    """Get all entries for a user"""
    return (
        db.query(EntryTable)
        .filter(EntryTable.user_id == user_id, EntryTable.deleted_at == None)
        .order_by(EntryTable.created_at.desc())
        .all()
    )


def create_entry(entry: EntryCreate, db: Session):
    """Create a new entry"""
    db_entry = EntryTable(
        entry_id=str(uuid4()),
        user_id=entry.user_id,
        entry_date=entry.entry_date,
        title=entry.title,
        content=entry.content,
    )
    db.add(db_entry)
    db.commit()
    db.refresh(db_entry)
    return db_entry


def update_entry(entry_id: str, entry: EntryUpdate, db: Session):
    """Update an existing entry"""
    db_entry = db.query(EntryTable).filter(EntryTable.entry_id == entry_id).first()
    if not db_entry:
        return None

    db_entry.title = entry.title
    db_entry.content = entry.content
    db_entry.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_entry)
    return db_entry


def delete_entry(entry_id: str, db: Session):
    """Delete an existing entry"""
    db_entry = db.query(EntryTable).filter(EntryTable.entry_id == entry_id).first()
    if not db_entry:
        return None

    db_entry.deleted_at = datetime.utcnow()
    db.commit()
    return db_entry
