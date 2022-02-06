from fastapi import FastAPI
from web.app.routes.history import api_router

my_app = FastAPI()
my_app.include_router(api_router)
