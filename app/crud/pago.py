from sqlalchemy import text
from sqlalchemy.orm import Session


def get_pagos(db: Session):
    result = db.execute(
        text("""
            SELECT *
            FROM pago
            ORDER BY id_pago
        """)
    )
    return result.mappings().all()


def get_pago_by_id(db: Session, id_pago: int):
    result = db.execute(
        text("""
            SELECT *
            FROM pago
            WHERE id_pago = :id_pago
        """),
        {"id_pago": id_pago}
    )
    return result.mappings().first()


def create_pago(
    db: Session,
    id_pedido,
    id_estado_pago,
    id_tipo_pago,
    anticipo,
    monto,
    fecha
):
    result = db.execute(
        text("""
            INSERT INTO pago (
                id_pedido,
                id_estado_pago,
                id_tipo_pago,
                anticipo,
                monto,
                fecha
            )
            VALUES (
                :id_pedido,
                :id_estado_pago,
                :id_tipo_pago,
                :anticipo,
                :monto,
                :fecha
            )
            RETURNING *
        """),
        {
            "id_pedido": id_pedido,
            "id_estado_pago": id_estado_pago,
            "id_tipo_pago": id_tipo_pago,
            "anticipo": anticipo,
            "monto": monto,
            "fecha": fecha
        }
    )
    db.commit()
    return result.mappings().first()


def update_pago(
    db: Session,
    id_pago: int,
    id_pedido=None,
    id_estado_pago=None,
    id_tipo_pago=None,
    anticipo=None,
    monto=None,
    fecha=None
):
    current = get_pago_by_id(db, id_pago)
    if not current:
        return None

    result = db.execute(
        text("""
            UPDATE pago
            SET id_pedido = :id_pedido,
                id_estado_pago = :id_estado_pago,
                id_tipo_pago = :id_tipo_pago,
                anticipo = :anticipo,
                monto = :monto,
                fecha = :fecha
            WHERE id_pago = :id_pago
            RETURNING *
        """),
        {
            "id_pago": id_pago,
            "id_pedido": id_pedido if id_pedido is not None else current["id_pedido"],
            "id_estado_pago": id_estado_pago if id_estado_pago is not None else current["id_estado_pago"],
            "id_tipo_pago": id_tipo_pago if id_tipo_pago is not None else current["id_tipo_pago"],
            "anticipo": anticipo if anticipo is not None else current["anticipo"],
            "monto": monto if monto is not None else current["monto"],
            "fecha": fecha if fecha is not None else current["fecha"],
        }
    )
    db.commit()
    return result.mappings().first()


def delete_pago(db: Session, id_pago: int):
    result = db.execute(
        text("""
            DELETE FROM pago
            WHERE id_pago = :id_pago
            RETURNING *
        """),
        {"id_pago": id_pago}
    )
    db.commit()
    return result.mappings().first()