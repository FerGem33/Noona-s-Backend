from pydantic import BaseModel, Field


class RecetaMateriaPrimaBase(BaseModel):
    id_receta: int = Field(..., ge=1)
    id_materia: int = Field(..., ge=1)
    cantidad: float = Field(..., ge=0)


class RecetaMateriaPrimaCreate(RecetaMateriaPrimaBase):
    pass


class RecetaMateriaPrimaUpdate(BaseModel):
    id_receta: int | None = Field(None, ge=1)
    id_materia: int | None = Field(None, ge=1)
    cantidad: float | None = Field(None, ge=0)


class RecetaMateriaPrimaOut(RecetaMateriaPrimaBase):
    pass