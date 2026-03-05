from pydantic import BaseModel, Field
from typing import Optional


class RolCreate(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=100)


class RolUpdate(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=100)


class RolRead(BaseModel):
    id_rol: int = Field(..., ge=1, le=2147483647)
    descripcion: str = Field(..., min_length=1, max_length=100)
