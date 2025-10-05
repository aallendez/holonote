from sqlalchemy.orm import Session
from datetime import datetime
from src.models.users import UserTable, UserCreate, UserUpdate, User

def get_user_by_id(user_id: str, db: Session):
    """Get a user by their ID"""
    return db.query(UserTable).filter(UserTable.user_id == user_id).first()

def get_user_by_email(user_email: str, db: Session):
    """Get a user by their email"""
    return db.query(UserTable).filter(UserTable.user_email == user_email).first()

def create_user(user: UserCreate, db: Session):
    """Create a new user"""
    db_user = UserTable(
        user_id=user.user_id,
        user_name=user.user_name,
        user_email=user.user_email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_user_in_transaction(user: UserCreate, db: Session):
    """Create a new user without committing; intended for use within an external transaction."""
    db_user = UserTable(
        user_id=user.user_id,
        user_name=user.user_name,
        user_email=user.user_email
    )
    db.add(db_user)
    # Flush to persist to DB without committing so FKs/defaults are available
    db.flush()
    db.refresh(db_user)
    return db_user

def update_user(user_id: str, user: UserUpdate, db: Session):
    """Update an existing user"""
    db_user = db.query(UserTable).filter(UserTable.user_id == user_id).first()
    if not db_user:
        return None
    
    if user.user_name is not None:
        db_user.user_name = user.user_name
    if user.user_email is not None:
        db_user.user_email = user.user_email
    
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(user_id: str, db: Session):
    """Soft delete a user by setting deleted_at timestamp"""
    db_user = db.query(UserTable).filter(UserTable.user_id == user_id).first()
    if not db_user:
        return None
    
    db_user.deleted_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

def user_exists(user_id: str, db: Session):
    """Check if a user exists in the database"""
    return db.query(UserTable).filter(UserTable.user_id == user_id).first() is not None
