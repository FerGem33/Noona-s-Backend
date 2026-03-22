from sqlalchemy import text
from sqlalchemy.orm import Session


def get_clientes(db: Session):
    result = db.execute(
        text("""
            SELECT id_cliente, nombre, apellido, telefono
            FROM cliente
            ORDER BY id_cliente
        """)
    )
    return result.mappings().all()


def get_cliente_by_id(db: Session, id_cliente: int):
    result = db.execute(
        text("""
            SELECT id_cliente, nombre, apellido, telefono
            FROM cliente
            WHERE id_cliente = :id_cliente
        """),
        {"id_cliente": id_cliente}
    )
    return result.mappings().first()


def create_cliente(db: Session, nombre: str, apellido: str, telefono: str):
    result = db.execute(
        text("""
            INSERT INTO cliente (nombre, apellido, telefono)
            VALUES (:nombre, :apellido, :telefono)
            RETURNING id_cliente, nombre, apellido, telefono
        """),
        {
            "nombre": nombre,
            "apellido": apellido,
            "telefono": telefono
        }
    )
    db.commit()
    return result.mappings().first()


def update_cliente(
    db: Session,
    id_cliente: int,
    nombre: str | None = None,
    apellido: str | None = None,
    telefono: str | None = None
):
    current = get_cliente_by_id(db, id_cliente)
    if not current:
        return None

    new_nombre = nombre if nombre is not None else current["nombre"]
    new_apellido = apellido if apellido is not None else current["apellido"]
    new_telefono = telefono if telefono is not None else current["telefono"]

    result = db.execute(
        text("""
            UPDATE cliente
            SET nombre = :nombre,
                apellido = :apellido,
                telefono = :telefono
            WHERE id_cliente = :id_cliente
            RETURNING id_cliente, nombre, apellido, telefono
        """),
        {
            "id_cliente": id_cliente,
            "nombre": new_nombre,
            "apellido": new_apellido,
            "telefono": new_telefono
        }
    )
    db.commit()
    return result.mappings().first()


def delete_cliente(db: Session, id_cliente: int):
    result = db.execute(
        text("""
            DELETE FROM cliente
            WHERE id_cliente = :id_cliente
            RETURNING id_cliente, nombre, apellido, telefono
        """),
        {"id_cliente": id_cliente}
    )
    db.commit()
    return result.mappings().first()