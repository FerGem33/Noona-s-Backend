from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.receta import RecetaCreate, RecetaUpdate


def create_receta(db: Session, receta: RecetaCreate):
    query = text("""
        INSERT INTO public.receta (descripcion, id_usuario)
        VALUES (:descripcion, :id_usuario)
        RETURNING id_receta
    """)

    result = db.execute(query, {
        "descripcion": receta.descripcion,
        "id_usuario": receta.id_usuario
    }).mappings().first()

    db.commit()
    return get_receta_by_id(db, result["id_receta"])


def get_recetas(db: Session):
    query = text("""
        SELECT r.id_receta, r.descripcion, u.id_usuario, u.nombre AS usuario
        FROM public.receta r
        JOIN usuario u ON r.id_usuario = u.id_usuario
        ORDER BY id_receta
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_receta_by_id(db: Session, id_receta: int):
    query = text("""
        SELECT r.id_receta, r.descripcion, u.id_usuario, u.nombre AS usuario
        FROM public.receta r
        JOIN usuario u ON r.id_usuario = u.id_usuario
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
        SET descripcion = :descripcion, id_usuario = :id_usuario
        WHERE id_receta = :id_receta
        RETURNING id_receta
    """)

    result = db.execute(query, {
        "id_receta": id_receta,
        "descripcion": receta.descripcion if receta.descripcion is not None else current_receta["descripcion"],
        "id_usuario": receta.id_usuario if receta.id_usuario is not None else current_receta["id_usuario"]
    }).mappings().first()

    db.commit()
    return get_receta_by_id(db, result["id_receta"])


def delete_receta(db: Session, id_receta: int):
    deleted_receta = get_receta_by_id(db, id_receta)

    query = text("""
        DELETE FROM public.receta
        WHERE id_receta = :id_receta
    """)

    db.execute(query, {
        "id_receta": id_receta
    })
    db.commit()

    return deleted_receta