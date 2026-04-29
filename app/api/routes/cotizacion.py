from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.cotizacion import (
    CotizacionCreate,
    CotizacionUpdate,
    CotizacionOut
)
from app.crud.cotizacion import (
    create_cotizacion,
    get_cotizacion,
    get_cotizacion_by_id,
    update_cotizacion,
    delete_cotizacion
)

router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=CotizacionOut, status_code=201)
def crear_cotizacion(
    cotizacion: CotizacionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, cotizacion.id_pedido, "pedidos", "id_pedido")
    validate_key_exist(db, cotizacion.id_producto, "producto", "id_producto")

    return create_cotizacion(db, cotizacion)


@router.get("/", response_model=list[CotizacionOut])
def listar_cotizacion(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_cotizacion(db)


@router.get("/{id_pedido}/{id_producto}", response_model=CotizacionOut)
def obtener_cotizacion(
    id_pedido: int,
    id_producto: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion = get_cotizacion_by_id(db, id_pedido, id_producto)

    if not relacion:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion


@router.put("/{id_pedido}/{id_producto}", response_model=CotizacionOut)
def actualizar_cotizacion(
    id_pedido: int,
    id_producto: int,
    cotizacion: CotizacionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if cotizacion.id_pedido is not None:
        validate_key_exist(db, cotizacion.id_pedido, "pedidos", "id_pedido")

    if cotizacion.id_producto is not None:
        validate_key_exist(db, cotizacion.id_producto, "producto", "id_producto")

    relacion_actualizada = update_cotizacion(
        db,
        id_pedido,
        id_producto,
        cotizacion
    )

    if not relacion_actualizada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_actualizada


@router.delete("/{id_pedido}/{id_producto}", response_model=CotizacionOut)
def eliminar_cotizacion(
    id_pedido: int,
    id_producto: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion_eliminada = delete_cotizacion(db, id_pedido, id_producto)

    if not relacion_eliminada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_eliminada