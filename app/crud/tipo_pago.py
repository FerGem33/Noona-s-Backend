from sqlalchemy import text
from sqlalchemy.orm import Session


def get_tipos_pago(db: Session):
    result = db.execute(
        text("""
            SELECT id_tipo_pago, descripcion
            FROM tipo_pago
            ORDER BY id_tipo_pago
        """)
    )
    return result.mappings().all()


def get_tipo_pago_by_id(db: Session, id_tipo_pago: int):
    result = db.execute(
        text("""
            SELECT id_tipo_pago, descripcion
            FROM tipo_pago
            WHERE id_tipo_pago = :id_tipo_pago
        """),
        {"id_tipo_pago": id_tipo_pago}
    )
    return result.mappings().first()


def create_tipo_pago(db: Session, descripcion: str):
    result = db.execute(
        text("""
            INSERT INTO tipo_pago (descripcion)
            VALUES (:descripcion)
            RETURNING id_tipo_pago, descripcion
        """),
        {"descripcion": descripcion}
    )
    db.commit()
    return result.mappings().first()


def update_tipo_pago(db: Session, id_tipo_pago: int, descripcion: str | None = None):
    current = get_tipo_pago_by_id(db, id_tipo_pago)
    if not current:
        return None

    new_descripcion = descripcion if descripcion is not None else current["descripcion"]

    result = db.execute(
        text("""
            UPDATE tipo_pago
            SET descripcion = :descripcion
            WHERE id_tipo_pago = :id_tipo_pago
            RETURNING id_tipo_pago, descripcion
        """),
        {
            "id_tipo_pago": id_tipo_pago,
            "descripcion": new_descripcion
        }
    )
    db.commit()
    return result.mappings().first()


def delete_tipo_pago(db: Session, id_tipo_pago: int):
    result = db.execute(
        text("""
            DELETE FROM tipo_pago
            WHERE id_tipo_pago = :id_tipo_pago
            RETURNING id_tipo_pago, descripcion
        """),
        {"id_tipo_pago": id_tipo_pago}
    )
    db.commit()
    return result.mappings().first()