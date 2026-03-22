from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.usuario_has_pedidos import (
    UsuarioPedidoCreate,
    UsuarioPedidoRead,
    UsuarioPedidoUpdate
)
from app.crud import usuario_has_pedidos as crud


router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=UsuarioPedidoRead, status_code=status.HTTP_201_CREATED)
def create_usuario_pedido(
    data: UsuarioPedidoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, data.id_usuario, "usuario", "id_usuario")
    validate_key_exist(db, data.id_pedido, "pedidos", "id_pedido")

    return crud.create_usuario_pedido(db, data.id_usuario, data.id_pedido)


@router.get("/", response_model=list[UsuarioPedidoRead])
def read_usuario_pedidos(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return crud.get_usuario_pedidos(db)


@router.get("/{id_usuario}/{id_pedido}", response_model=UsuarioPedidoRead)
def read_usuario_pedido(
    id_usuario: int,
    id_pedido: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    result = crud.get_usuario_pedido(db, id_usuario, id_pedido)
    if not result:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")
    return result


@router.put("/{id_usuario}/{id_pedido}", response_model=UsuarioPedidoRead)
def update_usuario_pedido(
    id_usuario: int,
    id_pedido: int,
    data: UsuarioPedidoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if data.id_usuario is not None:
        validate_key_exist(db, data.id_usuario, "usuario", "id_usuario")

    if data.id_pedido is not None:
        validate_key_exist(db, data.id_pedido, "pedidos", "id_pedido")

    result = crud.update_usuario_pedido(
        db,
        id_usuario,
        id_pedido,
        data.id_usuario,
        data.id_pedido
    )

    if not result:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")

    return result


@router.delete("/{id_usuario}/{id_pedido}", response_model=UsuarioPedidoRead)
def delete_usuario_pedido(
    id_usuario: int,
    id_pedido: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    result = crud.delete_usuario_pedido(db, id_usuario, id_pedido)
    if not result:
        raise HTTPException(status_code=404, detail="Relacion no encontrada")
    return result