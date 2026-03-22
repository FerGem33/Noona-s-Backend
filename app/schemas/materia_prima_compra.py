from decimal import Decimal

from pydantic import BaseModel, Field


class MateriaPrimaCompraBase(BaseModel):
    id_materia: int = Field(..., ge=1)
    id_compra: int = Field(..., ge=1)
    cantidad: float = Field(..., ge=0)
    precio_individual: Decimal = Field(..., ge=0)


class MateriaPrimaCompraCreate(MateriaPrimaCompraBase):
    pass


class MateriaPrimaCompraUpdate(BaseModel):
    id_materia: int | None = Field(None, ge=1)
    id_compra: int | None = Field(None, ge=1)
    cantidad: float | None = Field(None, ge=0)
    precio_individual: Decimal | None = Field(None, ge=0)


class MateriaPrimaCompraOut(MateriaPrimaCompraBase):
    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }