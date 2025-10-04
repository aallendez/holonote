import firebase_admin
from firebase_admin import auth, credentials
from .config import settings
from sqlalchemy.orm import Session
from src.db.session import SessionLocal
from src.services.user_service import ensure_user_exists
import json

# Initialize Firebase Admin SDK
try:
    firebase_admin.get_app()
except ValueError:
    # Parse the service account key from environment variable
    service_account_info = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_KEY)
    cred = credentials.Certificate(service_account_info)
    firebase_admin.initialize_app(cred, {
        "projectId": settings.FIREBASE_PROJECT_ID,
    })

def verify_token(id_token: str):
    """Verify Firebase ID token from frontend"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        return None

def verify_token_and_ensure_user(id_token: str):
    """Verify Firebase ID token and ensure user exists in database"""
    try:
        decoded_token = auth.verify_id_token(id_token)
        if not decoded_token:
            return None
        
        # Ensure user exists in our database
        db = SessionLocal()
        try:
            user_data = ensure_user_exists(decoded_token, db)
            if user_data:
                # Add user data to the token for use in routes
                decoded_token['user_data'] = user_data
                return decoded_token
            return None
        finally:
            db.close()
            
    except Exception as e:
        return None
