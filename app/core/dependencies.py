from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        id_usuario = int(payload.get("sub"))
    except (JWTError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    result = db.execute(
        text("""
            SELECT u.id_usuario, r.id_rol, u.nombre, r.descripcion as rol
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = :id_usuario
        """),
        {"id_usuario": id_usuario}
    ).mappings().first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    return result


def require_roles(*allowed_roles):
    def role_checker(current_user = Depends(get_current_user)):
        if current_user["rol"] not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail="No tienes permisos para acceder a este recurso"
            )
        return current_user
    return role_checker


def validate_key_exist(db: Session, key_value: int, table_name: str, key_field: str):

    query = text(f"""
        SELECT {key_field}
        FROM {table_name}
        WHERE {key_field} = :key_value
    """)

    result = db.execute(query, {"key_value": key_value}).first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"El id {key_value} no existe en la tabla {table_name}"
        )

    return key_value