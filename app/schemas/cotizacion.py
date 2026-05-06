from decimal import Decimal
from typing import List
from pydantic import BaseModel, Field
from app.schemas.detalle_cotizacion import DetalleCotizacionBase


class DetalleCotizacionCreate(DetalleCotizacionBase):
    pass


class DetalleCotizacionOut(DetalleCotizacionBase):
    class Config:
        json_encoders = {Decimal: float}


class CotizacionBase(BaseModel):
    precio_envio: Decimal = Field(..., ge=0)


class CotizacionCreate(CotizacionBase):
    detalles: List[DetalleCotizacionCreate]


class CotizacionUpdate(BaseModel):
    precio_envio: Decimal | None = Field(None, ge=0)
    detalles: List[DetalleCotizacionCreate] | None = None


class CotizacionOut(BaseModel):
    id_cotizacion: int
    precio_envio: Decimal
    detalles: List[DetalleCotizacionOut]

    class Config:
        json_encoders = {Decimal: float}