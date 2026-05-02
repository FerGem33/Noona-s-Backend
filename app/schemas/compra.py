from decimal import Decimal
from datetime import datetime

from typing import List
from pydantic import BaseModel, Field
from app.schemas.materia_prima_compra import MateriaPrimaCompraBase


class CompraBase(BaseModel):
    id_proveedor: int = Field(..., ge=1)
    fecha: datetime

class CompraPreCreate(CompraBase):
    detalle : List[MateriaPrimaCompraBase]


class CompraCreate(CompraPreCreate):
    total: Decimal = Field(..., ge=0)


class CompraPreUpdate(BaseModel):
    id_proveedor: int | None = Field(None, ge=1)
    fecha: datetime | None = None
    detalle: List[MateriaPrimaCompraBase] | None = None


class CompraUpdate(CompraPreUpdate):
    total: Decimal | None = Field(None, ge=0)


class CompraOut(CompraBase):
    id_compra: int = Field(..., ge=1)
    total: Decimal = Field(..., ge=0)
    efectuada: bool

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }