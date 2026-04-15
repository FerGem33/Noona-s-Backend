from sqlalchemy import text
from sqlalchemy.orm import Session


def get_pedidos(db: Session):
    result = db.execute(
        text("""
            SELECT p.id_pedido, p.id_direccion, p.id_estado, p.id_cliente, 
                   d.descripcion AS direccion, e.descripcion AS estado, c.nombre||' '||c.apellido AS cliente,
                   p.fecha_entrega, p.fecha_pedido, p.comentario, p.tipo_entrega, p.subtotal, p.total
            FROM pedidos p
            JOIN direccion d ON p.id_direccion = d.id_direccion
            JOIN estado e ON p.id_estado = e.id_estado
            JOIN cliente c ON p.id_cliente = c.id_cliente
            ORDER BY id_pedido
        """)
    )
    return result.mappings().all()


def get_pedido_by_id(db: Session, id_pedido: int):
    result = db.execute(
        text("""
            SELECT p.id_pedido, p.id_direccion, p.id_estado, p.id_cliente, 
                   d.descripcion AS direccion, e.descripcion AS estado, c.nombre||' '||c.apellido AS cliente,
                   p.fecha_entrega, p.fecha_pedido, p.comentario, p.tipo_entrega, p.subtotal, p.total
            FROM pedidos p
            JOIN direccion d ON p.id_direccion = d.id_direccion
            JOIN estado e ON p.id_estado = e.id_estado
            JOIN cliente c ON p.id_cliente = c.id_cliente
            WHERE id_pedido = :id_pedido
        """),
        {"id_pedido": id_pedido}
    )
    return result.mappings().first()


def create_pedido(
    db: Session,
    id_direccion: int,
    id_estado: int,
    id_cliente: int,
    fecha_entrega,
    fecha_pedido,
    comentario,
    tipo_entrega,
    subtotal,
    total
):
    result = db.execute(
        text("""
            INSERT INTO pedidos (
                id_direccion, id_estado, id_cliente,
                fecha_entrega, fecha_pedido,
                comentario, tipo_entrega,
                subtotal, total
            )
            VALUES (
                :id_direccion, :id_estado, :id_cliente,
                :fecha_entrega, :fecha_pedido,
                :comentario, :tipo_entrega,
                :subtotal, :total
            )
            RETURNING *
        """),
        {
            "id_direccion": id_direccion,
            "id_estado": id_estado,
            "id_cliente": id_cliente,
            "fecha_entrega": fecha_entrega,
            "fecha_pedido": fecha_pedido,
            "comentario": comentario,
            "tipo_entrega": tipo_entrega,
            "subtotal": subtotal,
            "total": total
        }
    )
    db.commit()
    return result.mappings().first()


def update_pedido(
    db: Session,
    id_pedido: int,
    id_direccion=None,
    id_estado=None,
    id_cliente=None,
    fecha_entrega=None,
    fecha_pedido=None,
    comentario=None,
    tipo_entrega=None,
    subtotal=None,
    total=None
):
    current = get_pedido_by_id(db, id_pedido)
    if not current:
        return None

    result = db.execute(
        text("""
            UPDATE pedidos
            SET id_direccion = :id_direccion,
                id_estado = :id_estado,
                id_cliente = :id_cliente,
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
            "id_direccion": id_direccion if id_direccion is not None else current["id_direccion"],
            "id_estado": id_estado if id_estado is not None else current["id_estado"],
            "id_cliente": id_cliente if id_cliente is not None else current["id_cliente"],
            "fecha_entrega": fecha_entrega if fecha_entrega is not None else current["fecha_entrega"],
            "fecha_pedido": fecha_pedido if fecha_pedido is not None else current["fecha_pedido"],
            "comentario": comentario if comentario is not None else current["comentario"],
            "tipo_entrega": tipo_entrega if tipo_entrega is not None else current["tipo_entrega"],
            "subtotal": subtotal if subtotal is not None else current["subtotal"],
            "total": total if total is not None else current["total"],
        }
    )
    db.commit()
    return result.mappings().first()


def delete_pedido(db: Session, id_pedido: int):
    result = db.execute(
        text("""
            DELETE FROM pedidos
            WHERE id_pedido = :id_pedido
            RETURNING *
        """),
        {"id_pedido": id_pedido}
    )
    db.commit()
    return result.mappings().first()