from fastapi import FastAPI

from app.core.database import Base, engine
from app.api.routes.products import router as products_router

# cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# instancia a aplicação FastAPI
app = FastAPI()

# registra as rotas de produtos
app.include_router(products_router)

@app.get("/")
def root():
    return {"message": "API ON"}