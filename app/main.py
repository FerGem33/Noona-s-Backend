from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.utils.files import ensure_upload_directories
from app.api.router import api_router

app = FastAPI(title="Noona's FastAPI Backend")
ensure_upload_directories()
app.mount("/media", StaticFiles(directory=settings.UPLOAD_DIR), name="media")
app.include_router(api_router)