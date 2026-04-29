from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.cotizacion import (
    CotizacionCreate,
    CotizacionUpdate
)


def create_cotizacion(db: Session, cotizacion: CotizacionCreate):
    query = text("""
        INSERT INTO public.cotizacion (
            id_pedido,
            id_producto,
            id_estado
            cantidad,
            precio_disenio,
            precio_envio
        )
        VALUES (
            :id_pedido,
            :id_producto,
            :id_estado,
            :cantidad,
            :precio_disenio,
            :precio_envio
        )
        RETURNING id_pedido, id_producto, id_estado, cantidad, precio_disenio, precio_envio
    """)

    result = db.execute(query, {
        "id_pedido": cotizacion.id_pedido,
        "id_producto": cotizacion.id_producto,
        "id_estado": cotizacion.id_estado,
        "cantidad": cotizacion.cantidad,
        "precio_disenio": cotizacion.precio_disenio,
        "precio_envio": cotizacion.precio_envio
    })

    db.commit()
    return result.mappings().first()


def get_cotizacion(db: Session):
    query = text("""
        SELECT id_pedido, id_producto, id_estado, cantidad, precio_disenio, precio_envio
        FROM public.cotizacion
        ORDER BY id_pedido, id_producto
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_cotizacion_by_id(db: Session, id_pedido: int, id_producto: int):
    query = text("""
        SELECT id_pedido, id_producto, id_estado, cantidad, precio_disenio, precio_envio
        FROM public.cotizacion
        WHERE id_pedido = :id_pedido AND id_producto = :id_producto
    """)

    result = db.execute(query, {
        "id_pedido": id_pedido,
        "id_producto": id_producto
    })

    return result.mappings().first()


def update_cotizacion(
    db: Session,
    id_pedido: int,
    id_producto: int,
    cotizacion: CotizacionUpdate
):
    current_relacion = get_cotizacion_by_id(db, id_pedido, id_producto)

    if not current_relacion:
        return None

    new_id_pedido = (
        cotizacion.id_pedido
        if cotizacion.id_pedido is not None
        else current_relacion["id_pedido"]
    )
    new_id_producto = (
        cotizacion.id_producto
        if cotizacion.id_producto is not None
        else current_relacion["id_producto"]
    )
    new_id_estado = (
        cotizacion.id_estado
        if cotizacion.id_estado is not None
        else current_relacion["id_estado"]
    )
    new_cantidad = (
        cotizacion.cantidad
        if cotizacion.cantidad is not None
        else current_relacion["cantidad"]
    )
    new_precio_disenio = (
        cotizacion.precio_disenio
        if cotizacion.precio_disenio is not None
        else current_relacion["precio_disenio"]
    )
    new_precio_envio = (
        cotizacion.precio_envio
        if cotizacion.precio_envio is not None
        else current_relacion["precio_envio"]
    )

    query = text("""
        UPDATE public.cotizacion
        SET id_pedido = :new_id_pedido,
            id_producto = :new_id_producto,
            id_estado = :id_estado,
            cantidad = :cantidad,
            precio_disenio = :precio_disenio,
            precio_envio = :precio_envio
        WHERE id_pedido = :id_pedido AND id_producto = :id_producto
        RETURNING id_pedido, id_producto, id_estado, cantidad, precio_disenio, precio_envio
    """)

    result = db.execute(query, {
        "id_pedido": id_pedido,
        "id_producto": id_producto,
        "id_estado": new_id_estado,
        "new_id_pedido": new_id_pedido,
        "new_id_producto": new_id_producto,
        "cantidad": new_cantidad,
        "precio_disenio": new_precio_disenio,
        "precio_envio": new_precio_envio
    })

    db.commit()
    return result.mappings().first()


def delete_cotizacion(db: Session, id_pedido: int, id_producto: int):
    query = text("""
        DELETE FROM public.cotizacion
        WHERE id_pedido = :id_pedido AND id_producto = :id_producto
        RETURNING id_pedido, id_producto, id_estado, cantidad, precio_disenio, precio_envio
    """)

    result = db.execute(query, {
        "id_pedido": id_pedido,
        "id_producto": id_producto
    })

    deleted_relacion = result.mappings().first()
    db.commit()
    return deleted_relacion