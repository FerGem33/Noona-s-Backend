from pydantic import BaseModel, Field


class ProveedorBase(BaseModel):
    descripcion: str = Field(..., max_length=100)
    direccion: str = Field(..., max_length=200)
    contacto: str = Field(..., max_length=100)


class ProveedorCreate(ProveedorBase):
    pass


class ProveedorUpdate(BaseModel):
    descripcion: str | None = Field(None, max_length=100)
    direccion: str | None = Field(None, max_length=200)
    contacto: str | None = Field(None, max_length=100)


class ProveedorOut(ProveedorBase):
    id_proveedor: int = Field(..., ge=1)