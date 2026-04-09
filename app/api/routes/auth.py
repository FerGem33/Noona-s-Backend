from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.core.security import create_access_token
from app.schemas.auth import Token
from app.schemas.usuario import UsuarioRead
from app.crud.auth import authenticate_user
from app.crud import usuario as crud_usuario
from app.core.roles import Roles

router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/login", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    access_token = create_access_token(
        data={"sub": str(user["id_usuario"])}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/usuario{usuario_nombre}", response_model=UsuarioRead)
def read_usuario(
    usuario_nombre: str,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    usuario = crud_usuario.get_usuario_by_nombre(db, usuario_nombre)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

