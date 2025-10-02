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
    FIREBASE_SERVICE_ACCOUNT_KEY = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")
    
    # Database settings
    DATABASE_URL_ENV = os.getenv("DATABASE_URL")
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "example")
    DB_NAME = os.getenv("DB_NAME", "holonote")
    DB_PORT = os.getenv("DB_PORT", "5432")
    
    @property
    def DATABASE_URL(self):
        # 1) If DB_* vars are present (as in docker-compose), build a Postgres URL
        if self.DB_HOST and self.DB_USER and self.DB_PASSWORD and self.DB_NAME and self.DB_PORT:
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        # 2) Explicit DATABASE_URL next (useful for tests or overrides)
        if self.DATABASE_URL_ENV:
            return self.DATABASE_URL_ENV
        # 3) Safe default for local dev/tests
        return "sqlite:///./holonote.db"

settings = Settings()
