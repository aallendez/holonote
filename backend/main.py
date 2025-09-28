from fastapi import FastAPI
from src.api.router import Router
from src.db.session import engine, Base

app = FastAPI()

# Create database tables
@app.on_event("startup")
async def startup_event():
    Base.metadata.create_all(bind=engine)

# Register routes automatically
Router(app).load_routers()