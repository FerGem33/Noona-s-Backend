from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.crud.materia_prima import (
    create_materia_prima,
    get_materia_primas,
    get_materia_prima_by_id,
    update_materia_prima,
    update_materia_prima_imagen,
    delete_materia_prima
)
from app.schemas.materia_prima import (
    MateriaPrimaCreate,
    MateriaPrimaUpdate,
    MateriaPrimaOut
)
from app.utils.files import build_image_url, delete_file_if_exists, save_image_file

router = APIRouter()
authorized_roles = [Roles.ADMIN, Roles.DUENA]


def add_image_url(materia_prima):
    if not materia_prima:
        return None

    materia_prima_dict = dict(materia_prima)
    materia_prima_dict["image_url"] = build_image_url(materia_prima_dict.get("imagen"))
    return materia_prima_dict


def add_image_url_list(materias_primas):
    return [add_image_url(materia_prima) for materia_prima in materias_primas]


@router.post("/", response_model=MateriaPrimaOut, status_code=201)
def crear_materia_prima(
    materia_prima: MateriaPrimaCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    validate_key_exist(db, materia_prima.id_unidad, "unidad_medida", "id_unidad")

    materia_prima_creada = create_materia_prima(db, materia_prima)
    return add_image_url(materia_prima_creada)


@router.get("/", response_model=list[MateriaPrimaOut])
def listar_materias_primas(
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    materias_primas = get_materia_primas(db)
    return add_image_url_list(materias_primas)


@router.get("/{id_materia}", response_model=MateriaPrimaOut)
def obtener_materia_prima(
    id_materia: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    materia_prima = get_materia_prima_by_id(db, id_materia)

    if not materia_prima:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

    return add_image_url(materia_prima)


@router.put("/{id_materia}", response_model=MateriaPrimaOut)
def actualizar_materia_prima(
    id_materia: int,
    materia_prima: MateriaPrimaUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    if materia_prima.id_unidad is not None:
        validate_key_exist(db, materia_prima.id_unidad, "unidad_medida", "id_unidad")

    materia_prima_actualizada = update_materia_prima(db, id_materia, materia_prima)

    if not materia_prima_actualizada:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

    return add_image_url(materia_prima_actualizada)


@router.delete("/{id_materia}", response_model=MateriaPrimaOut)
def eliminar_materia_prima(
    id_materia: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    materia_prima_eliminada = delete_materia_prima(db, id_materia)

    if not materia_prima_eliminada:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

    if materia_prima_eliminada.get("imagen"):
        delete_file_if_exists(materia_prima_eliminada["imagen"])

    return add_image_url(materia_prima_eliminada)


@router.post("/{id_materia}/imagen", response_model=MateriaPrimaOut)
async def subir_imagen_materia_prima(
    id_materia: int,
    imagen: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    materia_prima = get_materia_prima_by_id(db, id_materia)

    if not materia_prima:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

    imagen_anterior = materia_prima.get("imagen")
    nueva_imagen = None

    try:
        nueva_imagen = await save_image_file(imagen, "materia_prima")
        materia_prima_actualizada = update_materia_prima_imagen(db, id_materia, nueva_imagen)

        if imagen_anterior and imagen_anterior != nueva_imagen:
            delete_file_if_exists(imagen_anterior)

        return add_image_url(materia_prima_actualizada)

    except Exception:
        if nueva_imagen:
            delete_file_if_exists(nueva_imagen)
        raise


@router.delete("/{id_materia}/imagen", response_model=MateriaPrimaOut)
def eliminar_imagen_materia_prima(
    id_materia: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    materia_prima = get_materia_prima_by_id(db, id_materia)

    if not materia_prima:
        raise HTTPException(status_code=404, detail="Materia prima no encontrada")

    imagen_anterior = materia_prima.get("imagen")
    materia_prima_actualizada = update_materia_prima_imagen(db, id_materia, None)

    if imagen_anterior:
        delete_file_if_exists(imagen_anterior)

    return add_image_url(materia_prima_actualizada)