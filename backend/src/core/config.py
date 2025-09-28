from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # Firebase settings
    FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
    FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
    FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
    FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
    FIREBASE_MSG_SENDER_ID = os.getenv("FIREBASE_MSG_SENDER_ID")
    FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID")
    FIREBASE_MEASUREMENT_ID = os.getenv("FIREBASE_MEASUREMENT_ID")
    
    # Database settings
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "example")
    DB_NAME = os.getenv("DB_NAME", "holonote")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    @property
    def DATABASE_URL(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()
