from datetime import datetime

from pydantic import BaseModel, Field

# base com dados principais da venda
class SaleBase(BaseModel):
    # ID do produto vendido
    product_id: int

    # cliente pode ser opcional
    client_id: int | None = None

    # quantidade deve ser maior que 0
    quantity: int = Field(..., gt=0)

    # desconto não pode ser negativo
    discount: float = Field(default=0, ge=0)

    # status da venda (ex: concluída, cancelada, pendente)
    status: str = Field(..., min_length=1, max_length=50)

# schema para criação
class SaleCreate(SaleBase):
    pass

# schema para atualização
class SaleUpdate(BaseModel):
    product_id: int | None = None
    client_id: int | None = None
    quantity: int | None = Field(default=None, gt=0)
    discount: float | None = Field(default=None, ge=0)
    status: str | None = Field(default=None, min_length=1, max_length=50)

# schema de resposta
class SaleResponse(SaleBase):
    id: int

    # data gerada automaticamente pelo banco
    sale_date: datetime

    class Config:
        # permite retornar objetos do SQLAlchemy
        from_attributes = True