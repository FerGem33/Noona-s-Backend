from sqlalchemy import text
from sqlalchemy.orm import Session


def get_estados(db: Session):
    result = db.execute(
        text("""
            SELECT id_estado, descripcion
            FROM estado
            ORDER BY id_estado
        """)
    )
    return result.mappings().all()


def get_estado_by_id(db: Session, id_estado: int):
    result = db.execute(
        text("""
            SELECT id_estado, descripcion
            FROM estado
            WHERE id_estado = :id_estado
        """),
        {"id_estado": id_estado}
    )
    return result.mappings().first()


def create_estado(db: Session, descripcion: str):
    result = db.execute(
        text("""
            INSERT INTO estado (descripcion)
            VALUES (:descripcion)
            RETURNING id_estado, descripcion
        """),
        {"descripcion": descripcion}
    )
    db.commit()
    return result.mappings().first()


def update_estado(db: Session, id_estado: int, descripcion: str | None = None):
    current = get_estado_by_id(db, id_estado)
    if not current:
        return None

    new_descripcion = descripcion if descripcion is not None else current["descripcion"]

    result = db.execute(
        text("""
            UPDATE estado
            SET descripcion = :descripcion
            WHERE id_estado = :id_estado
            RETURNING id_estado, descripcion
        """),
        {
            "id_estado": id_estado,
            "descripcion": new_descripcion
        }
    )
    db.commit()
    return result.mappings().first()


def delete_estado(db: Session, id_estado: int):
    result = db.execute(
        text("""
            DELETE FROM estado
            WHERE id_estado = :id_estado
            RETURNING id_estado, descripcion
        """),
        {"id_estado": id_estado}
    )
    db.commit()
    return result.mappings().first()