from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class PedidoCreate(BaseModel):
    id_direccion: int = Field(..., ge=1)
    id_estado: int = Field(..., ge=1)
    id_cliente: int = Field(..., ge=1)
    fecha_entrega: datetime
    fecha_pedido: datetime
    comentario: Optional[str] = Field(None, max_length=255)
    tipo_entrega: bool
    subtotal: float = Field(..., ge=0)
    total: float = Field(..., ge=0)


class PedidoUpdate(BaseModel):
    id_direccion: Optional[int] = Field(None, ge=1)
    id_estado: Optional[int] = Field(None, ge=1)
    id_cliente: Optional[int] = Field(None, ge=1)
    fecha_entrega: Optional[datetime] = None
    fecha_pedido: Optional[datetime] = None
    comentario: Optional[str] = Field(None, max_length=255)
    tipo_entrega: Optional[bool] = None
    subtotal: Optional[float] = Field(None, ge=0)
    total: Optional[float] = Field(None, ge=0)


class PedidoRead(BaseModel):
    id_pedido: int
    id_direccion: int
    id_estado: int
    id_cliente: int
    direccion: str
    estado:  str
    cliente: str
    fecha_entrega: datetime
    fecha_pedido: datetime
    comentario: Optional[str]
    tipo_entrega: bool
    subtotal: float
    total: float