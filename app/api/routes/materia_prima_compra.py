from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.materia_prima_compra import (
    MateriaPrimaCompraCreate,
    MateriaPrimaCompraUpdate,
    MateriaPrimaCompraOut
)
from app.crud.materia_prima_compra import (
    create_materia_prima_compra,
    get_materia_prima_compra,
    get_materia_prima_compra_by_id,
    update_materia_prima_compra,
    delete_materia_prima_compra
)

router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=MateriaPrimaCompraOut, status_code=201)
def crear_materia_prima_compra(
    materia_prima_compra: MateriaPrimaCompraCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, materia_prima_compra.id_materia, "materia_prima", "id_materia")
    validate_key_exist(db, materia_prima_compra.id_compra, "compra", "id_compra")

    return create_materia_prima_compra(db, materia_prima_compra)


@router.get("/", response_model=list[MateriaPrimaCompraOut])
def listar_materia_prima_compra(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_materia_prima_compra(db)


@router.get("/{id_materia}/{id_compra}", response_model=MateriaPrimaCompraOut)
def obtener_materia_prima_compra(
    id_materia: int,
    id_compra: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion = get_materia_prima_compra_by_id(db, id_materia, id_compra)

    if not relacion:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion


@router.put("/{id_materia}/{id_compra}", response_model=MateriaPrimaCompraOut)
def actualizar_materia_prima_compra(
    id_materia: int,
    id_compra: int,
    materia_prima_compra: MateriaPrimaCompraUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if materia_prima_compra.id_materia is not None:
        validate_key_exist(db, materia_prima_compra.id_materia, "materia_prima", "id_materia")

    if materia_prima_compra.id_compra is not None:
        validate_key_exist(db, materia_prima_compra.id_compra, "compra", "id_compra")

    relacion_actualizada = update_materia_prima_compra(
        db,
        id_materia,
        id_compra,
        materia_prima_compra
    )

    if not relacion_actualizada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_actualizada


@router.delete("/{id_materia}/{id_compra}", response_model=MateriaPrimaCompraOut)
def eliminar_materia_prima_compra(
    id_materia: int,
    id_compra: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    relacion_eliminada = delete_materia_prima_compra(db, id_materia, id_compra)

    if not relacion_eliminada:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return relacion_eliminada