from sqlalchemy.orm import Session
from app.crud.usuario import get_usuario_by_nombre
from app.core.security import verify_password


def authenticate_user(db: Session, nombre: str, contrasena: str):
    user = get_usuario_by_nombre(db, nombre)
    if not user:
        return None

    if not verify_password(contrasena, user["contrasena_hash"]):
        return None

    return user