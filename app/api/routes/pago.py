from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.pago import PagoCreate, PagoRead, PagoUpdate
from app.crud import pago as crud_pago


router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=PagoRead, status_code=status.HTTP_201_CREATED)
def create_pago(
    pago_in: PagoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, pago_in.id_pedido, "pedidos", "id_pedido")
    validate_key_exist(db, pago_in.id_estado_pago, "estado_pago", "id_estado_pago")
    validate_key_exist(db, pago_in.id_tipo_pago, "tipo_pago", "id_tipo_pago")

    return crud_pago.create_pago(
        db,
        pago_in.id_pedido,
        pago_in.id_estado_pago,
        pago_in.id_tipo_pago,
        pago_in.anticipo,
        pago_in.monto,
        pago_in.fecha
    )


@router.get("/", response_model=list[PagoRead])
def read_pagos(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_pago.get_pagos(db)


@router.get("/{id_pago}", response_model=PagoRead)
def read_pago(
    id_pago: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    pago = crud_pago.get_pago_by_id(db, id_pago)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago


@router.put("/{id_pago}", response_model=PagoRead)
def update_pago(
    id_pago: int,
    pago_in: PagoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if pago_in.id_pedido is not None:
        validate_key_exist(db, pago_in.id_pedido, "pedidos", "id_pedido")

    if pago_in.id_estado_pago is not None:
        validate_key_exist(db, pago_in.id_estado_pago, "estado_pago", "id_estado_pago")

    if pago_in.id_tipo_pago is not None:
        validate_key_exist(db, pago_in.id_tipo_pago, "tipo_pago", "id_tipo_pago")

    pago = crud_pago.update_pago(
        db,
        id_pago,
        pago_in.id_pedido,
        pago_in.id_estado_pago,
        pago_in.id_tipo_pago,
        pago_in.anticipo,
        pago_in.monto,
        pago_in.fecha
    )

    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")

    return pago


@router.delete("/{id_pago}", response_model=PagoRead)
def delete_pago(
    id_pago: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    pago = crud_pago.delete_pago(db, id_pago)
    if not pago:
        raise HTTPException(status_code=404, detail="Pago no encontrado")
    return pago