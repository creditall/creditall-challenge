from sqlalchemy import Column, Integer, String

from app.core.database import Base


# model da entidade cliente
class Client(Base):
    __tablename__ = "clients"

    # chave primária do cliente
    id = Column(Integer, primary_key=True, index=True)

    # nome do cliente
    name = Column(String(150), nullable=False)

    # email do cliente
    email = Column(String(150), nullable=False, unique=True, index=True)

    # cpf do cliente
    cpf = Column(String(14), nullable=False, unique=True, index=True)