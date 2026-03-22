from sqlalchemy.orm import Session
from sqlalchemy import text

from app.schemas.materia_prima import MateriaPrimaCreate, MateriaPrimaUpdate


def create_materia_prima(db: Session, materia_prima: MateriaPrimaCreate):
    query = text("""
        INSERT INTO public.materia_prima (
            id_unidad,
            descripcion,
            precio_unitario,
            minimo,
            maximo,
            stock_actual,
            imagen,
            activo
        )
        VALUES (
            :id_unidad,
            :descripcion,
            :precio_unitario,
            :minimo,
            :maximo,
            :stock_actual,
            :imagen,
            :activo
        )
        RETURNING id_materia, id_unidad, descripcion, precio_unitario, minimo, maximo, stock_actual, imagen, activo
    """)

    result = db.execute(query, {
        "id_unidad": materia_prima.id_unidad,
        "descripcion": materia_prima.descripcion,
        "precio_unitario": materia_prima.precio_unitario,
        "minimo": materia_prima.minimo,
        "maximo": materia_prima.maximo,
        "stock_actual": materia_prima.stock_actual,
        "imagen": materia_prima.imagen,
        "activo": materia_prima.activo
    })

    db.commit()
    return result.mappings().first()


def get_materia_primas(db: Session):
    query = text("""
        SELECT id_materia, id_unidad, descripcion, precio_unitario, minimo, maximo, stock_actual, imagen, activo
        FROM public.materia_prima
        ORDER BY id_materia
    """)

    result = db.execute(query)
    return result.mappings().all()


def get_materia_prima_by_id(db: Session, id_materia: int):
    query = text("""
        SELECT id_materia, id_unidad, descripcion, precio_unitario, minimo, maximo, stock_actual, imagen, activo
        FROM public.materia_prima
        WHERE id_materia = :id_materia
    """)

    result = db.execute(query, {
        "id_materia": id_materia
    })

    return result.mappings().first()


def update_materia_prima(db: Session, id_materia: int, materia_prima: MateriaPrimaUpdate):
    current_materia_prima = get_materia_prima_by_id(db, id_materia)

    if not current_materia_prima:
        return None

    query = text("""
        UPDATE public.materia_prima
        SET id_unidad = :id_unidad,
            descripcion = :descripcion,
            precio_unitario = :precio_unitario,
            minimo = :minimo,
            maximo = :maximo,
            stock_actual = :stock_actual,
            imagen = :imagen,
            activo = :activo
        WHERE id_materia = :id_materia
        RETURNING id_materia, id_unidad, descripcion, precio_unitario, minimo, maximo, stock_actual, imagen, activo
    """)

    result = db.execute(query, {
        "id_materia": id_materia,
        "id_unidad": materia_prima.id_unidad if materia_prima.id_unidad is not None else current_materia_prima["id_unidad"],
        "descripcion": materia_prima.descripcion if materia_prima.descripcion is not None else current_materia_prima["descripcion"],
        "precio_unitario": materia_prima.precio_unitario if materia_prima.precio_unitario is not None else current_materia_prima["precio_unitario"],
        "minimo": materia_prima.minimo if materia_prima.minimo is not None else current_materia_prima["minimo"],
        "maximo": materia_prima.maximo if materia_prima.maximo is not None else current_materia_prima["maximo"],
        "stock_actual": materia_prima.stock_actual if materia_prima.stock_actual is not None else current_materia_prima["stock_actual"],
        "imagen": materia_prima.imagen if materia_prima.imagen is not None else current_materia_prima["imagen"],
        "activo": materia_prima.activo if materia_prima.activo is not None else current_materia_prima["activo"]
    })

    db.commit()
    return result.mappings().first()


def update_materia_prima_imagen(db: Session, id_materia: int, imagen: str | None):
    query = text("""
        UPDATE public.materia_prima
        SET imagen = :imagen
        WHERE id_materia = :id_materia
        RETURNING id_materia, id_unidad, descripcion, precio_unitario, minimo, maximo, stock_actual, imagen, activo
    """)

    result = db.execute(query, {
        "id_materia": id_materia,
        "imagen": imagen
    })

    db.commit()
    return result.mappings().first()


def delete_materia_prima(db: Session, id_materia: int):
    query = text("""
        DELETE FROM public.materia_prima
        WHERE id_materia = :id_materia
        RETURNING id_materia, id_unidad, descripcion, precio_unitario, minimo, maximo, stock_actual, imagen, activo
    """)

    result = db.execute(query, {
        "id_materia": id_materia
    })

    deleted_materia_prima = result.mappings().first()
    db.commit()
    return deleted_materia_prima