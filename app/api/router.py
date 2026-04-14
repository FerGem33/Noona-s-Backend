from fastapi import APIRouter
from app.api.routes import (
    auth, health, rol, usuario, cliente, direccion, estado, pedidos, usuario_has_pedidos, estado_pago,
    tipo_pago, pago, unidad_medida, materia_prima, receta, receta_materia_prima, producto, categoria,
    pedidos_has_producto, proveedor, compra, materia_prima_compra, reportes
)

api_router = APIRouter(prefix="/api")

routes = {
    "auth": auth.router,
    "health": health.router,
    "rol": rol.router,
    "usuario": usuario.router,
    "cliente": cliente.router,
    "direccion": direccion.router,
    "estado": estado.router,
    "pedidos": pedidos.router,
    "usuario_has_pedidos": usuario_has_pedidos.router,
    "estado_pago": estado_pago.router,
    "tipo_pago": tipo_pago.router,
    "pago": pago.router,
    "unidad_medida": unidad_medida.router,
    "materia_prima": materia_prima.router,
    "receta": receta.router,
    "receta_materia_prima": receta_materia_prima.router,
    "categoria": categoria.router,
    "producto": producto.router,
    "pedidos_has_producto": pedidos_has_producto.router,
    "proveedor": proveedor.router,
    "compra": compra.router,
    "materia_prima_compra": materia_prima_compra.router,
    "reportes": reportes.router,
}

for name, router in zip(routes.keys(), routes.values()):
    api_router.include_router(router, prefix=f"/{name}", tags=[name.capitalize()])
