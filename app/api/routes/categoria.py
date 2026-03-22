from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles
from app.core.roles import Roles
from app.schemas.categoria import CategoriaCreate, CategoriaUpdate, CategoriaOut
from app.crud.categoria import (
    create_categoria,
    get_categorias,
    get_categoria_by_id,
    update_categoria,
    delete_categoria
)

router = APIRouter(prefix="/categorias", tags=["Categoria"])

authorized_roles = [Roles.ADMIN, Roles.DUENA]


@router.post("/", response_model=CategoriaOut, status_code=201)
def crear_categoria(
    categoria: CategoriaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return create_categoria(db, categoria)


@router.get("/", response_model=list[CategoriaOut])
def listar_categorias(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    return get_categorias(db)


@router.get("/{id_categoria}", response_model=CategoriaOut)
def obtener_categoria(
    id_categoria: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    categoria = get_categoria_by_id(db, id_categoria)

    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categoria


@router.put("/{id_categoria}", response_model=CategoriaOut)
def actualizar_categoria(
    id_categoria: int,
    categoria: CategoriaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    categoria_actualizada = update_categoria(db, id_categoria, categoria)

    if not categoria_actualizada:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categoria_actualizada


@router.delete("/{id_categoria}", response_model=CategoriaOut)
def eliminar_categoria(
    id_categoria: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    categoria_eliminada = delete_categoria(db, id_categoria)

    if not categoria_eliminada:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")

    return categoria_eliminada