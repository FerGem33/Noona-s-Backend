from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.receta import RecetaCreate, RecetaUpdate, RecetaOut
from app.crud.receta import (
    create_receta,
    get_recetas,
    get_receta_by_id,
    update_receta,
    delete_receta
)

router = APIRouter(prefix="/recetas", tags=["Receta"])

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=RecetaOut, status_code=201)
def crear_receta(
    receta: RecetaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, receta.id_usuario, "usuario", "id_usuario")
    return create_receta(db, receta)


@router.get("/", response_model=list[RecetaOut])
def listar_recetas(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_recetas(db)


@router.get("/{id_receta}", response_model=RecetaOut)
def obtener_receta(
    id_receta: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    receta = get_receta_by_id(db, id_receta)

    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    return receta


@router.put("/{id_receta}", response_model=RecetaOut)
def actualizar_receta(
    id_receta: int,
    receta: RecetaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, id_receta, "receta", "id_receta")
    if receta.id_usuario is not None: validate_key_exist(db, receta.id_usuario, "usuario", "id_usuario")
    receta_actualizada = update_receta(db, id_receta, receta)

    if not receta_actualizada:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    return receta_actualizada


@router.delete("/{id_receta}", response_model=RecetaOut)
def eliminar_receta(
    id_receta: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, id_receta, "receta", "id_receta")
    receta_eliminada = delete_receta(db, id_receta)

    if not receta_eliminada:
        raise HTTPException(status_code=404, detail="Receta no encontrada")

    return receta_eliminada