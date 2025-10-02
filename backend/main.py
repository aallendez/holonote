from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.router import Router
from src.db.session import engine, Base

app = FastAPI()

# CORS configuration to allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Create database tables
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

# Register routes automatically
Router(app).load_routers()