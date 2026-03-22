from decimal import Decimal

from pydantic import BaseModel, Field


class PedidosHasProductoBase(BaseModel):
    id_pedido: int = Field(..., ge=1)
    id_producto: int = Field(..., ge=1)
    cantidad: int = Field(..., ge=0)
    precio_diseno: Decimal = Field(..., ge=0)
    precio_envio: Decimal = Field(..., ge=0)


class PedidosHasProductoCreate(PedidosHasProductoBase):
    pass


class PedidosHasProductoUpdate(BaseModel):
    id_pedido: int | None = Field(None, ge=1)
    id_producto: int | None = Field(None, ge=1)
    cantidad: int | None = Field(None, ge=0)
    precio_diseno: Decimal | None = Field(None, ge=0)
    precio_envio: Decimal | None = Field(None, ge=0)


class PedidosHasProductoOut(PedidosHasProductoBase):
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }