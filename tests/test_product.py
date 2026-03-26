from fastapi.testclient import TestClient

from app.main import app

# cria cliente de teste da API
client = TestClient(app)


# testa criação de produto
def test_create_product():
    response = client.post(
        "/products/",
        json={
            "name": "produto teste",
            "description": "teste",
            "price": 100
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "produto teste"
    assert data["price"] == 100
    assert "id" in data


# testa listagem de produtos
def test_get_products():
    response = client.get("/products/")

    assert response.status_code == 200
    assert isinstance(response.json(), list)