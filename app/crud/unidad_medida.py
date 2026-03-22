from sqlalchemy import text
from sqlalchemy.orm import Session


def get_unidades(db: Session):
    result = db.execute(
        text("""
            SELECT id_unidad, descripcion, abreviatura
            FROM unidad_medida
            ORDER BY id_unidad
        """)
    )
    return result.mappings().all()


def get_unidad_by_id(db: Session, id_unidad: int):
    result = db.execute(
        text("""
            SELECT id_unidad, descripcion, abreviatura
            FROM unidad_medida
            WHERE id_unidad = :id_unidad
        """),
        {"id_unidad": id_unidad}
    )
    return result.mappings().first()


def create_unidad(db: Session, descripcion: str, abreviatura: str):
    result = db.execute(
        text("""
            INSERT INTO unidad_medida (descripcion, abreviatura)
            VALUES (:descripcion, :abreviatura)
            RETURNING id_unidad, descripcion, abreviatura
        """),
        {
            "descripcion": descripcion,
            "abreviatura": abreviatura
        }
    )
    db.commit()
    return result.mappings().first()


def update_unidad(
    db: Session,
    id_unidad: int,
    descripcion: str | None = None,
    abreviatura: str | None = None
):
    current = get_unidad_by_id(db, id_unidad)
    if not current:
        return None

    new_descripcion = descripcion if descripcion is not None else current["descripcion"]
    new_abreviatura = abreviatura if abreviatura is not None else current["abreviatura"]

    result = db.execute(
        text("""
            UPDATE unidad_medida
            SET descripcion = :descripcion,
                abreviatura = :abreviatura
            WHERE id_unidad = :id_unidad
            RETURNING id_unidad, descripcion, abreviatura
        """),
        {
            "id_unidad": id_unidad,
            "descripcion": new_descripcion,
            "abreviatura": new_abreviatura
        }
    )
    db.commit()
    return result.mappings().first()


def delete_unidad(db: Session, id_unidad: int):
    result = db.execute(
        text("""
            DELETE FROM unidad_medida
            WHERE id_unidad = :id_unidad
            RETURNING id_unidad, descripcion, abreviatura
        """),
        {"id_unidad": id_unidad}
    )
    db.commit()
    return result.mappings().first()