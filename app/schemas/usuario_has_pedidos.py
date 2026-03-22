from pydantic import BaseModel, Field
from typing import Optional


class UsuarioPedidoCreate(BaseModel):
    id_usuario: int = Field(..., ge=1)
    id_pedido: int = Field(..., ge=1)


class UsuarioPedidoUpdate(BaseModel):
    id_usuario: Optional[int] = Field(None, ge=1)
    id_pedido: Optional[int] = Field(None, ge=1)


class UsuarioPedidoRead(BaseModel):
    id_usuario: int
    id_pedido: int