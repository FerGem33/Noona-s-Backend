from sqlalchemy import text
from sqlalchemy.orm import Session
from app.core.security import hash_password


def get_usuarios(db: Session):
    result = db.execute(
        text("""
            SELECT u.id_usuario, u.nombre, r.id_rol, r.descripcion as rol
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            ORDER BY id_rol
        """)
    )
    return result.mappings().all()


def get_usuario_by_id(db: Session, id_usuario: int):
    result = db.execute(
        text("""
           SELECT u.id_usuario, u.nombre, r.id_rol, r.descripcion as rol
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.id_usuario = :id_usuario
        """),
        {"id_usuario": id_usuario}
    )
    return result.mappings().first()


def get_usuario_by_nombre(db: Session, nombre: str):
    result = db.execute(
        text("""
            SELECT u.id_usuario, u.nombre, r.id_rol, r.descripcion as rol, u.contrasena_hash
            FROM usuario u
            JOIN rol r ON u.id_rol = r.id_rol
            WHERE u.nombre = :nombre
        """),
        {"nombre": nombre}
    )
    return result.mappings().first()


def create_usuario(db: Session, nombre: str, id_rol: int, contrasena: str):
    result = db.execute(
        text("""
            INSERT INTO usuario (nombre, id_rol, contrasena_hash)
            VALUES (:nombre, :id_rol, :contrasena_hash)
            RETURNING id_usuario, nombre, id_rol, (select descripcion as rol from rol where id_rol = :id_rol)
        """),
        {
            "nombre": nombre,
            "id_rol": id_rol,
            "contrasena_hash": hash_password(contrasena)
        }
    )
    db.commit()
    return result.mappings().first()


def update_usuario(db: Session, id_usuario: int, nombre: str=None, id_rol: int=None, contrasena: str=None):
    current = db.execute(
        text("""
            SELECT id_usuario, nombre, id_rol, contrasena_hash
            FROM usuario
            WHERE id_usuario = :id_usuario
        """),
        {"id_usuario": id_usuario}
    ).mappings().first()

    if not current:
        return None

    new_nombre = nombre if nombre is not None else current["nombre"]
    new_id_rol = id_rol if id_rol is not None else current["id_rol"]
    new_contrasena_hash = (
        hash_password(contrasena)
        if contrasena is not None
        else current["contrasena_hash"]
    )

    result = db.execute(
        text("""
            UPDATE usuario
            SET nombre = :nombre,
                id_rol = :id_rol,
                contrasena_hash = :contrasena_hash
            WHERE id_usuario = :id_usuario
            RETURNING id_usuario, nombre, id_rol, (select descripcion as rol from rol where id_rol = :id_rol)
        """),
        {
            "id_usuario": id_usuario,
            "nombre": new_nombre,
            "id_rol": new_id_rol,
            "contrasena_hash": new_contrasena_hash
        }
    )
    db.commit()
    return result.mappings().first()


def delete_usuario(db: Session, id_usuario: int):
    result = db.execute(
        text("""
            DELETE FROM usuario
            WHERE id_usuario = :id_usuario
            RETURNING id_usuario, nombre, id_rol, 
                (select descripcion as rol from rol where id_rol = (select id_rol from usuario where id_usuario = :id_usuario))
        """),
        {"id_usuario": id_usuario}
    )
    db.commit()
    return result.mappings().first()