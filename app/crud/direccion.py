from sqlalchemy import text
from sqlalchemy.orm import Session


def get_direcciones(db: Session):
    result = db.execute(
        text("""
            SELECT id_direccion, id_cliente, descripcion
            FROM direccion
            ORDER BY id_direccion
        """)
    )
    return result.mappings().all()


def get_direccion_by_id(db: Session, id_direccion: int):
    result = db.execute(
        text("""
            SELECT id_direccion, id_cliente, descripcion
            FROM direccion
            WHERE id_direccion = :id_direccion
        """),
        {"id_direccion": id_direccion}
    )
    return result.mappings().first()


def create_direccion(db: Session, id_cliente: int, descripcion: str):
    result = db.execute(
        text("""
            INSERT INTO direccion (id_cliente, descripcion)
            VALUES (:id_cliente, :descripcion)
            RETURNING id_direccion, id_cliente, descripcion
        """),
        {
            "id_cliente": id_cliente,
            "descripcion": descripcion
        }
    )
    db.commit()
    return result.mappings().first()


def update_direccion(
    db: Session,
    id_direccion: int,
    id_cliente: int | None = None,
    descripcion: str | None = None
):
    current = get_direccion_by_id(db, id_direccion)
    if not current:
        return None

    new_id_cliente = id_cliente if id_cliente is not None else current["id_cliente"]
    new_descripcion = descripcion if descripcion is not None else current["descripcion"]

    result = db.execute(
        text("""
            UPDATE direccion
            SET id_cliente = :id_cliente,
                descripcion = :descripcion
            WHERE id_direccion = :id_direccion
            RETURNING id_direccion, id_cliente, descripcion
        """),
        {
            "id_direccion": id_direccion,
            "id_cliente": new_id_cliente,
            "descripcion": new_descripcion
        }
    )
    db.commit()
    return result.mappings().first()


def delete_direccion(db: Session, id_direccion: int):
    result = db.execute(
        text("""
            DELETE FROM direccion
            WHERE id_direccion = :id_direccion
            RETURNING id_direccion, id_cliente, descripcion
        """),
        {"id_direccion": id_direccion}
    )
    db.commit()
    return result.mappings().first()