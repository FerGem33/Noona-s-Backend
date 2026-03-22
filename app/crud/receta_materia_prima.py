from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.receta_materia_prima import (
    RecetaMateriaPrimaCreate,
    RecetaMateriaPrimaUpdate
)


def create_receta_materia_prima(db: Session, receta_materia_prima: RecetaMateriaPrimaCreate):
    query = text("""
        INSERT INTO public.receta_materia_prima (id_receta, id_materia, cantidad)
        VALUES (:id_receta, :id_materia, :cantidad)
        RETURNING id_receta, id_materia, cantidad
    """)

    result = db.execute(query, {
        "id_receta": receta_materia_prima.id_receta,
        "id_materia": receta_materia_prima.id_materia,
        "cantidad": receta_materia_prima.cantidad
    })

    db.commit()
    return result.mappings().first()


def get_receta_materia_prima(db: Session):
    query = text("""
        SELECT id_receta, id_materia, cantidad
        FROM public.receta_materia_prima
        ORDER BY id_receta, id_materia
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_receta_materia_prima_by_id(db: Session, id_receta: int, id_materia: int):
    query = text("""
        SELECT id_receta, id_materia, cantidad
        FROM public.receta_materia_prima
        WHERE id_receta = :id_receta AND id_materia = :id_materia
    """)

    result = db.execute(query, {
        "id_receta": id_receta,
        "id_materia": id_materia
    })

    return result.mappings().first()


def update_receta_materia_prima(
    db: Session,
    id_receta: int,
    id_materia: int,
    receta_materia_prima: RecetaMateriaPrimaUpdate
):
    current_relacion = get_receta_materia_prima_by_id(db, id_receta, id_materia)

    if not current_relacion:
        return None

    new_id_receta = (
        receta_materia_prima.id_receta
        if receta_materia_prima.id_receta is not None
        else current_relacion["id_receta"]
    )
    new_id_materia = (
        receta_materia_prima.id_materia
        if receta_materia_prima.id_materia is not None
        else current_relacion["id_materia"]
    )
    new_cantidad = (
        receta_materia_prima.cantidad
        if receta_materia_prima.cantidad is not None
        else current_relacion["cantidad"]
    )

    query = text("""
        UPDATE public.receta_materia_prima
        SET id_receta = :new_id_receta,
            id_materia = :new_id_materia,
            cantidad = :cantidad
        WHERE id_receta = :id_receta AND id_materia = :id_materia
        RETURNING id_receta, id_materia, cantidad
    """)

    result = db.execute(query, {
        "id_receta": id_receta,
        "id_materia": id_materia,
        "new_id_receta": new_id_receta,
        "new_id_materia": new_id_materia,
        "cantidad": new_cantidad
    })

    db.commit()
    return result.mappings().first()


def delete_receta_materia_prima(db: Session, id_receta: int, id_materia: int):
    query = text("""
        DELETE FROM public.receta_materia_prima
        WHERE id_receta = :id_receta AND id_materia = :id_materia
        RETURNING id_receta, id_materia, cantidad
    """)

    result = db.execute(query, {
        "id_receta": id_receta,
        "id_materia": id_materia
    })

    deleted_relacion = result.mappings().first()
    db.commit()
    return deleted_relacion