from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.core.roles import Roles
from app.schemas.estado import EstadoCreate, EstadoRead, EstadoUpdate
from app.crud import estado as crud_estado


router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=EstadoRead, status_code=status.HTTP_201_CREATED)
def create_estado(
    estado_in: EstadoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_estado.create_estado(db, estado_in.descripcion)


@router.get("/", response_model=list[EstadoRead])
def read_estados(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_estado.get_estados(db)


@router.get("/{id_estado}", response_model=EstadoRead)
def read_estado(
    id_estado: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    estado = crud_estado.get_estado_by_id(db, id_estado)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado


@router.put("/{id_estado}", response_model=EstadoRead)
def update_estado(
    id_estado: int,
    estado_in: EstadoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    estado = crud_estado.update_estado(
        db,
        id_estado,
        estado_in.descripcion
    )
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado


@router.delete("/{id_estado}", response_model=EstadoRead)
def delete_estado(
    id_estado: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    estado = crud_estado.delete_estado(db, id_estado)
    if not estado:
        raise HTTPException(status_code=404, detail="Estado no encontrado")
    return estado