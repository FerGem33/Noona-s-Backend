from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.utils.files import ensure_upload_directories
from app.api.router import api_router

app = FastAPI(title="Noona's FastAPI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:5173",
        "http://localhost:5500"
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

ensure_upload_directories()

app.mount("/media", StaticFiles(directory=settings.UPLOAD_DIR), name="media")
app.include_router(api_router)