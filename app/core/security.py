import hashlib
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def _prehash(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def hash_password(password: str):
    return pwd_context.hash(_prehash(password))


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(_prehash(plain_password), hashed_password)


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire})
    return jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )