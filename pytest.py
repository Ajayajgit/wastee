import pytest
from fastapi import status
from main import app

@pytest.fixture
def client():
    with TestClient(app) as client:
        yield client

def test_get_menu(client):
    response = client.get("/menu?name=Margherita")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "Margherita"

def test_get_nonexistent_menu_item(client):
    response = client.get("/menu?name=NonexistentPizza")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_place_order(client):
    order_data = [{"id": 1, "quantity": 2}, {"id": 2, "quantity": 1}]
    response = client.post("/order", json=order_data)
    assert response.status_code == status.HTTP_200_OK
    assert "order_id" in response.json()
    assert "price" in response.json()

def test_place_invalid_order(client):
    order_data = [{"id": 100, "quantity": 2}]
    response = client.post("/order", json=order_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
