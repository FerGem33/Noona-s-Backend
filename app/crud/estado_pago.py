from sqlalchemy import text
from sqlalchemy.orm import Session


def get_estados_pago(db: Session):
    result = db.execute(
        text("""
            SELECT id_estado_pago, descripcion
            FROM estado_pago
            ORDER BY id_estado_pago
        """)
    )
    return result.mappings().all()


def get_estado_pago_by_id(db: Session, id_estado_pago: int):
    result = db.execute(
        text("""
            SELECT id_estado_pago, descripcion
            FROM estado_pago
            WHERE id_estado_pago = :id_estado_pago
        """),
        {"id_estado_pago": id_estado_pago}
    )
    return result.mappings().first()


def create_estado_pago(db: Session, descripcion: str):
    result = db.execute(
        text("""
            INSERT INTO estado_pago (descripcion)
            VALUES (:descripcion)
            RETURNING id_estado_pago, descripcion
        """),
        {"descripcion": descripcion}
    )
    db.commit()
    return result.mappings().first()


def update_estado_pago(db: Session, id_estado_pago: int, descripcion: str | None = None):
    current = get_estado_pago_by_id(db, id_estado_pago)
    if not current:
        return None

    new_descripcion = descripcion if descripcion is not None else current["descripcion"]

    result = db.execute(
        text("""
            UPDATE estado_pago
            SET descripcion = :descripcion
            WHERE id_estado_pago = :id_estado_pago
            RETURNING id_estado_pago, descripcion
        """),
        {
            "id_estado_pago": id_estado_pago,
            "descripcion": new_descripcion
        }
    )
    db.commit()
    return result.mappings().first()


def delete_estado_pago(db: Session, id_estado_pago: int):
    result = db.execute(
        text("""
            DELETE FROM estado_pago
            WHERE id_estado_pago = :id_estado_pago
            RETURNING id_estado_pago, descripcion
        """),
        {"id_estado_pago": id_estado_pago}
    )
    db.commit()
    return result.mappings().first()