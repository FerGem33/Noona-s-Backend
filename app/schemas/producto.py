from decimal import Decimal
from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    id_categoria: int = Field(..., ge=1)
    id_receta: int = Field(..., ge=1)
    descripcion: str = Field(..., max_length=100)
    precio_unitario: Decimal = Field(..., ge=0)
    imagen: str | None = Field(None, max_length=255)
    activo: bool


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(BaseModel):
    id_categoria: int | None = Field(None, ge=1)
    id_receta: int | None = Field(None, ge=1)
    descripcion: str | None = Field(None, max_length=100)
    precio_unitario: Decimal | None = Field(None, ge=0)
    imagen: str | None = Field(None, max_length=255)
    activo: bool | None = None


class ProductoOut(ProductoBase):
    id_producto: int = Field(..., ge=1)
    image_url: str | None = None

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }