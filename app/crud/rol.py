from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session


def get_roles(db: Session):
    result = db.execute(
        text("""
            SELECT id_rol, descripcion
            FROM rol
            WHERE estado_rol = TRUE
            ORDER BY id_rol
        """)
    )
    return result.mappings().all()


def get_rol_by_id(db: Session, id_rol: int):
    result = db.execute(
        text("""
            SELECT id_rol, descripcion
            FROM rol
            WHERE id_rol = :id_rol AND estado_rol = TRUE
        """),
        {"id_rol": id_rol}
    )
    return result.mappings().first()


def get_rol_by_descripcion(db: Session, descripcion: str):
    result = db.execute(
        text("""
            SELECT id_rol, descripcion
            FROM rol
            WHERE LOWER(descripcion) = LOWER(:descripcion)
        """),
        {"descripcion": descripcion}
    )
    return result.mappings().first()


def create_rol(db: Session, descripcion: str = None):
    existing = get_rol_by_descripcion(db, descripcion)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un rol con esa descripcion"
        )

    result = db.execute(
        text("""
            INSERT INTO rol (descripcion)
            VALUES (:descripcion)
            RETURNING id_rol, descripcion
        """),
        {"descripcion": descripcion}
    )
    db.commit()
    return result.mappings().first()


def update_rol(db: Session, id_rol: int, descripcion: str = None):
    current = get_rol_by_id(db, id_rol)
    if not current:
        return None

    new_descripcion = descripcion if descripcion is not None else current["descripcion"]

    existing = get_rol_by_descripcion(db, new_descripcion)
    if existing and existing["id_rol"] != id_rol:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Ya existe un rol con esa descripcion"
        )

    result = db.execute(
        text("""
            UPDATE rol
            SET descripcion = :descripcion
            WHERE id_rol = :id_rol
            RETURNING id_rol, descripcion
        """),
        {
            "id_rol": id_rol,
            "descripcion": new_descripcion
        }
    )
    db.commit()
    return result.mappings().first()


def delete_rol(db: Session, id_rol: int):
    current = get_rol_by_id(db, id_rol)
    if not current:
        return None

    try:
        result = db.execute(
            text("""
                UPDATE rol
                SET estado_rol = FALSE
                WHERE id_rol = :id_rol
                RETURNING id_rol, descripcion
            """),
            {"id_rol": id_rol}
        )
        db.commit()
        return result.mappings().first()
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="No se puede eliminar el rol porque esta siendo usado por otros registros"
        )