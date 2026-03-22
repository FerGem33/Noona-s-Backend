from pydantic import BaseModel, Field


class CategoriaBase(BaseModel):
    descripcion: str = Field(..., max_length=100)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaUpdate(BaseModel):
    descripcion: str | None = Field(None, max_length=100)


class CategoriaOut(CategoriaBase):
    id_categoria: int = Field(..., ge=1)