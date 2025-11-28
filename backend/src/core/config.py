import os

from dotenv import load_dotenv

load_dotenv()


class Settings:
    _instance = None

    # Singleton pattern
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return

        # Firebase settings
        self.FIREBASE_API_KEY = os.getenv("FIREBASE_API_KEY")
        self.FIREBASE_AUTH_DOMAIN = os.getenv("FIREBASE_AUTH_DOMAIN")
        self.FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")
        self.FIREBASE_STORAGE_BUCKET = os.getenv("FIREBASE_STORAGE_BUCKET")
        self.FIREBASE_MSG_SENDER_ID = os.getenv("FIREBASE_MSG_SENDER_ID")
        self.FIREBASE_APP_ID = os.getenv("FIREBASE_APP_ID")
        self.FIREBASE_MEASUREMENT_ID = os.getenv("FIREBASE_MEASUREMENT_ID")
        self.FIREBASE_SERVICE_ACCOUNT_KEY = os.getenv("FIREBASE_SERVICE_ACCOUNT_KEY")

        # Database settings
        self.DATABASE_URL_ENV = os.getenv("DATABASE_URL")
        self.DB_HOST = os.getenv("DB_HOST", "localhost")
        self.DB_USER = os.getenv("DB_USER", "root")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD", "example")
        self.DB_NAME = os.getenv("DB_NAME", "holonote")
        self.DB_PORT = os.getenv("DB_PORT", "5432")

        self._initialized = True

    @property
    def DATABASE_URL(self):
        if self.DATABASE_URL_ENV:
            return self.DATABASE_URL_ENV
        if all(
            [self.DB_HOST, self.DB_USER, self.DB_PASSWORD, self.DB_NAME, self.DB_PORT]
        ):
            return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        raise RuntimeError(
            "DATABASE_URL is not configured. Set DB_* vars or DATABASE_URL."
        )


settings = Settings()  # Creating a global instance
