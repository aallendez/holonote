import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import Router
from src.db.session import Base, engine

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
    Base.metadata.create_all(bind=engine)


# Register routes automatically
Router(app).load_routers()
