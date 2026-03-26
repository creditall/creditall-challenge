from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

# define o roteador com prefixo e tag para documentação automática
router = APIRouter(prefix="/products", tags=["Products"])

# retorna todos os produtos cadastrados
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    # consulta todos os registros da tabela products
    products = db.query(Product).all()
    return products

# retorna um produto específico pelo id
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    # busca o produto pelo id
    product = db.query(Product).filter(Product.id == product_id).first()

    # valida se o produto existe
    if not product:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    return product

# cria um novo produto no banco de dados
@router.post("/", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    # instancia o model com os dados recebidos
    product = Product(**product_data.dict())

    # adiciona ao banco
    db.add(product)
    db.commit()
    db.refresh(product)

    return product

# atualiza um produto existente
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    # busca o produto pelo id
    product = db.query(Product).filter(Product.id == product_id).first()

    # valida existência
    if not product:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    # atualiza apenas os campos enviados na requisição
    update_data = product_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

# remove um produto do banco
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # busca o produto
    product = db.query(Product).filter(Product.id == product_id).first()

    # valida existência
    if not product:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    # remove do banco
    db.delete(product)
    db.commit()

    return {"message": "produto deletado com sucesso"}