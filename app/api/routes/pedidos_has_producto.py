from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.pedidos_has_producto import (
    PedidosHasProductoCreate,
    PedidosHasProductoUpdate,
    PedidosHasProductoOut
)
from app.crud.pedidos_has_producto import (
    create_pedidos_has_producto,
    get_pedidos_has_producto,
    get_pedidos_has_producto_by_id,
    update_pedidos_has_producto,
    delete_pedidos_has_producto
)

router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=PedidosHasProductoOut, status_code=201)
def crear_pedidos_has_producto(
    pedidos_has_producto: PedidosHasProductoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, pedidos_has_producto.id_pedido, "pedidos", "id_pedido")
    validate_key_exist(db, pedidos_has_producto.id_producto, "producto", "id_producto")

    return create_pedidos_has_producto(db, pedidos_has_producto)


@router.get("/", response_model=list[PedidosHasProductoOut])
def listar_pedidos_has_producto(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_pedidos_has_producto(db)


@router.get("/{id_pedido}/{id_producto}", response_model=PedidosHasProductoOut)
def obtener_pedidos_has_producto(
    id_pedido: int,
    id_producto: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion = get_pedidos_has_producto_by_id(db, id_pedido, id_producto)

    if not relacion:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion


@router.put("/{id_pedido}/{id_producto}", response_model=PedidosHasProductoOut)
def actualizar_pedidos_has_producto(
    id_pedido: int,
    id_producto: int,
    pedidos_has_producto: PedidosHasProductoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if pedidos_has_producto.id_pedido is not None:
        validate_key_exist(db, pedidos_has_producto.id_pedido, "pedidos", "id_pedido")

    if pedidos_has_producto.id_producto is not None:
        validate_key_exist(db, pedidos_has_producto.id_producto, "producto", "id_producto")

    relacion_actualizada = update_pedidos_has_producto(
        db,
        id_pedido,
        id_producto,
        pedidos_has_producto
    )

    if not relacion_actualizada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_actualizada


@router.delete("/{id_pedido}/{id_producto}", response_model=PedidosHasProductoOut)
def eliminar_pedidos_has_producto(
    id_pedido: int,
    id_producto: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion_eliminada = delete_pedidos_has_producto(db, id_pedido, id_producto)

    if not relacion_eliminada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_eliminada