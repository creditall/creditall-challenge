from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

# define o roteador com prefixo e tag
router = APIRouter(prefix="/products", tags=["Products"])

# define o diretório onde os uploads serão salvos
base_dir = Path(__file__).resolve().parents[2]
upload_dir = base_dir / "static" / "uploads"
upload_dir.mkdir(parents=True, exist_ok=True)


# retorna todos os produtos cadastrados
@router.get("/", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return products


# retorna um produto específico pelo id
@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    return product


# cria um novo produto
@router.post("/", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**product_data.dict())

    db.add(product)
    db.commit()
    db.refresh(product)

    return product


# atualiza um produto existente
@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_data: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    update_data = product_data.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product


# faz upload de imagem para um produto existente
@router.post("/{product_id}/upload-image", response_model=ProductResponse)
def upload_product_image(
    product_id: int,
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # busca o produto no banco
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    # valida se o arquivo enviado é uma imagem
    if not image.content_type or not image.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="o arquivo enviado não é uma imagem válida")

    # gera nome único para evitar conflito entre arquivos
    file_extension = Path(image.filename).suffix
    file_name = f"{uuid4()}{file_extension}"
    file_path = upload_dir / file_name

    # salva o arquivo fisicamente na pasta de uploads
    with open(file_path, "wb") as buffer:
        buffer.write(image.file.read())

    # salva o caminho relativo no banco
    product.image = f"/static/uploads/{file_name}"

    db.commit()
    db.refresh(product)

    return product


# remove um produto do banco
@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()

    if not product:
        raise HTTPException(status_code=404, detail="produto não encontrado")

    db.delete(product)
    db.commit()

    return {"message": "produto deletado com sucesso"}