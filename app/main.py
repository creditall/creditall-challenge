from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.api.routes.clients import router as clients_router
from app.api.routes.products import router as products_router
from app.api.routes.sales import router as sales_router
from app.core.database import Base, engine
from app.models.client import Client
from app.models.product import Product
from app.models.sale import Sale

# cria as tabelas no banco
Base.metadata.create_all(bind=engine)

# instancia a aplicação
app = FastAPI()

# define o caminho da pasta static
base_dir = Path(__file__).resolve().parent
static_dir = base_dir / "static"
uploads_dir = static_dir / "uploads"

# garante que a pasta de uploads exista
uploads_dir.mkdir(parents=True, exist_ok=True)

# registra a pasta static para servir arquivos
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# registra as rotas
app.include_router(products_router)
app.include_router(clients_router)
app.include_router(sales_router)


@app.get("/")
def root():
    return {"message": "API ON"}