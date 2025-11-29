import json
import logging

import firebase_admin
from firebase_admin import auth, credentials
from src.db.session import SessionLocal
from src.services.user_service import ensure_user_exists

from .config import settings

logger = logging.getLogger(__name__)


# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK if not already initialized"""
    try:
        firebase_admin.get_app()
        logger.info("Firebase Admin SDK already initialized")
        return True
    except ValueError:
        # Only initialize if service account key is provided (skip in test environments)
        if not settings.FIREBASE_SERVICE_ACCOUNT_KEY:
            logger.warning(
                "FIREBASE_SERVICE_ACCOUNT_KEY not set. Firebase Admin SDK will not be initialized."
            )
            return False

        try:
            # Parse the service account key from environment variable
            service_account_info = json.loads(settings.FIREBASE_SERVICE_ACCOUNT_KEY)
            # Extract project_id from service account key (it's already in there)
            project_id = service_account_info.get("project_id")
            if not project_id:
                logger.error("Firebase service account key missing project_id")
                return False
            cred = credentials.Certificate(service_account_info)
            firebase_admin.initialize_app(
                cred,
                {
                    "projectId": project_id,
                },
            )
            logger.info("Firebase Admin SDK initialized successfully")
            return True
        except json.JSONDecodeError as e:
            logger.error(
                f"Failed to parse FIREBASE_SERVICE_ACCOUNT_KEY as JSON: {str(e)}"
            )
            return False
        except Exception as e:
            logger.error(
                f"Failed to initialize Firebase Admin SDK: {str(e)}", exc_info=True
            )
            return False


# Initialize on module import
initialize_firebase()


def verify_token(id_token: str):
    """Verify Firebase ID token from frontend"""
    try:
        # Check if Firebase is initialized
        firebase_admin.get_app()
    except ValueError:
        logger.error(
            "Firebase Admin SDK not initialized. Cannot verify tokens. "
            "Set FIREBASE_SERVICE_ACCOUNT_KEY environment variable."
        )
        return None

    try:
        decoded_token = auth.verify_id_token(id_token)
        return decoded_token
    except Exception as e:
        logger.warning("verify_token failed: %s: %s", e.__class__.__name__, str(e))
        return None


def verify_token_and_ensure_user(id_token: str):
    """Verify Firebase ID token and ensure user exists in database"""
    try:
        # Check if Firebase is initialized
        firebase_admin.get_app()
    except ValueError:
        logger.error(
            "Firebase Admin SDK not initialized. Cannot verify tokens. "
            "Set FIREBASE_SERVICE_ACCOUNT_KEY environment variable."
        )
        return None

    try:
        decoded_token = auth.verify_id_token(id_token)
        if not decoded_token:
            logger.warning(
                "verify_token_and_ensure_user: token verification returned no claims"
            )
            return None

        # Ensure user exists in our database
        db = SessionLocal()
        try:
            user_data = ensure_user_exists(decoded_token, db)
            if user_data:
                # Add user data to the token for use in routes
                decoded_token["user_data"] = user_data
                return decoded_token
            return None
        finally:
            db.close()

    except Exception as e:
        logger.warning(
            "verify_token_and_ensure_user failed: %s: %s", e.__class__.__name__, str(e)
        )
        return None
