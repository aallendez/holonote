import logging
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import Router
from src.db.session import Base, engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# CORS configuration
# In production, frontend and backend are served from the same ALB
# Allow all origins for now - can be restricted later for better security
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create database tables
@app.on_event("startup")
async def startup_event():
    # During pytest, tests manage their own in-memory DB and schema
    if os.getenv(
        "PYTEST_CURRENT_TEST"
    ):  # Automatically set by pytest when running tests
        return

    try:
        logger.info("Attempting to create database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {str(e)}", exc_info=True)
        # Don't raise - allow the app to start even if tables already exist
        # This prevents the app from crashing if tables are already created


# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok"}


# Register routes automatically
Router(app).load_routers()
