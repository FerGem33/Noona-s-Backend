from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.categoria import CategoriaCreate, CategoriaUpdate


def create_categoria(db: Session, categoria: CategoriaCreate):
    query = text("""
        INSERT INTO public.categoria (descripcion)
        VALUES (:descripcion)
        RETURNING id_categoria, descripcion
    """)

    result = db.execute(query, {
        "descripcion": categoria.descripcion
    })

    db.commit()
    return result.mappings().first()


def get_categorias(db: Session):
    query = text("""
        SELECT id_categoria, descripcion
        FROM public.categoria
        ORDER BY id_categoria
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_categoria_by_id(db: Session, id_categoria: int):
    query = text("""
        SELECT id_categoria, descripcion
        FROM public.categoria
        WHERE id_categoria = :id_categoria
    """)

    result = db.execute(query, {
        "id_categoria": id_categoria
    })

    return result.mappings().first()


def update_categoria(db: Session, id_categoria: int, categoria: CategoriaUpdate):
    current_categoria = get_categoria_by_id(db, id_categoria)

    if not current_categoria:
        return None

    query = text("""
        UPDATE public.categoria
        SET descripcion = :descripcion
        WHERE id_categoria = :id_categoria
        RETURNING id_categoria, descripcion
    """)

    result = db.execute(query, {
        "id_categoria": id_categoria,
        "descripcion": categoria.descripcion if categoria.descripcion is not None else current_categoria["descripcion"]
    })

    db.commit()
    return result.mappings().first()


def delete_categoria(db: Session, id_categoria: int):
    query = text("""
        DELETE FROM public.categoria
        WHERE id_categoria = :id_categoria
        RETURNING id_categoria, descripcion
    """)

    result = db.execute(query, {
        "id_categoria": id_categoria
    })

    deleted_categoria = result.mappings().first()
    db.commit()
    return deleted_categoria