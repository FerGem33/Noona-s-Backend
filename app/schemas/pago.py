from decimal import Decimal
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PagoCreate(BaseModel):
    id_pedido: int = Field(..., ge=1)
    id_estado_pago: int = Field(..., ge=1)
    id_tipo_pago: int = Field(..., ge=1)
    anticipo: bool
    monto: Decimal = Field(..., ge=0)
    fecha: datetime


class PagoUpdate(BaseModel):
    id_pedido: Optional[int] = Field(None, ge=1)
    id_estado_pago: Optional[int] = Field(None, ge=1)
    id_tipo_pago: Optional[int] = Field(None, ge=1)
    anticipo: Optional[bool] = None
    monto: Optional[Decimal] = Field(None, ge=0)
    fecha: Optional[datetime] = None


class PagoRead(BaseModel):
    id_pago: int
    id_pedido: int
    id_estado_pago: int
    id_tipo_pago: int
    anticipo: bool
    monto: Decimal
    fecha: datetime

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }