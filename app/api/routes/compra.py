from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.compra import CompraCreate, CompraUpdate, CompraOut
from app.crud.compra import (
    create_compra,
    get_compras,
    get_compra_by_id,
    update_compra,
    delete_compra
)

router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=CompraOut, status_code=201)
def crear_compra(
    compra: CompraCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, compra.id_proveedor, "proveedor", "id_proveedor")

    return create_compra(db, compra)


@router.get("/", response_model=list[CompraOut])
def listar_compras(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_compras(db)


@router.get("/{id_compra}", response_model=CompraOut)
def obtener_compra(
    id_compra: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    compra = get_compra_by_id(db, id_compra)

    if not compra:
        raise HTTPException(status_code=404, detail="Compra no encontrada")

    return compra


@router.put("/{id_compra}", response_model=CompraOut)
def actualizar_compra(
    id_compra: int,
    compra: CompraUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if compra.id_proveedor is not None:
        validate_key_exist(db, compra.id_proveedor, "proveedor", "id_proveedor")

    compra_actualizada = update_compra(db, id_compra, compra)

    if not compra_actualizada:
        raise HTTPException(status_code=404, detail="Compra no encontrada")

    return compra_actualizada


@router.delete("/{id_compra}", response_model=CompraOut)
def eliminar_compra(
    id_compra: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    compra_eliminada = delete_compra(db, id_compra)

    if not compra_eliminada:
        raise HTTPException(status_code=404, detail="Compra no encontrada")

    return compra_eliminada