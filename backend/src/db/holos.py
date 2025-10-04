from datetime import date
from sqlalchemy.orm import Session

from src.models.holos import HoloTable, HoloDailiesTable, HoloCreate, HoloUpdate, HoloDailyCreate

# Holo config
def get_holo_config(user_id: str, db: Session):
    """Get the holo questions config for a user"""
    return (
        db.query(HoloTable)
        .filter(HoloTable.user_id == user_id)
        .first()
    )

def update_holo_config(user_id: str, holo: HoloUpdate, db: Session):
    """Update the holo questions config for a user"""
    db_holo = db.query(HoloTable).filter(HoloTable.user_id == user_id).first()
    if not db_holo:
        return None
    db_holo.questions = holo.questions
    db.commit()
    db.refresh(db_holo)
    return db_holo

def create_holo_config(user_id: str, holo: HoloCreate, db: Session):
    db_holo = HoloTable(
        user_id=user_id,
        questions=holo.questions,
    )
    db.add(db_holo)
    db.commit()
    db.refresh(db_holo)
    return db_holo

# Holo daily
def get_holo_daily_by_date(holo_id: str, entry_date: date, db: Session):
    """Get the holo daily for a user"""
    return (
        db.query(HoloDailiesTable)
        .filter(HoloDailiesTable.holo_id == holo_id, HoloDailiesTable.entry_date == entry_date)
        .first()
    )
    
def get_latest_holo_daily(holo_id: str, db: Session):
    """Get the latest holo daily for a user"""
    return (
        db.query(HoloDailiesTable)
        .filter(HoloDailiesTable.holo_id == holo_id)
        .order_by(HoloDailiesTable.entry_date.desc())
        .first()
    )
    
def create_holo_daily(holo_id: str, holo_daily: HoloDailyCreate, db: Session):
    """Create a new holo daily for a user"""
    db_holo_daily = HoloDailiesTable(
        holo_id=holo_id,
        entry_date=holo_daily.entry_date,
        score=holo_daily.score,
        answers=holo_daily.answers,
    )
    db.add(db_holo_daily)
    db.commit()
    db.refresh(db_holo_daily)
    return db_holo_daily