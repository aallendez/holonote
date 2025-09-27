import importlib
import pkgutil
from fastapi import FastAPI
from . import routes

class Router:
    def __init__(self, app: FastAPI):
        self.app = app

    def load_routers(self):
        for _, module_name, _ in pkgutil.iter_modules(routes.__path__):
            module = importlib.import_module(f"{routes.__name__}.{module_name}")
            if hasattr(module, "router"):
                self.app.include_router(module.router)