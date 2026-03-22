from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate


def create_proveedor(db: Session, proveedor: ProveedorCreate):
    query = text("""
        INSERT INTO public.proveedor (descripcion, direccion, contacto)
        VALUES (:descripcion, :direccion, :contacto)
        RETURNING id_proveedor, descripcion, direccion, contacto
    """)

    result = db.execute(query, {
        "descripcion": proveedor.descripcion,
        "direccion": proveedor.direccion,
        "contacto": proveedor.contacto
    })

    db.commit()
    return result.mappings().first()


def get_proveedores(db: Session):
    query = text("""
        SELECT id_proveedor, descripcion, direccion, contacto
        FROM public.proveedor
        ORDER BY id_proveedor
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_proveedor_by_id(db: Session, id_proveedor: int):
    query = text("""
        SELECT id_proveedor, descripcion, direccion, contacto
        FROM public.proveedor
        WHERE id_proveedor = :id_proveedor
    """)

    result = db.execute(query, {
        "id_proveedor": id_proveedor
    })

    return result.mappings().first()


def update_proveedor(db: Session, id_proveedor: int, proveedor: ProveedorUpdate):
    current_proveedor = get_proveedor_by_id(db, id_proveedor)

    if not current_proveedor:
        return None

    query = text("""
        UPDATE public.proveedor
        SET descripcion = :descripcion,
            direccion = :direccion,
            contacto = :contacto
        WHERE id_proveedor = :id_proveedor
        RETURNING id_proveedor, descripcion, direccion, contacto
    """)

    result = db.execute(query, {
        "id_proveedor": id_proveedor,
        "descripcion": proveedor.descripcion if proveedor.descripcion is not None else current_proveedor["descripcion"],
        "direccion": proveedor.direccion if proveedor.direccion is not None else current_proveedor["direccion"],
        "contacto": proveedor.contacto if proveedor.contacto is not None else current_proveedor["contacto"]
    })

    db.commit()
    return result.mappings().first()


def delete_proveedor(db: Session, id_proveedor: int):
    query = text("""
        DELETE FROM public.proveedor
        WHERE id_proveedor = :id_proveedor
        RETURNING id_proveedor, descripcion, direccion, contacto
    """)

    result = db.execute(query, {
        "id_proveedor": id_proveedor
    })

    deleted_proveedor = result.mappings().first()
    db.commit()
    return deleted_proveedor