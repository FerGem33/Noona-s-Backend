from pydantic import BaseModel, Field
from typing import Optional


class UnidadMedidaCreate(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=100)
    abreviatura: str = Field(..., min_length=1, max_length=10)


class UnidadMedidaUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, min_length=1, max_length=100)
    abreviatura: Optional[str] = Field(None, min_length=1, max_length=10)


class UnidadMedidaRead(BaseModel):
    id_unidad: int
    descripcion: str
    abreviatura: str