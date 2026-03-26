from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.client import Client
from app.schemas.client import ClientCreate, ClientResponse, ClientUpdate

# define o roteador para clientes
router = APIRouter(prefix="/clients", tags=["Clients"])


# retorna todos os clientes
@router.get("/", response_model=list[ClientResponse])
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()


# retorna um cliente específico pelo id
@router.get("/{client_id}", response_model=ClientResponse)
def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="cliente não encontrado")

    return client


# cria um novo cliente com validação de duplicidade
@router.post("/", response_model=ClientResponse)
def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    # verifica se já existe cliente com o mesmo email
    existing_email = db.query(Client).filter(Client.email == client_data.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="email já cadastrado")

    # verifica se já existe cliente com o mesmo cpf
    existing_cpf = db.query(Client).filter(Client.cpf == client_data.cpf).first()
    if existing_cpf:
        raise HTTPException(status_code=400, detail="cpf já cadastrado")

    # cria a instância do cliente
    client = Client(**client_data.dict())

    db.add(client)
    db.commit()
    db.refresh(client)

    return client


# atualiza um cliente existente
@router.put("/{client_id}", response_model=ClientResponse)
def update_client(client_id: int, client_data: ClientUpdate, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="cliente não encontrado")

    update_data = client_data.dict(exclude_unset=True)

    # valida duplicidade de email em atualização
    if "email" in update_data:
        existing_email = db.query(Client).filter(
            Client.email == update_data["email"],
            Client.id != client_id
        ).first()

        if existing_email:
            raise HTTPException(status_code=400, detail="email já cadastrado")

    # valida duplicidade de cpf em atualização
    if "cpf" in update_data:
        existing_cpf = db.query(Client).filter(
            Client.cpf == update_data["cpf"],
            Client.id != client_id
        ).first()

        if existing_cpf:
            raise HTTPException(status_code=400, detail="cpf já cadastrado")

    # aplica os campos recebidos
    for key, value in update_data.items():
        setattr(client, key, value)

    db.commit()
    db.refresh(client)

    return client


# remove um cliente
@router.delete("/{client_id}")
def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(status_code=404, detail="cliente não encontrado")

    db.delete(client)
    db.commit()

    return {"message": "cliente deletado com sucesso"}