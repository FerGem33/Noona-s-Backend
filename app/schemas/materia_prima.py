from decimal import Decimal

from pydantic import BaseModel, Field


class MateriaPrimaBase(BaseModel):
    id_unidad: int = Field(..., ge=1)
    descripcion: str = Field(..., max_length=100)
    precio_unitario: Decimal = Field(..., ge=0)
    minimo: float = Field(..., ge=0)
    maximo: float = Field(..., ge=0)
    stock_actual: float = Field(..., ge=0)
    imagen: str | None = Field(None, max_length=255)
    activo: bool


class MateriaPrimaCreate(MateriaPrimaBase):
    pass


class MateriaPrimaUpdate(BaseModel):
    id_unidad: int | None = Field(None, ge=1)
    descripcion: str | None = Field(None, max_length=100)
    precio_unitario: Decimal | None = Field(None, ge=0)
    minimo: float | None = Field(None, ge=0)
    maximo: float | None = Field(None, ge=0)
    stock_actual: float | None = Field(None, ge=0)
    imagen: str | None = Field(None, max_length=255)
    activo: bool | None = None


class MateriaPrimaOut(MateriaPrimaBase):
    id_materia: int = Field(..., ge=1)
    image_url: str | None = None

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }