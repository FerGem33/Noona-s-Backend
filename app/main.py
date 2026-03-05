from fastapi import FastAPI
from app.api.router import api_router

app = FastAPI(title="Noona's FastAPI Backend")

app.include_router(api_router)