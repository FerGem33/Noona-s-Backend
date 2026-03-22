from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.receta import RecetaCreate, RecetaUpdate


def create_receta(db: Session, receta: RecetaCreate):
    query = text("""
        INSERT INTO public.receta (descripcion)
        VALUES (:descripcion)
        RETURNING id_receta, descripcion
    """)

    result = db.execute(query, {
        "descripcion": receta.descripcion
    })

    db.commit()
    return result.mappings().first()


def get_recetas(db: Session):
    query = text("""
        SELECT id_receta, descripcion
        FROM public.receta
        ORDER BY id_receta
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_receta_by_id(db: Session, id_receta: int):
    query = text("""
        SELECT id_receta, descripcion
        FROM public.receta
        WHERE id_receta = :id_receta
    """)

    result = db.execute(query, {
        "id_receta": id_receta
    })

    return result.mappings().first()


def update_receta(db: Session, id_receta: int, receta: RecetaUpdate):
    current_receta = get_receta_by_id(db, id_receta)

    if not current_receta:
        return None

    query = text("""
        UPDATE public.receta
        SET descripcion = :descripcion
        WHERE id_receta = :id_receta
        RETURNING id_receta, descripcion
    """)

    result = db.execute(query, {
        "id_receta": id_receta,
        "descripcion": receta.descripcion if receta.descripcion is not None else current_receta["descripcion"]
    })

    db.commit()
    return result.mappings().first()


def delete_receta(db: Session, id_receta: int):
    query = text("""
        DELETE FROM public.receta
        WHERE id_receta = :id_receta
        RETURNING id_receta, descripcion
    """)

    result = db.execute(query, {
        "id_receta": id_receta
    })

    deleted_receta = result.mappings().first()
    db.commit()
    return deleted_receta