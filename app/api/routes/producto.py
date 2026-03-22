from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.crud.producto import (
    create_producto,
    get_productos,
    get_producto_by_id,
    update_producto,
    update_producto_imagen,
    delete_producto
)
from app.schemas.producto import ProductoCreate, ProductoUpdate, ProductoOut
from app.utils.files import build_image_url, delete_file_if_exists, save_image_file

router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


def add_image_url(producto):
    if not producto:
        return None

    producto_dict = dict(producto)
    producto_dict["image_url"] = build_image_url(producto_dict.get("imagen"))
    return producto_dict


def add_image_url_list(productos):
    return [add_image_url(producto) for producto in productos]


@router.post("/", response_model=ProductoOut, status_code=201)
def crear_producto(
    producto: ProductoCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, producto.id_categoria, "categoria", "id_categoria")
    validate_key_exist(db, producto.id_receta, "receta", "id_receta")

    producto_creado = create_producto(db, producto)
    return add_image_url(producto_creado)


@router.get("/", response_model=list[ProductoOut])
def listar_productos(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    productos = get_productos(db)
    return add_image_url_list(productos)


@router.get("/{id_producto}", response_model=ProductoOut)
def obtener_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    producto = get_producto_by_id(db, id_producto)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return add_image_url(producto)


@router.put("/{id_producto}", response_model=ProductoOut)
def actualizar_producto(
    id_producto: int,
    producto: ProductoUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if producto.id_categoria is not None:
        validate_key_exist(db, producto.id_categoria, "categoria", "id_categoria")

    if producto.id_receta is not None:
        validate_key_exist(db, producto.id_receta, "receta", "id_receta")

    producto_actualizado = update_producto(db, id_producto, producto)

    if not producto_actualizado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return add_image_url(producto_actualizado)


@router.delete("/{id_producto}", response_model=ProductoOut)
def eliminar_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    producto_eliminado = delete_producto(db, id_producto)

    if not producto_eliminado:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    if producto_eliminado.get("imagen"):
        delete_file_if_exists(producto_eliminado["imagen"])

    return add_image_url(producto_eliminado)


@router.post("/{id_producto}/imagen", response_model=ProductoOut)
async def subir_imagen_producto(
    id_producto: int,
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    producto = get_producto_by_id(db, id_producto)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    imagen_anterior = producto.get("imagen")
    nueva_imagen = None

    try:
        nueva_imagen = await save_image_file(imagen, "productos")
        producto_actualizado = update_producto_imagen(db, id_producto, nueva_imagen)

        if imagen_anterior and imagen_anterior != nueva_imagen:
            delete_file_if_exists(imagen_anterior)

        return add_image_url(producto_actualizado)

    except Exception:
        if nueva_imagen:
            delete_file_if_exists(nueva_imagen)
        raise


@router.delete("/{id_producto}/imagen", response_model=ProductoOut)
def eliminar_imagen_producto(
    id_producto: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    producto = get_producto_by_id(db, id_producto)

    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    imagen_anterior = producto.get("imagen")
    producto_actualizado = update_producto_imagen(db, id_producto, None)

    if imagen_anterior:
        delete_file_if_exists(imagen_anterior)

    return add_image_url(producto_actualizado)