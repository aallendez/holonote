import firebase_admin
from firebase_admin import auth, credentials
from .config import settings

# Initialize Firebase Admin only once
if not firebase_admin._apps:
    cred = credentials.ApplicationDefault() 
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
