from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.materia_prima_compra import (
    MateriaPrimaCompraCreate,
    MateriaPrimaCompraUpdate
)


def create_materia_prima_compra(db: Session, materia_prima_compra: MateriaPrimaCompraCreate):
    query = text("""
        INSERT INTO public.materia_prima_compra (
            id_materia,
            id_compra,
            cantidad,
            precio_individual
        )
        VALUES (
            :id_materia,
            :id_compra,
            :cantidad,
            :precio_individual
        )
        RETURNING id_materia, id_compra, cantidad, precio_individual
    """)

    result = db.execute(query, {
        "id_materia": materia_prima_compra.id_materia,
        "id_compra": materia_prima_compra.id_compra,
        "cantidad": materia_prima_compra.cantidad,
        "precio_individual": materia_prima_compra.precio_individual
    })

    db.commit()
    return result.mappings().first()


def get_materia_prima_compra(db: Session):
    query = text("""
        SELECT id_materia, id_compra, cantidad, precio_individual
        FROM public.materia_prima_compra
        ORDER BY id_materia, id_compra
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_materia_prima_compra_by_id(db: Session, id_materia: int, id_compra: int):
    query = text("""
        SELECT id_materia, id_compra, cantidad, precio_individual
        FROM public.materia_prima_compra
        WHERE id_materia = :id_materia AND id_compra = :id_compra
    """)

    result = db.execute(query, {
        "id_materia": id_materia,
        "id_compra": id_compra
    })

    return result.mappings().first()


def update_materia_prima_compra(
    db: Session,
    id_materia: int,
    id_compra: int,
    materia_prima_compra: MateriaPrimaCompraUpdate
):
    current_relacion = get_materia_prima_compra_by_id(db, id_materia, id_compra)

    if not current_relacion:
        return None

    new_id_materia = (
        materia_prima_compra.id_materia
        if materia_prima_compra.id_materia is not None
        else current_relacion["id_materia"]
    )
    new_id_compra = (
        materia_prima_compra.id_compra
        if materia_prima_compra.id_compra is not None
        else current_relacion["id_compra"]
    )
    new_cantidad = (
        materia_prima_compra.cantidad
        if materia_prima_compra.cantidad is not None
        else current_relacion["cantidad"]
    )
    new_precio_individual = (
        materia_prima_compra.precio_individual
        if materia_prima_compra.precio_individual is not None
        else current_relacion["precio_individual"]
    )

    query = text("""
        UPDATE public.materia_prima_compra
        SET id_materia = :new_id_materia,
            id_compra = :new_id_compra,
            cantidad = :cantidad,
            precio_individual = :precio_individual
        WHERE id_materia = :id_materia AND id_compra = :id_compra
        RETURNING id_materia, id_compra, cantidad, precio_individual
    """)

    result = db.execute(query, {
        "id_materia": id_materia,
        "id_compra": id_compra,
        "new_id_materia": new_id_materia,
        "new_id_compra": new_id_compra,
        "cantidad": new_cantidad,
        "precio_individual": new_precio_individual
    })

    db.commit()
    return result.mappings().first()


def delete_materia_prima_compra(db: Session, id_materia: int, id_compra: int):
    query = text("""
        DELETE FROM public.materia_prima_compra
        WHERE id_materia = :id_materia AND id_compra = :id_compra
        RETURNING id_materia, id_compra, cantidad, precio_individual
    """)

    result = db.execute(query, {
        "id_materia": id_materia,
        "id_compra": id_compra
    })

    deleted_relacion = result.mappings().first()
    db.commit()
    return deleted_relacion