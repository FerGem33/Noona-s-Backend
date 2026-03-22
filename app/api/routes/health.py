from fastapi import APIRouter
from sqlalchemy import create_engine, text
import os

router = APIRouter()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

@router.get("/")
def health():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        return {"status": "ok", "database": "reachable"}
    except Exception as e:
        return {"status": "error", "database": "unreachable", "detail": str(e)}