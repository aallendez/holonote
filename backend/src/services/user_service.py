from sqlalchemy.orm import Session
from src.models.users import UserCreate
from src.models.holos import HoloCreate
from src.db.users import get_user_by_id, create_user_in_transaction
from src.db.holos import create_holo_config_in_transaction
from typing import Optional

# Default holo questions for new users (binary yes/no questions)
DEFAULT_HOLO_QUESTIONS = [
    "Have you slept +8h?",
    "Have you worked out?",
    "Have you eaten healthy?",
    "Have you done a hobby?",
    "Have you gone to uni?"
]

def ensure_user_exists(firebase_user_data: dict, db: Session) -> Optional[dict]:
    """
    Ensures a user exists in the database. If not, creates the user and their holo config.
    Returns user data if successful, None if failed.
    
    IMPORTANT: This design is so that in the future users can customize their holo questions. If not, we would just hardcode the questions in the database.
    
    Args:
        firebase_user_data: Dictionary containing Firebase user data (uid, email, name, etc.)
        db: Database session
    
    Returns:
        Dictionary with user data or None if creation failed
    """
    user_id = firebase_user_data.get('uid')
    user_email = firebase_user_data.get('email', '')
    user_name = firebase_user_data.get('name', firebase_user_data.get('display_name', 'User'))
    
    if not user_id:
        return None
    
    # Check if user already exists
    existing_user = get_user_by_id(user_id, db)
    if existing_user:
        return {
            'user_id': existing_user.user_id,
            'user_name': existing_user.user_name,
            'user_email': existing_user.user_email
        }
    
    try:
        # Begin a single transaction that wraps both creations
        # Rely on SQLAlchemy session transaction management; commit only once
        user_create = UserCreate(
            user_id=user_id,
            user_name=user_name,
            user_email=user_email
        )
        new_user = create_user_in_transaction(user_create, db)

        holo_create = HoloCreate(
            user_id=user_id,
            questions=DEFAULT_HOLO_QUESTIONS
        )
        _ = create_holo_config_in_transaction(user_id, holo_create, db) # _ is used to avoid the return value since we don't need it

        db.commit()

        return {
            'user_id': new_user.user_id,
            'user_name': new_user.user_name,
            'user_email': new_user.user_email
        }

    except Exception as e:
        db.rollback()
        print(f"Error creating user and holo: {str(e)}")
        return None
