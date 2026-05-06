from sqlalchemy import text
from sqlalchemy.orm import Session
from app.schemas.pedidos import PedidoCreate, PedidoUpdate


def get_pedidos(db: Session):
    pedidos = db.execute(
        text("""
            SELECT p.id_pedido, p.id_direccion, p.id_estado, p.id_cliente, p.id_cotizacion,
                   d.descripcion AS direccion, e.descripcion AS estado, c.nombre||' '||c.apellido AS cliente,
                   p.fecha_entrega, p.fecha_pedido, p.comentario, p.tipo_entrega, p.subtotal, p.total
            FROM pedidos p
            JOIN direccion d ON p.id_direccion = d.id_direccion
            JOIN estado e ON p.id_estado = e.id_estado
            JOIN cliente c ON p.id_cliente = c.id_cliente
            ORDER BY id_pedido
        """)
    ).mappings().all()

    result = []

    for pedido in pedidos:
        productos = db.execute(
            text("""
            SELECT dc.id_producto, pr.descripcion AS producto, dc.cantidad, dc.precio_disenio
            FROM pedidos pe
            JOIN cotizacion c ON pe.id_cotizacion = c.id_cotizacion
            JOIN detalles_cotizacion dc ON c.id_cotizacion = dc.id_cotizacion
            JOIN producto pr ON dc.id_producto = pr.id_producto
            WHERE pe.id_pedido = :id_pedido        
        """), {"id_pedido": pedido["id_pedido"]}).mappings().all()

        result.append({
            **pedido,
            "productos": productos
        })


    return result


def get_pedido_by_id(db: Session, id_pedido: int):
    pedido = db.execute(
        text("""
                SELECT p.id_pedido, p.id_direccion, p.id_estado, p.id_cliente, p.id_cotizacion,
                       d.descripcion AS direccion, e.descripcion AS estado, c.nombre||' '||c.apellido AS cliente,
                       p.fecha_entrega, p.fecha_pedido, p.comentario, p.tipo_entrega, p.subtotal, p.total
                FROM pedidos p
                JOIN direccion d ON p.id_direccion = d.id_direccion
                JOIN estado e ON p.id_estado = e.id_estado
                JOIN cliente c ON p.id_cliente = c.id_cliente
                WHERE p.id_pedido = :id_pedido
            """),
        {"id_pedido": id_pedido}
    ).mappings().first()

    if not pedido:
        return None

    productos = db.execute(
        text("""
            SELECT dc.id_producto, pr.descripcion AS producto, dc.cantidad, dc.precio_disenio
            FROM pedidos pe
            JOIN cotizacion c ON pe.id_cotizacion = c.id_cotizacion
            JOIN detalles_cotizacion dc ON c.id_cotizacion = dc.id_cotizacion
            JOIN producto pr ON dc.id_producto = pr.id_producto
            WHERE pe.id_pedido = :id_pedido        
        """), {"id_pedido": id_pedido}).mappings().all()

    return {
        **pedido,
        "productos": productos
    }


def create_pedido(db: Session, pedido: PedidoCreate):
    result = db.execute(
        text("""
            INSERT INTO pedidos (
                id_direccion, id_estado, id_cliente, id_cotizacion,
                fecha_entrega, fecha_pedido,
                comentario, tipo_entrega,
                subtotal, total
            )
            VALUES (
                :id_direccion, :id_estado, :id_cliente, :id_cotizacion,
                :fecha_entrega, :fecha_pedido,
                :comentario, :tipo_entrega,
                :subtotal, :total
            )
            RETURNING *
        """),
        {
            "id_direccion": pedido.id_direccion,
            "id_estado": pedido.id_estado,
            "id_cliente": pedido.id_cliente,
            "id_cotizacion": pedido.id_cotizacion,
            "fecha_entrega": pedido.fecha_entrega,
            "fecha_pedido": pedido.fecha_pedido,
            "comentario": pedido.comentario,
            "tipo_entrega": pedido.tipo_entrega,
            "subtotal": pedido.subtotal,
            "total": pedido.total
        }
    )

    db.commit()
    created = result.mappings().first()

    return get_pedido_by_id(db, created["id_pedido"])


def update_pedido(db: Session, id_pedido: int, pedido: PedidoUpdate):
    current = get_pedido_by_id(db, id_pedido)

    if not current:
        return None

    result = db.execute(
        text("""
            UPDATE pedidos
            SET id_direccion = :id_direccion,
                id_estado = :id_estado,
                id_cliente = :id_cliente,
                id_cotizacion = :id_cotizacion,
                fecha_entrega = :fecha_entrega,
                fecha_pedido = :fecha_pedido,
                comentario = :comentario,
                tipo_entrega = :tipo_entrega,
                subtotal = :subtotal,
                total = :total
            WHERE id_pedido = :id_pedido
            RETURNING *
        """),
        {
            "id_pedido": id_pedido,
            "id_direccion": pedido.id_direccion if pedido.id_direccion is not None else current["id_direccion"],
            "id_estado": pedido.id_estado if pedido.id_estado is not None else current["id_estado"],
            "id_cliente": pedido.id_cliente if pedido.id_cliente is not None else current["id_cliente"],
            "id_cotizacion": pedido.id_cotizacion if pedido.id_cotizacion is not None else current["id_cotizacion"],
            "fecha_entrega": pedido.fecha_entrega if pedido.fecha_entrega is not None else current["fecha_entrega"],
            "fecha_pedido": pedido.fecha_pedido if pedido.fecha_pedido is not None else current["fecha_pedido"],
            "comentario": pedido.comentario if pedido.comentario is not None else current["comentario"],
            "tipo_entrega": pedido.tipo_entrega if pedido.tipo_entrega is not None else current["tipo_entrega"],
            "subtotal": pedido.subtotal if pedido.subtotal is not None else current["subtotal"],
            "total": pedido.total if pedido.total is not None else current["total"],
        }
    )

    db.commit()
    updated = result.mappings().first()

    return get_pedido_by_id(db, updated["id_pedido"])


def delete_pedido(db: Session, id_pedido: int):
    pedido = get_pedido_by_id(db, id_pedido)

    if not pedido:
        return None

    db.execute(
        text("""
                DELETE FROM pago
                WHERE id_pedido = :id_pedido
            """),
        {"id_pedido": id_pedido}
    )
    db.execute(
        text("""
                DELETE FROM usuario_has_pedidos
                WHERE id_pedido = :id_pedido
            """),
        {"id_pedido": id_pedido}
    )
    db.execute(
        text("""
            DELETE FROM pedidos
            WHERE id_pedido = :id_pedido
        """),
        {"id_pedido": id_pedido}
    )
    db.commit()

    return pedido