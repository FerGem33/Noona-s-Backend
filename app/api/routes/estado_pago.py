from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.core.roles import Roles
from app.schemas.estado_pago import (
    EstadoPagoCreate,
    EstadoPagoRead,
    EstadoPagoUpdate
)
from app.crud import estado_pago as crud_estado_pago


router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=EstadoPagoRead, status_code=status.HTTP_201_CREATED)
def create_estado_pago(
    estado_pago_in: EstadoPagoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_estado_pago.create_estado_pago(db, estado_pago_in.descripcion)


@router.get("/", response_model=list[EstadoPagoRead])
def read_estados_pago(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_estado_pago.get_estados_pago(db)


@router.get("/{id_estado_pago}", response_model=EstadoPagoRead)
def read_estado_pago(
    id_estado_pago: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    estado_pago = crud_estado_pago.get_estado_pago_by_id(db, id_estado_pago)
    if not estado_pago:
        raise HTTPException(status_code=404, detail="Estado de pago no encontrado")
    return estado_pago


@router.put("/{id_estado_pago}", response_model=EstadoPagoRead)
def update_estado_pago(
    id_estado_pago: int,
    estado_pago_in: EstadoPagoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    estado_pago = crud_estado_pago.update_estado_pago(
        db,
        id_estado_pago,
        estado_pago_in.descripcion
    )
    if not estado_pago:
        raise HTTPException(status_code=404, detail="Estado de pago no encontrado")
    return estado_pago


@router.delete("/{id_estado_pago}", response_model=EstadoPagoRead)
def delete_estado_pago(
    id_estado_pago: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    estado_pago = crud_estado_pago.delete_estado_pago(db, id_estado_pago)
    if not estado_pago:
        raise HTTPException(status_code=404, detail="Estado de pago no encontrado")
    return estado_pago