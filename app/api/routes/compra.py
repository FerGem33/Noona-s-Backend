from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List
from decimal import Decimal

from app.core.dependencies import get_db, require_roles, validate_key_exist
from app.core.roles import Roles
from app.schemas.compra import CompraPreCreate, CompraCreate, CompraPreUpdate, CompraUpdate, CompraOut
from app.schemas.materia_prima_compra import MateriaPrimaCompraBase, MateriaPrimaCompraCreate
from app.crud.materia_prima_compra import create_materia_prima_compra, get_materia_prima_compra_by_id_compra, delete_materia_prima_compra
from app.crud.compra import (
    create_compra,
    get_compras,
    get_compra_by_id,
    update_compra,
    delete_compra
)


router = APIRouter()

authorized_roles = [Roles.ADMIN, Roles.DUENA]


def aplicar_compra(db:Session, id_compra:int, detalle: List[MateriaPrimaCompraBase], revert=False):
    for materia in detalle:
        if revert:
            delete_materia_prima_compra(db, materia.id_materia, id_compra, do_commit=False)

        else:
            create_materia_prima_compra(db,
                MateriaPrimaCompraCreate(
                    id_compra=id_compra,
                    id_materia=materia.id_materia,
                    cantidad=materia.cantidad
                ), do_commit=False
            )

        db.execute(
            text("""
            UPDATE materia_prima SET stock_actual = (stock_actual + :cantidad)
            WHERE id_materia = :id_materia
            """),
            {"id_materia": materia.id_materia,
             "cantidad": materia.cantidad if not revert else -materia.cantidad }
        )


@router.post("/", response_model=CompraOut, status_code=201)
def crear_compra(
    pre_compra: CompraPreCreate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    db.reset()
    with db.begin():
        validate_key_exist(db, pre_compra.id_proveedor, "proveedor", "id_proveedor")

        for materia in pre_compra.detalle:
            validate_key_exist(db, materia.id_materia, "materia_prima", "id_materia")

        compra = CompraCreate(**pre_compra.model_dump(), total=Decimal(0.0))

        created_compra = create_compra(db, compra, do_commit=False)
        aplicar_compra(db, created_compra.id_compra, compra.detalle)

        db.execute(text("""UPDATE compra SET efectuada = TRUE WHERE id_compra = :id_compra"""), {"id_compra": created_compra.id_compra})

        created_compra = db.execute(
            text("""
                 UPDATE compra 
                 SET total = (SELECT SUM(mp.precio_unitario * mpc.cantidad)
                                 FROM materia_prima mp
                                 JOIN materia_prima_compra mpc ON mp.id_materia = mpc.id_materia
                                 WHERE mpc.id_compra = :id_compra)
                 WHERE id_compra = :id_compra
                 RETURNING id_compra, id_proveedor, fecha, total, efectuada
                 """), {"id_compra": created_compra.id_compra}
        ).mappings().first()

        return created_compra


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
    pre_compra: CompraPreUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(require_roles(*authorized_roles))
):
    db.reset()
    with db.begin():
        validate_key_exist(db, id_compra, "compra", "id_compra")

        if pre_compra.id_proveedor is not None:
            validate_key_exist(db, pre_compra.id_proveedor, "proveedor", "id_proveedor")

        current_compra = get_compra_by_id(db, id_compra)
        total = Decimal(current_compra["total"])
        if pre_compra.detalle is not None:
            current_detalle = get_materia_prima_compra_by_id_compra(db, id_compra)

            if current_compra.efectuada:
                aplicar_compra(db, id_compra, current_detalle, revert=True)
            aplicar_compra(db, id_compra, pre_compra.detalle)

            updated_total = db.execute(
                text("""
                SELECT SUM(mp.precio_unitario * mpc.cantidad) AS total
                FROM materia_prima mp 
                JOIN materia_prima_compra mpc ON mp.id_materia = mpc.id_materia
                WHERE mpc.id_compra = :id_compra
                """), {"id_compra": id_compra}
            )
            total = Decimal(updated_total.mappings().first()["total"])

        db.execute(text("""UPDATE compra SET efectuada = TRUE WHERE id_compra = :id_compra"""),{"id_compra": id_compra})
        compra = CompraUpdate(**pre_compra.model_dump(), total=total)
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
    validate_key_exist(db, id_compra, "compra", "id_compra")

    current_compra = get_compra_by_id(db, id_compra)
    current_detalle = get_materia_prima_compra_by_id_compra(db, id_compra)

    if current_compra.efectuada:
        aplicar_compra(db, id_compra, current_detalle, revert=True)
    compra_eliminada = delete_compra(db, id_compra)

    if not compra_eliminada:
        raise HTTPException(status_code=404, detail="Compra no encontrada")

    return compra_eliminada