from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from app.core.database import Base


# model da entidade venda
class Sale(Base):
    __tablename__ = "sales"

    # chave primária da venda
    id = Column(Integer, primary_key=True, index=True)

    # id do produto relacionado à venda
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)

    # id do cliente relacionado à venda
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=True)

    # data da venda gerada automaticamente
    sale_date = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    # quantidade vendida
    quantity = Column(Integer, nullable=False)

    # desconto aplicado
    discount = Column(Float, nullable=False, default=0)

    # status da venda
    status = Column(String(50), nullable=False)