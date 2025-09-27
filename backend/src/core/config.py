from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
    FIREBASE_MSG_SENDER_ID = os.getenv("FIREBASE_MSG_SENDER_ID")
    FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID")
    FIREBASE_MEASUREMENT_ID = os.getenv("FIREBASE_MEASUREMENT_ID")

settings = Settings()
