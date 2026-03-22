from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.core.roles import Roles
from app.schemas.unidad_medida import (
    UnidadMedidaCreate,
    UnidadMedidaRead,
    UnidadMedidaUpdate
)
from app.crud import unidad_medida as crud_unidad


router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=UnidadMedidaRead, status_code=status.HTTP_201_CREATED)
def create_unidad(
    unidad_in: UnidadMedidaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_unidad.create_unidad(
        db,
        unidad_in.descripcion,
        unidad_in.abreviatura
    )


@router.get("/", response_model=list[UnidadMedidaRead])
def read_unidades(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_unidad.get_unidades(db)


@router.get("/{id_unidad}", response_model=UnidadMedidaRead)
def read_unidad(
    id_unidad: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    unidad = crud_unidad.get_unidad_by_id(db, id_unidad)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return unidad


@router.put("/{id_unidad}", response_model=UnidadMedidaRead)
def update_unidad(
    id_unidad: int,
    unidad_in: UnidadMedidaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    unidad = crud_unidad.update_unidad(
        db,
        id_unidad,
        unidad_in.descripcion,
        unidad_in.abreviatura
    )
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return unidad


@router.delete("/{id_unidad}", response_model=UnidadMedidaRead)
def delete_unidad(
    id_unidad: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    unidad = crud_unidad.delete_unidad(db, id_unidad)
    if not unidad:
        raise HTTPException(status_code=404, detail="Unidad no encontrada")
    return unidad