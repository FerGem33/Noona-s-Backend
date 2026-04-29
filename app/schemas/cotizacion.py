from decimal import Decimal

from pydantic import BaseModel, Field


class CotizacionBase(BaseModel):
    id_pedido: int = Field(..., ge=1)
    id_producto: int = Field(..., ge=1)
    id_estado: int = Field(..., ge=1)
    cantidad: int = Field(..., ge=0)
    precio_disenio: Decimal = Field(..., ge=0)
    precio_envio: Decimal = Field(..., ge=0)


class CotizacionCreate(CotizacionBase):
    pass


class CotizacionUpdate(BaseModel):
    id_pedido: int | None = Field(None, ge=1)
    id_producto: int | None = Field(None, ge=1)
    id_estado: int | None = Field(None, ge=1)
    cantidad: int | None = Field(None, ge=0)
    precio_disenio: Decimal | None = Field(None, ge=0)
    precio_envio: Decimal | None = Field(None, ge=0)


class CotizacionOut(CotizacionBase):
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }