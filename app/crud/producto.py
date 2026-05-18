from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.producto import ProductoCreate, ProductoUpdate


def create_producto(db: Session, producto: ProductoCreate):
    query = text("""
        INSERT INTO public.producto (
            id_categoria,
            id_receta,
            descripcion,
            precio_unitario,
            imagen,
            activo
        )
        VALUES (
            :id_categoria,
            :id_receta,
            :descripcion,
            :precio_unitario,
            :imagen,
            :activo
        )
        RETURNING id_producto, id_categoria, id_receta, descripcion, precio_unitario, imagen, activo
    """)

    result = db.execute(query, {
        "id_categoria": producto.id_categoria,
        "id_receta": producto.id_receta,
        "descripcion": producto.descripcion,
        "precio_unitario": producto.precio_unitario,
        "imagen": producto.imagen,
        "activo": producto.activo
    })

    db.commit()
    return result.mappings().first()


def get_productos(db: Session):
    query = text("""
        SELECT id_producto, id_categoria, id_receta, descripcion, precio_unitario, imagen, activo
        FROM public.producto
        WHERE activo = TRUE
        ORDER BY id_producto
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_producto_by_id(db: Session, id_producto: int):
    query = text("""
        SELECT id_producto, id_categoria, id_receta, descripcion, precio_unitario, imagen, activo
        FROM public.producto
        WHERE id_producto = :id_producto AND activo = TRUE
    """)

    result = db.execute(query, {
        "id_producto": id_producto
    })

    return result.mappings().first()


def update_producto(db: Session, id_producto: int, producto: ProductoUpdate):
    current_producto = get_producto_by_id(db, id_producto)

    if not current_producto:
        return None

    query = text("""
        UPDATE public.producto
        SET id_categoria = :id_categoria,
            id_receta = :id_receta,
            descripcion = :descripcion,
            precio_unitario = :precio_unitario,
            imagen = :imagen,
            activo = :activo
        WHERE id_producto = :id_producto
        RETURNING id_producto, id_categoria, id_receta, descripcion, precio_unitario, imagen, activo
    """)

    result = db.execute(query, {
        "id_producto": id_producto,
        "id_categoria": producto.id_categoria if producto.id_categoria is not None else current_producto["id_categoria"],
        "id_receta": producto.id_receta if producto.id_receta is not None else current_producto["id_receta"],
        "descripcion": producto.descripcion if producto.descripcion is not None else current_producto["descripcion"],
        "precio_unitario": producto.precio_unitario if producto.precio_unitario is not None else current_producto["precio_unitario"],
        "imagen": producto.imagen if producto.imagen is not None else current_producto["imagen"],
        "activo": producto.activo if producto.activo is not None else current_producto["activo"]
    })

    db.commit()
    return result.mappings().first()


def update_producto_imagen(db: Session, id_producto: int, imagen: str | None):
    query = text("""
        UPDATE public.producto
        SET imagen = :imagen
        WHERE id_producto = :id_producto
        RETURNING id_producto, id_categoria, id_receta, descripcion, precio_unitario, imagen, activo
    """)

    result = db.execute(query, {
        "id_producto": id_producto,
        "imagen": imagen
    })

    db.commit()
    return result.mappings().first()


def delete_producto(db: Session, id_producto: int):
    query = text("""
        UPDATE producto
        SET activo = FALSE
        WHERE id_producto = :id_producto
        RETURNING id_producto, id_categoria, id_receta, descripcion, precio_unitario, imagen, activo
    """)

    result = db.execute(query, {
        "id_producto": id_producto
    })

    deleted_producto = result.mappings().first()
    db.commit()
    return deleted_producto