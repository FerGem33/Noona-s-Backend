from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.cotizacion import (
    CotizacionCreate,
    CotizacionUpdate
)


def create_cotizacion(db: Session, cotizacion: CotizacionCreate):
    query = text("""
        INSERT INTO public.cotizacion (precio_envio)
        VALUES (:precio_envio)
        RETURNING id_cotizacion, precio_envio
    """)

    result = db.execute(query, {
        "precio_envio": cotizacion.precio_envio
    })

    cot_row = result.mappings().first()
    id_cotizacion = cot_row["id_cotizacion"]

    for detalle in cotizacion.detalles:
        db.execute(text("""
                INSERT INTO public.detalles_cotizacion (
                    producto_id_producto,
                    cotizacion_id_cotizacion,
                    cantidad,
                    precio_diseño
                )
                VALUES (
                    :id_producto,
                    :id_cotizacion,
                    :cantidad,
                    :precio
                )
            """), {
            "id_producto": detalle.producto_id_producto,
            "id_cotizacion": id_cotizacion,
            "cantidad": detalle.cantidad,
            "precio": detalle.precio_disenio
        })

    db.commit()

    return get_cotizacion_by_id(db, id_cotizacion)


def get_cotizacion(db: Session):
    cotizaciones = db.execute(text("""
        SELECT id_cotizacion, precio_envio
        FROM cotizacion
    """)).mappings().all()

    result = []

    for cot in cotizaciones:
        detalles = db.execute(text("""
            SELECT producto_id_producto, cantidad, precio_diseño
            FROM detalles_cotizacion
            WHERE cotizacion_id_cotizacion = :id
        """), {"id": cot["id_cotizacion"]}).mappings().all()

        result.append({
            **cot,
            "detalles": detalles
        })

    return result


def get_cotizacion_by_id(db: Session, id_cotizacion: int):
    cot = db.execute(text("""
        SELECT id_cotizacion, precio_envio
        FROM cotizacion
        WHERE id_cotizacion = :id
    """), {"id": id_cotizacion}).mappings().first()

    if not cot:
        return None

    detalles = db.execute(text("""
        SELECT producto_id_producto, cantidad, precio_diseño
        FROM detalles_cotizacion
        WHERE cotizacion_id_cotizacion = :id
    """), {"id": id_cotizacion}).mappings().all()

    return {
        **cot,
        "detalles": detalles
    }


def update_cotizacion(db: Session, id_cotizacion: int, cotizacion: CotizacionUpdate):
    existing = get_cotizacion_by_id(db, id_cotizacion)
    if not existing:
        return None

    if cotizacion.precio_envio is not None:
        db.execute(text("""
            UPDATE cotizacion
            SET precio_envio = :precio
            WHERE id_cotizacion = :id
        """), {
            "precio": cotizacion.precio_envio,
            "id": id_cotizacion
        })

    if cotizacion.detalles is not None:
        # delete old
        db.execute(text("""
            DELETE FROM detalles_cotizacion
            WHERE cotizacion_id_cotizacion = :id
        """), {"id": id_cotizacion})

        # insert new
        for d in cotizacion.detalles:
            db.execute(text("""
                INSERT INTO detalles_cotizacion (
                    producto_id_producto,
                    cotizacion_id_cotizacion,
                    cantidad,
                    precio_diseño
                )
                VALUES (:prod, :cot, :cant, :precio)
            """), {
                "prod": d.producto_id_producto,
                "cot": id_cotizacion,
                "cant": d.cantidad,
                "precio": d.precio_disenio
            })

    db.commit()
    return get_cotizacion_by_id(db, id_cotizacion)


def delete_cotizacion(db: Session, id_cotizacion: int):
    existing = get_cotizacion_by_id(db, id_cotizacion)
    if not existing:
        return None

    db.execute(text("""
        DELETE FROM detalles_cotizacion
        WHERE cotizacion_id_cotizacion = :id
    """), {"id": id_cotizacion})

    db.execute(text("""
        DELETE FROM cotizacion
        WHERE id_cotizacion = :id
    """), {"id": id_cotizacion})

    db.commit()
    return existing