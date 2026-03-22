from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.core.roles import Roles
from app.schemas.proveedor import ProveedorCreate, ProveedorUpdate, ProveedorOut
from app.crud.proveedor import (
    create_proveedor,
    get_proveedores,
    get_proveedor_by_id,
    update_proveedor,
    delete_proveedor
)

router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=ProveedorOut, status_code=201)
def crear_proveedor(
    proveedor: ProveedorCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return create_proveedor(db, proveedor)


@router.get("/", response_model=list[ProveedorOut])
def listar_proveedores(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_proveedores(db)


@router.get("/{id_proveedor}", response_model=ProveedorOut)
def obtener_proveedor(
    id_proveedor: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    proveedor = get_proveedor_by_id(db, id_proveedor)

    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return proveedor


@router.put("/{id_proveedor}", response_model=ProveedorOut)
def actualizar_proveedor(
    id_proveedor: int,
    proveedor: ProveedorUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    proveedor_actualizado = update_proveedor(db, id_proveedor, proveedor)

    if not proveedor_actualizado:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return proveedor_actualizado


@router.delete("/{id_proveedor}", response_model=ProveedorOut)
def eliminar_proveedor(
    id_proveedor: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    proveedor_eliminado = delete_proveedor(db, id_proveedor)

    if not proveedor_eliminado:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    return proveedor_eliminado