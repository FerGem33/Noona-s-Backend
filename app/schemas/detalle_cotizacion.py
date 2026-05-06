from decimal import Decimal
from pydantic import BaseModel, Field


class DetalleCotizacionBase(BaseModel):
    id_producto: int = Field(..., ge=1)
    cantidad: int = Field(..., ge=0)
    precio_disenio: Decimal = Field(..., ge=0)


class DetalleCotizacionRead(DetalleCotizacionBase):
    producto: str