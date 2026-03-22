from pydantic import BaseModel, Field
from typing import Optional


class UsuarioCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    id_rol: int = Field(..., ge=1, le=2147483647)
    contrasena: str = Field(..., min_length=1, max_length=72)


class UsuarioUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    id_rol: Optional[int] = Field(None, ge=1, le=2147483647)
    contrasena: Optional[str] = Field(None, min_length=1, max_length=72)


class UsuarioRead(BaseModel):
    id_usuario: int = Field(..., ge=1, le=2147483647)
    nombre: str = Field(..., min_length=1, max_length=100)
    id_rol: int = Field(..., ge=1, le=2147483647)
    rol: str = Field(..., min_length=1, max_length=100)