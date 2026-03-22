from pydantic import BaseModel, Field
from typing import Optional


class DireccionCreate(BaseModel):
    id_cliente: int = Field(..., ge=1)
    descripcion: str = Field(..., min_length=1, max_length=200)


class DireccionUpdate(BaseModel):
    id_cliente: Optional[int] = Field(None, ge=1)
    descripcion: Optional[str] = Field(None, min_length=1, max_length=200)


class DireccionRead(BaseModel):
    id_direccion: int
    id_cliente: int
    descripcion: str