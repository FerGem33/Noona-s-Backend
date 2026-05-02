from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.compra import CompraCreate, CompraUpdate


def create_compra(db: Session, compra: CompraCreate, do_commit=True):
    query = text("""
        INSERT INTO public.compra (id_proveedor, fecha, total)
        VALUES (:id_proveedor, :fecha, :total)
        RETURNING id_compra, id_proveedor, fecha, total, efectuada
    """)

    result = db.execute(query, {
        "id_proveedor": compra.id_proveedor,
        "fecha": compra.fecha,
        "total": compra.total
    })

    if do_commit: db.commit()
    return result.mappings().first()


def get_compras(db: Session):
    query = text("""
        SELECT id_compra, id_proveedor, fecha, total, efectuada
        FROM public.compra
        ORDER BY id_compra
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_compra_by_id(db: Session, id_compra: int):
    query = text("""
        SELECT id_compra, id_proveedor, fecha, total, efectuada
        FROM public.compra
        WHERE id_compra = :id_compra
    """)

    result = db.execute(query, {
        "id_compra": id_compra
    })

    return result.mappings().first()


def update_compra(db: Session, id_compra: int, compra: CompraUpdate):
    current_compra = get_compra_by_id(db, id_compra)

    if not current_compra:
        return None

    query = text("""
        UPDATE public.compra
        SET id_proveedor = :id_proveedor,
            fecha = :fecha,
            total = :total
        WHERE id_compra = :id_compra
        RETURNING id_compra, id_proveedor, fecha, total, efectuada
    """)

    result = db.execute(query, {
        "id_compra": id_compra,
        "id_proveedor": compra.id_proveedor if compra.id_proveedor is not None else current_compra["id_proveedor"],
        "fecha": compra.fecha if compra.fecha is not None else current_compra["fecha"],
        "total": compra.total if compra.total is not None else current_compra["total"]
    })

    db.commit()
    return result.mappings().first()


def delete_compra(db: Session, id_compra: int):
    query = text("""
         DELETE
         FROM public.materia_prima_compra
         WHERE id_compra = :id_compra
         """)
    db.execute(query, {"id_compra": id_compra})

    query = text("""
        DELETE FROM public.compra
        WHERE id_compra = :id_compra
        RETURNING id_compra, id_proveedor, fecha, total, efectuada
    """)

    result = db.execute(query, {
        "id_compra": id_compra
    })

    deleted_compra = result.mappings().first()
    db.commit()
    return deleted_compra