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
    for cot in cotizacion.detalles:
        validate_key_exist(db, cot.id_producto, "producto", "id_producto")

    return create_cotizacion(db, cotizacion)


@router.get("/", response_model=list[CotizacionOut])
def listar_cotizacion(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_cotizacion(db)


@router.get("/{id_cotizacion}", response_model=CotizacionOut)
def obtener_cotizacion(
    id_cotizacion: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion = get_cotizacion_by_id(db, id_cotizacion)

    if not relacion:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion


@router.put("/{id_cotizacion}", response_model=CotizacionOut)
def actualizar_cotizacion(
    id_cotizacion: int,
    cotizacion: CotizacionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, id_cotizacion, "cotizacion", "id_cotizacion")
    if cotizacion.detalles is not None:
        for cot in cotizacion.detalles:
            validate_key_exist(db, cot.id_producto, "producto", "id_producto")

    relacion_actualizada = update_cotizacion(
        db,
        id_cotizacion,
        cotizacion
    )

    if not relacion_actualizada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_actualizada


@router.delete("/{id_cotizacion}", response_model=CotizacionOut)
def eliminar_cotizacion(
    id_cotizacion: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion_eliminada = delete_cotizacion(db, id_cotizacion)

    if not relacion_eliminada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_eliminada