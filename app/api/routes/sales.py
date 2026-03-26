from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.client import Client
from app.models.product import Product
from app.models.sale import Sale
from app.schemas.sale import SaleCreate, SaleResponse, SaleUpdate

# define o roteador para vendas
router = APIRouter(prefix="/sales", tags=["Sales"])


# retorna todas as vendas cadastradas
@router.get("/", response_model=list[SaleResponse])
def get_sales(db: Session = Depends(get_db)):
    return db.query(Sale).all()


# retorna uma venda específica pelo id
@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        raise HTTPException(status_code=404, detail="venda não encontrada")

    return sale


# cria uma nova venda com validação de relacionamento
@router.post("/", response_model=SaleResponse)
def create_sale(sale_data: SaleCreate, db: Session = Depends(get_db)):
    # verifica se o produto informado existe
    product = db.query(Product).filter(Product.id == sale_data.product_id).first()
    if not product:
        raise HTTPException(status_code=400, detail="produto informado não existe")

    # se client_id for informado, valida se o cliente existe
    if sale_data.client_id is not None:
        client = db.query(Client).filter(Client.id == sale_data.client_id).first()
        if not client:
            raise HTTPException(status_code=400, detail="cliente informado não existe")

    # cria a instância da venda
    sale = Sale(**sale_data.dict())

    db.add(sale)
    db.commit()
    db.refresh(sale)

    return sale


# atualiza uma venda existente
@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(sale_id: int, sale_data: SaleUpdate, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        raise HTTPException(status_code=404, detail="venda não encontrada")

    update_data = sale_data.dict(exclude_unset=True)

    # se product_id for enviado, valida se o produto existe
    if "product_id" in update_data:
        product = db.query(Product).filter(Product.id == update_data["product_id"]).first()
        if not product:
            raise HTTPException(status_code=400, detail="produto informado não existe")

    # se client_id for enviado e não for nulo, valida se o cliente existe
    if "client_id" in update_data and update_data["client_id"] is not None:
        client = db.query(Client).filter(Client.id == update_data["client_id"]).first()
        if not client:
            raise HTTPException(status_code=400, detail="cliente informado não existe")

    # aplica os campos recebidos
    for key, value in update_data.items():
        setattr(sale, key, value)

    db.commit()
    db.refresh(sale)

    return sale


# remove uma venda
@router.delete("/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(get_db)):
    sale = db.query(Sale).filter(Sale.id == sale_id).first()

    if not sale:
        raise HTTPException(status_code=404, detail="venda não encontrada")

    db.delete(sale)
    db.commit()

    return {"message": "venda deletada com sucesso"}