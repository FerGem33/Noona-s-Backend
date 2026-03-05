from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.schemas.rol import RolCreate, RolRead, RolUpdate
from app.crud import rol as crud_rol
from app.core.roles import Roles


router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=RolRead, status_code=status.HTTP_201_CREATED)
def create_rol(
    rol_in: RolCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_rol.create_rol(db, rol_in.descripcion)


@router.get("/", response_model=list[RolRead])
def read_roles(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_rol.get_roles(db)


@router.get("/{id_rol}", response_model=RolRead)
def read_rol(
    id_rol: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    rol = crud_rol.get_rol_by_id(db, id_rol)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return rol


@router.put(    "/{id_rol}", response_model=RolRead)
def update_rol(
    id_rol: int,
    rol_in: RolUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    rol = crud_rol.update_rol(db, id_rol, rol_in.descripcion)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return rol


@router.delete("/{id_rol}", response_model=RolRead)
def delete_rol(
    id_rol: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    rol = crud_rol.delete_rol(db, id_rol)
    if not rol:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Rol no encontrado"
        )
    return rol