from sqlalchemy import Column, Float, Integer, String

from app.core.database import Base


# model da entidade produto
class Product(Base):
    __tablename__ = "products"

    # chave primária do produto
    id = Column(Integer, primary_key=True, index=True)

    # nome do produto
    name = Column(String(150), nullable=False)

    # descrição do produto
    description = Column(String(255), nullable=False)

    # preço do produto
    price = Column(Float, nullable=False)

    # caminho da imagem do produto, caso exista
    image = Column(String(255), nullable=True)