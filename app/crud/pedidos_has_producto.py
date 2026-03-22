from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.pedidos_has_producto import (
    PedidosHasProductoCreate,
    PedidosHasProductoUpdate
)


def create_pedidos_has_producto(db: Session, pedidos_has_producto: PedidosHasProductoCreate):
    query = text("""
        INSERT INTO public.pedidos_has_producto (
            id_pedido,
            id_producto,
            cantidad,
            precio_diseño,
            precio_envio
        )
        VALUES (
            :id_pedido,
            :id_producto,
            :cantidad,
            :precio_diseno,
            :precio_envio
        )
        RETURNING id_pedido, id_producto, cantidad, precio_diseño, precio_envio
    """)

    result = db.execute(query, {
        "id_pedido": pedidos_has_producto.id_pedido,
        "id_producto": pedidos_has_producto.id_producto,
        "cantidad": pedidos_has_producto.cantidad,
        "precio_diseno": pedidos_has_producto.precio_diseno,
        "precio_envio": pedidos_has_producto.precio_envio
    })

    db.commit()
    return result.mappings().first()


def get_pedidos_has_producto(db: Session):
    query = text("""
        SELECT id_pedido, id_producto, cantidad, precio_diseño, precio_envio
        FROM public.pedidos_has_producto
        ORDER BY id_pedido, id_producto
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_pedidos_has_producto_by_id(db: Session, id_pedido: int, id_producto: int):
    query = text("""
        SELECT id_pedido, id_producto, cantidad, precio_diseño, precio_envio
        FROM public.pedidos_has_producto
        WHERE id_pedido = :id_pedido AND id_producto = :id_producto
    """)

    result = db.execute(query, {
        "id_pedido": id_pedido,
        "id_producto": id_producto
    })

    return result.mappings().first()


def update_pedidos_has_producto(
    db: Session,
    id_pedido: int,
    id_producto: int,
    pedidos_has_producto: PedidosHasProductoUpdate
):
    current_relacion = get_pedidos_has_producto_by_id(db, id_pedido, id_producto)

    if not current_relacion:
        return None

    new_id_pedido = (
        pedidos_has_producto.id_pedido
        if pedidos_has_producto.id_pedido is not None
        else current_relacion["id_pedido"]
    )
    new_id_producto = (
        pedidos_has_producto.id_producto
        if pedidos_has_producto.id_producto is not None
        else current_relacion["id_producto"]
    )
    new_cantidad = (
        pedidos_has_producto.cantidad
        if pedidos_has_producto.cantidad is not None
        else current_relacion["cantidad"]
    )
    new_precio_diseno = (
        pedidos_has_producto.precio_diseno
        if pedidos_has_producto.precio_diseno is not None
        else current_relacion["precio_diseño"]
    )
    new_precio_envio = (
        pedidos_has_producto.precio_envio
        if pedidos_has_producto.precio_envio is not None
        else current_relacion["precio_envio"]
    )

    query = text("""
        UPDATE public.pedidos_has_producto
        SET id_pedido = :new_id_pedido,
            id_producto = :new_id_producto,
            cantidad = :cantidad,
            precio_diseño = :precio_diseno,
            precio_envio = :precio_envio
        WHERE id_pedido = :id_pedido AND id_producto = :id_producto
        RETURNING id_pedido, id_producto, cantidad, precio_diseño, precio_envio
    """)

    result = db.execute(query, {
        "id_pedido": id_pedido,
        "id_producto": id_producto,
        "new_id_pedido": new_id_pedido,
        "new_id_producto": new_id_producto,
        "cantidad": new_cantidad,
        "precio_diseno": new_precio_diseno,
        "precio_envio": new_precio_envio
    })

    db.commit()
    return result.mappings().first()


def delete_pedidos_has_producto(db: Session, id_pedido: int, id_producto: int):
    query = text("""
        DELETE FROM public.pedidos_has_producto
        WHERE id_pedido = :id_pedido AND id_producto = :id_producto
        RETURNING id_pedido, id_producto, cantidad, precio_diseño, precio_envio
    """)

    result = db.execute(query, {
        "id_pedido": id_pedido,
        "id_producto": id_producto
    })

    deleted_relacion = result.mappings().first()
    db.commit()
    return deleted_relacion