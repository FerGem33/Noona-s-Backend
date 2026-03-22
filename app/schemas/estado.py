from pydantic import BaseModel, Field
from typing import Optional


class EstadoCreate(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=100)


class EstadoUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, min_length=1, max_length=100)


class EstadoRead(BaseModel):
    id_estado: int
    descripcion: str