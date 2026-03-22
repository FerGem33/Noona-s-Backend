from pydantic import BaseModel, Field
from typing import Optional


class TipoPagoCreate(BaseModel):
    descripcion: str = Field(..., min_length=1, max_length=100)


class TipoPagoUpdate(BaseModel):
    descripcion: Optional[str] = Field(None, min_length=1, max_length=100)


class TipoPagoRead(BaseModel):
    id_tipo_pago: int
    descripcion: str