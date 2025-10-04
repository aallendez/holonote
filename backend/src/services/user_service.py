from sqlalchemy.orm import Session
from src.models.users import UserCreate
from src.models.holos import HoloCreate
from src.db.users import get_user_by_id, create_user
from src.db.holos import create_holo_config
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
        # Create user
        user_create = UserCreate(
            user_id=user_id,
            user_name=user_name,
            user_email=user_email
        )
        new_user = create_user(user_create, db)
        
        # Create holo config for the new user
        holo_create = HoloCreate(
            user_id=user_id,
            questions=DEFAULT_HOLO_QUESTIONS
        )
        new_holo = create_holo_config(user_id, holo_create, db)
        
        return {
            'user_id': new_user.user_id,
            'user_name': new_user.user_name,
            'user_email': new_user.user_email
        }
        
    except Exception as e:
        # If anything fails, rollback the transaction
        db.rollback()
        print(f"Error creating user and holo: {str(e)}")
        return None
