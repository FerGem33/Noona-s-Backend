from pydantic import BaseModel, Field


class MateriaPrimaCompraBase(BaseModel):
    id_materia: int = Field(..., ge=1)
    cantidad: float = Field(..., gt=0)


class MateriaPrimaCompraCreate(MateriaPrimaCompraBase):
    id_compra: int = Field(..., ge=1)

class MateriaPrimaCompraUpdate(BaseModel):
    id_materia: int | None = Field(None, ge=1)
    id_compra: int | None = Field(None, ge=1)
    cantidad: float | None = Field(None, ge=0)


class MateriaPrimaCompraOut(MateriaPrimaCompraBase):
    id_compra: int = Field(..., ge=1)