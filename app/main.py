from fastapi import FastAPI

from app.api.routes.clients import router as clients_router
from app.api.routes.products import router as products_router
from app.core.database import Base, engine
from app.models.client import Client
from app.models.product import Product
from app.models.sale import Sale

# cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# instancia a aplicação
app = FastAPI()

# registra as rotas
app.include_router(products_router)
app.include_router(clients_router)


@app.get("/")
def root():
    return {"message": "API ON"}