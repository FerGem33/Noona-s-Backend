from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.schemas.usuario import UsuarioCreate, UsuarioRead, UsuarioUpdate
from app.crud import usuario as crud_usuario
from app.core.roles import Roles

router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def create_usuario(
    usuario_in: UsuarioCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, usuario_in.id_rol, "rol", "id_rol")

    return crud_usuario.create_usuario(
        db,
        usuario_in.nombre,
        usuario_in.id_rol,
        usuario_in.contrasena
    )


@router.get("/", response_model=list[UsuarioRead])
def read_usuarios(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_usuario.get_usuarios(db)


@router.get("/{usuario_id}", response_model=UsuarioRead)
def read_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    usuario = crud_usuario.get_usuario_by_id(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.put("/{usuario_id}", response_model=UsuarioRead)
def update_usuario(
    usuario_id: int,
    usuario_in: UsuarioUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):

    if usuario_in.id_rol is not None:
        validate_key_exist(db, usuario_in.id_rol, "rol", "id_rol")

    usuario = crud_usuario.update_usuario(
        db,
        usuario_id,
        usuario_in.nombre,
        usuario_in.id_rol,
        usuario_in.contrasena
    )
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.delete("/{usuario_id}", response_model=UsuarioRead)
def delete_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    usuario = crud_usuario.delete_usuario(db, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario