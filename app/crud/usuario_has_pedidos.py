from sqlalchemy import text
from sqlalchemy.orm import Session


def get_usuario_pedidos(db: Session):
    result = db.execute(
        text("""
            SELECT id_usuario, id_pedido
            FROM usuario_has_pedidos
            ORDER BY id_usuario, id_pedido
        """)
    )
    return result.mappings().all()


def get_usuario_pedido(db: Session, id_usuario: int, id_pedido: int):
    result = db.execute(
        text("""
            SELECT id_usuario, id_pedido
            FROM usuario_has_pedidos
            WHERE id_usuario = :id_usuario AND id_pedido = :id_pedido
        """),
        {"id_usuario": id_usuario, "id_pedido": id_pedido}
    )
    return result.mappings().first()


def create_usuario_pedido(db: Session, id_usuario: int, id_pedido: int):
    result = db.execute(
        text("""
            INSERT INTO usuario_has_pedidos (id_usuario, id_pedido)
            VALUES (:id_usuario, :id_pedido)
            RETURNING id_usuario, id_pedido
        """),
        {
            "id_usuario": id_usuario,
            "id_pedido": id_pedido
        }
    )
    db.commit()
    return result.mappings().first()


def update_usuario_pedido(
    db: Session,
    id_usuario: int,
    id_pedido: int,
    new_id_usuario: int | None = None,
    new_id_pedido: int | None = None
):
    current = get_usuario_pedido(db, id_usuario, id_pedido)
    if not current:
        return None

    final_id_usuario = new_id_usuario if new_id_usuario is not None else current["id_usuario"]
    final_id_pedido = new_id_pedido if new_id_pedido is not None else current["id_pedido"]

    result = db.execute(
        text("""
            UPDATE usuario_has_pedidos
            SET id_usuario = :new_id_usuario,
                id_pedido = :new_id_pedido
            WHERE id_usuario = :id_usuario AND id_pedido = :id_pedido
            RETURNING id_usuario, id_pedido
        """),
        {
            "id_usuario": id_usuario,
            "id_pedido": id_pedido,
            "new_id_usuario": final_id_usuario,
            "new_id_pedido": final_id_pedido
        }
    )
    db.commit()
    return result.mappings().first()


def delete_usuario_pedido(db: Session, id_usuario: int, id_pedido: int):
    result = db.execute(
        text("""
            DELETE FROM usuario_has_pedidos
            WHERE id_usuario = :id_usuario AND id_pedido = :id_pedido
            RETURNING id_usuario, id_pedido
        """),
        {"id_usuario": id_usuario, "id_pedido": id_pedido}
    )
    db.commit()
    return result.mappings().first()