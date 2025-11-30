import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import Router

# Import auth module early to trigger Firebase initialization
from src.core import auth  # noqa: F401
from src.core.metrics import get_amp_writer
from src.db.session import Base, engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
# Get allowed origins from environment or use defaults
# Note: Cannot use "*" with allow_credentials=True, so we need explicit origins
allowed_origins = [
    "http://holonote-frontend-prod.s3-website-eu-west-1.amazonaws.com",
    "https://d1i7v3bh4lq4r0.cloudfront.net",  # CloudFront HTTPS URL
    "http://holonote-alb-1922459695.eu-west-1.elb.amazonaws.com",
    "http://localhost:5173",  # For local development
    "http://localhost:3000",  # Alternative local port
    "https://holonote.xyz",
    "https://www.holonote.xyz",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes automatically (before instrumentator)
Router(app).load_routers()

# Set up Prometheus metrics after routes are registered
try:
    from prometheus_fastapi_instrumentator import Instrumentator

    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)
    logger.info("Prometheus metrics instrumentation enabled at /metrics")
except ImportError as e:
    logger.error(
        f"prometheus-fastapi-instrumentator import failed: {str(e)}. "
        f"Python path: {os.environ.get('PYTHONPATH', 'not set')}. "
        "Metrics will not be exposed."
    )
except Exception as e:
    logger.error(f"Failed to set up Prometheus metrics: {str(e)}", exc_info=True)


# Create database tables and verify Firebase initialization
@app.on_event("startup")
async def startup_event():
    # During pytest, tests manage their own in-memory DB and schema
    if os.getenv(
        "PYTEST_CURRENT_TEST"
    ):  # Automatically set by pytest when running tests
        return

    # Verify Firebase initialization
    try:
        import firebase_admin

        firebase_admin.get_app()
        logger.info("Firebase Admin SDK initialized successfully")
    except ValueError:
        logger.warning(
            "Firebase Admin SDK not initialized. "
            "FIREBASE_SERVICE_ACCOUNT_KEY may be missing or invalid. "
            "Authentication will fail."
        )

    try:
        logger.info("Attempting to create database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}", exc_info=True)
        # Don't raise - allow the app to start even if tables already exist
        # This prevents the app from crashing if tables are already created

    # Initialize AMP writer (logs endpoint if configured)
    amp_writer = get_amp_writer()
    if amp_writer and amp_writer.enabled:
        logger.info(
            "AMP endpoint configured. Consider using AWS Distro for OpenTelemetry for remote write."
        )
