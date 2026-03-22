from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.schemas.cliente import ClienteCreate, ClienteRead, ClienteUpdate
from app.crud import cliente as crud_cliente
from app.core.roles import Roles


router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
def create_cliente(
    cliente_in: ClienteCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_cliente.create_cliente(
        db,
        cliente_in.nombre,
        cliente_in.apellido,
        cliente_in.telefono
    )


@router.get("/", response_model=list[ClienteRead])
def read_clientes(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud_cliente.get_clientes(db)


@router.get("/{id_cliente}", response_model=ClienteRead)
def read_cliente(
    id_cliente: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    cliente = crud_cliente.get_cliente_by_id(db, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.put("/{id_cliente}", response_model=ClienteRead)
def update_cliente(
    id_cliente: int,
    cliente_in: ClienteUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    cliente = crud_cliente.update_cliente(
        db,
        id_cliente,
        cliente_in.nombre,
        cliente_in.apellido,
        cliente_in.telefono
    )
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente


@router.delete("/{id_cliente}", response_model=ClienteRead)
def delete_cliente(
    id_cliente: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    cliente = crud_cliente.delete_cliente(db, id_cliente)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente