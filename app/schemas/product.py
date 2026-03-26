from pydantic import BaseModel, Field

# base com campos comuns do produto
class ProductBase(BaseModel):
    # nome do produto (obrigatório)
    name: str = Field(..., min_length=1, max_length=150)

    # descrição do produto (obrigatória)
    description: str = Field(..., min_length=1, max_length=255)

    # preço deve ser maior que 0
    price: float = Field(..., gt=0)

# schema usado para criação de produto
class ProductCreate(ProductBase):
    pass

# schema usado para atualização (campos opcionais)
class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = Field(default=None, min_length=1, max_length=255)
    price: float | None = Field(default=None, gt=0)

    # caminho da imagem (opcional)
    image: str | None = None

# schema de resposta da API
class ProductResponse(ProductBase):
    id: int
    image: str | None = None

    class Config:
        # permite retornar diretamente objetos do SQLAlchemy
        from_attributes = True