from fastapi import APIRouter
from app.api.routes import auth, usuario, rol

api_router = APIRouter(prefix="/api")

api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["Auth"]
)

api_router.include_router(
    usuario.router,
    prefix="/usuarios",
    tags=["Usuarios"]
)

api_router.include_router(
    rol.router,
    prefix="/roles",
    tags=["Roles"]
)