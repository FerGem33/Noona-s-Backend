from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.receta_materia_prima import (
    RecetaMateriaPrimaCreate,
    RecetaMateriaPrimaUpdate,
    RecetaMateriaPrimaOut
)
from app.crud.receta_materia_prima import (
    create_receta_materia_prima,
    get_receta_materia_prima,
    get_receta_materia_prima_by_id,
    update_receta_materia_prima,
    delete_receta_materia_prima
)

router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=RecetaMateriaPrimaOut, status_code=201)
def crear_receta_materia_prima(
    receta_materia_prima: RecetaMateriaPrimaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, receta_materia_prima.id_receta, "receta", "id_receta")
    validate_key_exist(db, receta_materia_prima.id_materia, "materia_prima", "id_materia")

    return create_receta_materia_prima(db, receta_materia_prima)


@router.get("/", response_model=list[RecetaMateriaPrimaOut])
def listar_receta_materia_prima(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_receta_materia_prima(db)


@router.get("/{id_receta}/{id_materia}", response_model=RecetaMateriaPrimaOut)
def obtener_receta_materia_prima(
    id_receta: int,
    id_materia: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion = get_receta_materia_prima_by_id(db, id_receta, id_materia)

    if not relacion:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion


@router.put("/{id_receta}/{id_materia}", response_model=RecetaMateriaPrimaOut)
def actualizar_receta_materia_prima(
    id_receta: int,
    id_materia: int,
    receta_materia_prima: RecetaMateriaPrimaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if receta_materia_prima.id_receta is not None:
        validate_key_exist(db, receta_materia_prima.id_receta, "receta", "id_receta")

    if receta_materia_prima.id_materia is not None:
        validate_key_exist(db, receta_materia_prima.id_materia, "materia_prima", "id_materia")

    relacion_actualizada = update_receta_materia_prima(
        db,
        id_receta,
        id_materia,
        receta_materia_prima
    )

    if not relacion_actualizada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_actualizada


@router.delete("/{id_receta}/{id_materia}", response_model=RecetaMateriaPrimaOut)
def eliminar_receta_materia_prima(
    id_receta: int,
    id_materia: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion_eliminada = delete_receta_materia_prima(db, id_receta, id_materia)

    if not relacion_eliminada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_eliminada