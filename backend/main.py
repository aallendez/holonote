import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import Router
from src.db.session import Base, engine

app = FastAPI()

# CORS configuration to allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://holonote-frontend-prod.s3-website-eu-west-1.amazonaws.com",
        "https://holonote.xyz",
        "https://www.holonote.xyz",
    ],
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
