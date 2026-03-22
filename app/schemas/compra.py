from decimal import Decimal
from datetime import datetime

from pydantic import BaseModel, Field


class CompraBase(BaseModel):
    id_proveedor: int = Field(..., ge=1)
    fecha: datetime
    total: Decimal = Field(..., ge=0)


class CompraCreate(CompraBase):
    pass


class CompraUpdate(BaseModel):
    id_proveedor: int | None = Field(None, ge=1)
    fecha: datetime | None = None
    total: Decimal | None = Field(None, ge=0)


class CompraOut(CompraBase):
    id_compra: int = Field(..., ge=1)

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }