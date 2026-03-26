from pydantic import BaseModel, EmailStr, Field

# base com dados comuns do cliente
class ClientBase(BaseModel):
    # nome do cliente
    name: str = Field(..., min_length=1, max_length=150)

    # Email validado automaticamente
    email: EmailStr

    # CPF (sem validação de algoritmo, apenas tamanho)
    cpf: str = Field(..., min_length=11, max_length=14)


# schema para criação
class ClientCreate(ClientBase):
    pass

# schema para atualização (campos opcionais)
class ClientUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    cpf: str | None = Field(default=None, min_length=11, max_length=14)

# schema de resposta
class ClientResponse(ClientBase):
    id: int

    class Config:
        # prmite integração com ORM (SQLAlchemy)
        from_attributes = True