from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.direccion import DireccionCreate, DireccionRead, DireccionUpdate
from app.crud import direccion as crud_direccion


router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=DireccionRead, status_code=status.HTTP_201_CREATED)
def create_direccion(
    direccion_in: DireccionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, direccion_in.id_cliente, "cliente", "id_cliente")

    return crud_direccion.create_direccion(
        db,
        direccion_in.id_cliente,
        direccion_in.descripcion
    )


@router.get("/", response_model=list[DireccionRead])
def read_direcciones(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_direccion.get_direcciones(db)


@router.get("/{id_direccion}", response_model=DireccionRead)
def read_direccion(
    id_direccion: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    direccion = crud_direccion.get_direccion_by_id(db, id_direccion)
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return direccion


@router.put("/{id_direccion}", response_model=DireccionRead)
def update_direccion(
    id_direccion: int,
    direccion_in: DireccionUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if direccion_in.id_cliente is not None:
        validate_key_exist(db, direccion_in.id_cliente, "cliente", "id_cliente")

    direccion = crud_direccion.update_direccion(
        db,
        id_direccion,
        direccion_in.id_cliente,
        direccion_in.descripcion
    )
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return direccion


@router.delete("/{id_direccion}", response_model=DireccionRead)
def delete_direccion(
    id_direccion: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    direccion = crud_direccion.delete_direccion(db, id_direccion)
    if not direccion:
        raise HTTPException(status_code=404, detail="Dirección no encontrada")
    return direccion