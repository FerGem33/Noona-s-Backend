from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import date, datetime
from zoneinfo import ZoneInfo

from app.core.dependencies import get_db, validate_key_exist
from app.services.pdf import generate_pdf


def format_date(_date: date):
    return _date.strftime("%d/%m/%Y")


def get_today(formatted=True):
    if formatted:
        return format_date(datetime.now(tz=ZoneInfo("America/Mexico_City")).date())

    return datetime.now(tz=ZoneInfo("America/Mexico_City")).date()


def validar_rango_fechas(fecha_inicio: date, fecha_fin: date):
    hoy = get_today(False)

    if fecha_inicio > hoy or fecha_fin > hoy:
        raise HTTPException(
            status_code=400,
            detail="Las fechas deben ser pasadas o como máximo la fecha actual"
        )

    if fecha_inicio > fecha_fin:
        raise HTTPException(
            status_code=400,
            detail="fecha_inicio debe ser menor o igual que fecha_fin"
        )


router = APIRouter()


@router.get("/inventario")
def reporte_inventario(db: Session = Depends(get_db)):
    result = db.execute(text("""
         SELECT mp.descripcion as insumo, u.abreviatura as unidad, mp.stock_actual, 
                mp.minimo as stock_minimo, mp.maximo as stock_maximo,
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
        {"label": "Insumos", "value": len(items)},
        {"label": "Insumos con stock bajo", "value": insumos_bajo},
        {"label": "Insumos con stock suficiente", "value": insumos_normal},
        {"label": "Insumos con stock excesivo", "value": insumos_exceso},
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


@router.get("/ventas")
def reporte_ventas(
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db)
):
    validar_rango_fechas(fecha_inicio, fecha_fin)

    result = db.execute(text("""
        SELECT c.nombre || ' ' || c.apellido AS cliente, 
               to_char(p.fecha_pedido, 'DD/MM/YYYY') AS fecha_pedido,
               to_char(p.fecha_entrega, 'DD/MM/YYYY') AS fecha_entrega,
               p.total
        FROM pedidos p
        JOIN cliente c ON p.id_cliente = c.id_cliente
        WHERE p.fecha_entrega::date BETWEEN :fecha_inicio AND :fecha_fin
          AND p.id_estado = (
              SELECT id_estado 
              FROM estado 
              WHERE descripcion = 'Entregado'
          )
        ORDER BY p.fecha_entrega DESC;
    """), {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    })

    ventas = result.mappings().all()

    n_ventas = len(ventas)
    sum_ventas = sum(c.total for c in ventas)

    if n_ventas > 0:
        avg_ventas = sum_ventas / n_ventas
    else:
        avg_ventas = 0

    stats = [
        {"label": "Ventas", "value": n_ventas},
        {"label": "Total de ventas", "value": f'${sum_ventas:,.2f}'},
        {"label": "Promedio de ventas", "value": f'${avg_ventas:,.2f}'},
    ]

    pdf = generate_pdf(
        "ventas.html",
        {
            "reporte_titulo": "Reporte de ventas",
            "inicio": format_date(fecha_inicio),
            "fin": format_date(fecha_fin),
            "ventas": ventas,
            "stats": stats,
        }
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=ventas.pdf"}
    )


@router.get("/compras")
def reporte_compras(
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db)
):
    validar_rango_fechas(fecha_inicio, fecha_fin)

    result = db.execute(text("""
        SELECT p.descripcion AS proveedor, 
               to_char(c.fecha, 'DD/MM/YYYY') AS fecha,
               c.total
        FROM compra c
        JOIN proveedor p ON c.id_proveedor = p.id_proveedor
        WHERE c.fecha::date BETWEEN :fecha_inicio AND :fecha_fin
        ORDER BY c.fecha DESC;
    """), {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    })

    compras = result.mappings().all()

    n_compras = len(compras)
    sum_compras = sum(c.total for c in compras)

    if n_compras > 0:
        avg_compras = sum_compras / n_compras
    else:
        avg_compras = 0

    stats = [
        {"label": "Compras", "value": n_compras},
        {"label": "Total de compras", "value": f'${sum_compras:,.2f}'},
        {"label": "Promedio de compras", "value": f'${avg_compras:,.2f}'},
    ]

    pdf = generate_pdf(
        "compras.html",
        {
            "reporte_titulo": "Reporte de compras",
            "inicio": format_date(fecha_inicio),
            "fin": format_date(fecha_fin),
            "compras": compras,
            "stats": stats,
        }
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=compras.pdf"}
    )


@router.get("/pedidos")
def reporte_pedidos(
    fecha_inicio: date,
    fecha_fin: date,
    db: Session = Depends(get_db)
):
    validar_rango_fechas(fecha_inicio, fecha_fin)

    result = db.execute(text("""
         SELECT c.nombre || ' ' || c.apellido AS cliente,
                d.descripcion AS direccion,
                to_char(p.fecha_pedido, 'DD/MM/YYYY') AS fecha_pedido,
                to_char(p.fecha_entrega, 'DD/MM/YYYY') AS fecha_entrega,
                p.total,
                CASE 
                    WHEN p.tipo_entrega = TRUE THEN 'Domicilio'
                    ELSE 'En local'
                END AS tipo_entrega,
                e.descripcion AS estado
         FROM pedidos p
         JOIN cliente c ON p.id_cliente = c.id_cliente
         JOIN direccion d ON p.id_direccion = d.id_direccion
         JOIN estado e ON p.id_estado = e.id_estado
         WHERE p.fecha_pedido::date BETWEEN :fecha_inicio AND :fecha_fin
            OR p.fecha_entrega::date BETWEEN :fecha_inicio AND :fecha_fin
         ORDER BY p.fecha_entrega;
    """), {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    })

    pedidos = result.mappings().all()

    result2 = db.execute(text("""
        SELECT e.descripcion AS estado,
               COUNT(*) AS pedidos
        FROM estado e
        JOIN pedidos p ON e.id_estado = p.id_estado
        WHERE p.fecha_pedido::date BETWEEN :fecha_inicio AND :fecha_fin
           OR p.fecha_entrega::date BETWEEN :fecha_inicio AND :fecha_fin
        GROUP BY e.descripcion;
    """), {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin
    })

    estados = result2.mappings().all()

    stats = [
        {"label": "Pedidos", "value": sum(e.pedidos for e in estados)},
    ]

    for estado in estados:
        stats.append({
            "label": f'Pedidos {estado["estado"]}',
            "value": estado["pedidos"]
        })

    pdf = generate_pdf(
        "pedidos.html",
        {
            "reporte_titulo": "Reporte de pedidos",
            "inicio": format_date(fecha_inicio),
            "fin": format_date(fecha_fin),
            "pedidos": pedidos,
            "stats": stats,
        }
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=pedidos.pdf"}
    )


@router.get("/compra/{id_compra}")
def reporte_compra(
    id_compra: int,
    db: Session = Depends(get_db)
):
    validate_key_exist(db, id_compra, "compra", "id_compra")

    result = db.execute(text("""
        SELECT mp.descripcion, mpc.cantidad, um.abreviatura AS unidad, mp.precio_unitario, (mpc.cantidad * mp.precio_unitario) AS subtotal
        FROM materia_prima mp
        JOIN materia_prima_compra mpc ON mp.id_materia = mpc.id_materia
        JOIN unidad_medida um ON mp.id_unidad = um.id_unidad
        WHERE mpc.id_compra = :id_compra
        ORDER BY descripcion
    """), {
        "id_compra": id_compra
    })

    detalle = result.mappings().all()

    result = db.execute(text("""
            SELECT p.descripcion AS proveedor, c.fecha, c.total
            FROM compra c
            JOIN proveedor p ON c.id_proveedor = p.id_proveedor
            WHERE c.id_compra = :id_compra;
        """), {
        "id_compra": id_compra
    })

    compra = result.mappings().first()

    stats = [
        {"label": "Proveedor", "value": compra["proveedor"]},
        {"label": "Total de compra", "value": f'${compra["total"]:,.2f}'},
        {"label": "Fecha", "value": format_date(compra["fecha"])},
    ]

    pdf = generate_pdf(
        "compra.html",
        {
            "reporte_titulo": "Reporte de compra",
            "fecha_de_hoy": get_today(),
            "id": id_compra,
            "detalle": detalle,
            "stats": stats,
        }
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=compra.pdf"}
    )


@router.get("/pedido/{id_pedido}")
def reporte_pedido(
    id_pedido: int,
    db: Session = Depends(get_db)
):
    validate_key_exist(db, id_pedido, "pedidos", "id_pedido")

    pedido = db.execute(text("""
        SELECT 
            p.id_pedido,
            p.id_cotizacion,
            c.nombre || ' ' || c.apellido AS cliente,
            d.descripcion AS direccion,
            e.descripcion AS estado,
            p.fecha_pedido,
            p.fecha_entrega,
            CASE 
                WHEN p.tipo_entrega = TRUE THEN 'A domicilio'
                ELSE 'Recoger en tienda'
            END AS tipo_entrega,
            p.subtotal,
            cot.precio_envio,
            p.total,
            p.comentario
        FROM pedidos p
        JOIN cliente c ON p.id_cliente = c.id_cliente
        JOIN direccion d ON p.id_direccion = d.id_direccion
        JOIN estado e ON p.id_estado = e.id_estado
        JOIN cotizacion cot ON p.id_cotizacion = cot.id_cotizacion
        WHERE p.id_pedido = :id_pedido
    """), {
        "id_pedido": id_pedido
    }).mappings().first()

    pedido = dict(pedido)
    pedido["fecha_pedido"] = format_date(pedido["fecha_pedido"])
    pedido["fecha_entrega"] =  format_date(pedido["fecha_entrega"])

    detalle = db.execute(text("""
        SELECT
            pr.descripcion AS producto,
            dc.cantidad,
            pr.precio_unitario,
            dc.precio_disenio,
            (pr.precio_unitario * dc.cantidad) AS subtotal_producto,
            ((pr.precio_unitario * dc.cantidad) + dc.precio_disenio) AS total_producto
        FROM pedidos p
        JOIN cotizacion cot ON p.id_cotizacion = cot.id_cotizacion
        JOIN detalles_cotizacion dc ON cot.id_cotizacion = dc.id_cotizacion
        JOIN producto pr ON dc.id_producto = pr.id_producto
        WHERE p.id_pedido = :id_pedido
        ORDER BY pr.descripcion
    """), {
        "id_pedido": id_pedido
    }).mappings().all()

    pdf = generate_pdf(
        "pedido.html",
        {
            "reporte_titulo": f"Reporte de pedido #{id_pedido}",
            "fecha_de_hoy": get_today(),
            "id": id_pedido,
            "pedido": pedido,
            "detalle": detalle,
        }
    )

    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=pedido.pdf"}
    )
