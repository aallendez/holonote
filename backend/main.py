from fastapi import FastAPI
from src.api.router import Router

app = FastAPI()

# Register routes automatically
Router(app).load_routers()