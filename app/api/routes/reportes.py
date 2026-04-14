from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime, timedelta
from zoneinfo import ZoneInfo

from app.core.dependencies import get_db
from app.services.pdf import generate_pdf

def format_date(_date: date):
    return _date.strftime("%d/%m/%Y")

def get_today(formatted=True):
    if formatted:
        return format_date(datetime.now(tz=ZoneInfo("America/Mexico_City")).date())
    return datetime.now(tz=ZoneInfo("America/Mexico_City")).date()


router = APIRouter()

@router.get("/inventario")
def reporte_inventario(db: Session = Depends(get_db)):
    result = db.execute(text("""
         SELECT mp.descripcion as insumo, u.descripcion as unidad, mp.stock_actual, 
                mp.minimo as stock_minimo, mp.maximo as stock_maximo, mp.precio_unitario,
                CASE
                    WHEN stock_actual < minimo THEN 1
                    WHEN stock_actual > maximo THEN 3
                    ELSE 2
                END AS estado
         FROM materia_prima mp
         JOIN unidad_medida u ON mp.id_unidad = u.id_unidad
         ORDER BY estado;
     """))
    items = [dict(row) for row in result.mappings().all()]

    insumos_bajo = 0
    insumos_normal = 0
    insumos_exceso = 0

    for item in items:
        estado = item["estado"]

        if estado == 1:
            insumos_bajo += 1
            item["estado"] = "Bajo"
        elif estado == 2:
            insumos_normal += 1
            item["estado"] = "Suficiente"
        else:
            insumos_exceso += 1
            item["estado"] = "Exceso"

    stats = [
        {"label":"Insumos", "value":len(items)},
        {"label":"Insumos con stock bajo", "value":insumos_bajo},
        {"label":"Insumos con stock suficiente", "value":insumos_normal},
        {"label":"Insumos con stock excesivo", "value":insumos_exceso},
    ]

    pdf = generate_pdf(
        "inventario.html",
        {
            "reporte_titulo": "Reporte de inventario",
            "fecha": get_today(),
            "items": items,
            "stats": stats,
        }
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=inventario.pdf"}
    )

@router.get("/ventas/{dias}")
def reporte_ventas(dias: int, db: Session = Depends(get_db)):
    result = db.execute(text("""
        SELECT c.nombre||' '||apellido AS cliente, 
        to_char(p.fecha_pedido, 'DD/MM/YYYY') as fecha_pedido,
        to_char(p.fecha_entrega, 'DD/MM/YYYY') as fecha_entrega, p.total
        FROM pedidos p
        JOIN cliente c ON p.id_cliente = c.id_cliente
        WHERE p.fecha_entrega > CURRENT_DATE - :days
            AND p.id_estado = (SELECT id_estado FROM estado WHERE descripcion = 'Entregado')
        ORDER BY fecha_entrega DESC;
    """), {
        "days": dias
        }
    )
    ventas = result.mappings().all()

    n_ventas = len(ventas)
    sum_ventas = sum(c.total for c in ventas)
    if n_ventas > 0:
        avg_ventas = sum_ventas/n_ventas
    else:
        avg_ventas = 0

    stats = [
        {"label": "Ventas", "value": n_ventas},
        {"label": "Total de ventas", "value": f'${sum_ventas}'},
        {"label": "Promedio de ventas", "value": f'${avg_ventas}'},
    ]

    pdf = generate_pdf(
        "ventas.html",
        {
            "reporte_titulo": "Reporte de ventas",
            "inicio": format_date(get_today(False) - timedelta(days=dias)),
            "fin": get_today(),
            "ventas": ventas,
            "stats": stats,
        }
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=ventas.pdf"}
    )

