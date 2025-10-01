import firebase_admin
from firebase_admin import auth, credentials
from .config import settings
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
