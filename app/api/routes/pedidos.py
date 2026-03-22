from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.pedidos import PedidoCreate, PedidoRead, PedidoUpdate
from app.crud import pedidos as crud_pedidos


router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=PedidoRead, status_code=status.HTTP_201_CREATED)
def create_pedido(
    pedido_in: PedidoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, pedido_in.id_direccion, "direccion", "id_direccion")
    validate_key_exist(db, pedido_in.id_estado, "estado", "id_estado")
    validate_key_exist(db, pedido_in.id_cliente, "cliente", "id_cliente")

    return crud_pedidos.create_pedido(
        db,
        pedido_in.id_direccion,
        pedido_in.id_estado,
        pedido_in.id_cliente,
        pedido_in.fecha_entrega,
        pedido_in.fecha_pedido,
        pedido_in.comentario,
        pedido_in.tipo_entrega,
        pedido_in.subtotal,
        pedido_in.total
    )


@router.get("/", response_model=list[PedidoRead])
def read_pedidos(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_pedidos.get_pedidos(db)


@router.get("/{id_pedido}", response_model=PedidoRead)
def read_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    pedido = crud_pedidos.get_pedido_by_id(db, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@router.put("/{id_pedido}", response_model=PedidoRead)
def update_pedido(
    id_pedido: int,
    pedido_in: PedidoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if pedido_in.id_direccion is not None:
        validate_key_exist(db, pedido_in.id_direccion, "direccion", "id_direccion")

    if pedido_in.id_estado is not None:
        validate_key_exist(db, pedido_in.id_estado, "estado", "id_estado")

    if pedido_in.id_cliente is not None:
        validate_key_exist(db, pedido_in.id_cliente, "cliente", "id_cliente")

    pedido = crud_pedidos.update_pedido(
        db,
        id_pedido,
        pedido_in.id_direccion,
        pedido_in.id_estado,
        pedido_in.id_cliente,
        pedido_in.fecha_entrega,
        pedido_in.fecha_pedido,
        pedido_in.comentario,
        pedido_in.tipo_entrega,
        pedido_in.subtotal,
        pedido_in.total
    )

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")

    return pedido


@router.delete("/{id_pedido}", response_model=PedidoRead)
def delete_pedido(
    id_pedido: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    pedido = crud_pedidos.delete_pedido(db, id_pedido)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido