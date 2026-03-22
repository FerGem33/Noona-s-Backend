from pydantic import BaseModel, Field
from typing import Optional


class ClienteCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    apellido: str = Field(..., min_length=1, max_length=100)
    telefono: str = Field(..., min_length=1, max_length=20)


class ClienteUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, min_length=1, max_length=100)
    telefono: Optional[str] = Field(None, min_length=1, max_length=20)


class ClienteRead(BaseModel):
    id_cliente: int
    nombre: str
    apellido: str
    telefono: str