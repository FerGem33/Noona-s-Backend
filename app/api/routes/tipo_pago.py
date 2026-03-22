from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.core.roles import Roles
from app.schemas.tipo_pago import (
    TipoPagoCreate,
    TipoPagoRead,
    TipoPagoUpdate
)
from app.crud import tipo_pago as crud_tipo_pago


router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=TipoPagoRead, status_code=status.HTTP_201_CREATED)
def create_tipo_pago(
    tipo_pago_in: TipoPagoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_tipo_pago.create_tipo_pago(db, tipo_pago_in.descripcion)


@router.get("/", response_model=list[TipoPagoRead])
def read_tipos_pago(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_tipo_pago.get_tipos_pago(db)


@router.get("/{id_tipo_pago}", response_model=TipoPagoRead)
def read_tipo_pago(
    id_tipo_pago: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    tipo_pago = crud_tipo_pago.get_tipo_pago_by_id(db, id_tipo_pago)
    if not tipo_pago:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    return tipo_pago


@router.put("/{id_tipo_pago}", response_model=TipoPagoRead)
def update_tipo_pago(
    id_tipo_pago: int,
    tipo_pago_in: TipoPagoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    tipo_pago = crud_tipo_pago.update_tipo_pago(
        db,
        id_tipo_pago,
        tipo_pago_in.descripcion
    )
    if not tipo_pago:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    return tipo_pago


@router.delete("/{id_tipo_pago}", response_model=TipoPagoRead)
def delete_tipo_pago(
    id_tipo_pago: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    tipo_pago = crud_tipo_pago.delete_tipo_pago(db, id_tipo_pago)
    if not tipo_pago:
        raise HTTPException(status_code=404, detail="Tipo de pago no encontrado")
    return tipo_pago