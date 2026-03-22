from pydantic import BaseModel, Field
from typing import Optional


class EstadoPagoCreate(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=100)


class EstadoPagoUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, min_length=1, max_length=100)


class EstadoPagoRead(BaseModel):
    id_estado_pago: int
    descripcion: str