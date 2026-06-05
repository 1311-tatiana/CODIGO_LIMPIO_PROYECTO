"""Pruebas de integracion para los endpoints de productos."""

from fastapi.testclient import TestClient

from src.api.dependencies import get_producto_service
from src.api.main import app
from src.services.services import ProductoService
from src.storage.storage import JSONProductoRepository


def create_test_client(tmp_path):
    repository = JSONProductoRepository(tmp_path / "database.json")
    service = ProductoService(repository)
    app.dependency_overrides[get_producto_service] = lambda: service
    return TestClient(app)


def test_health(tmp_path):
    client = create_test_client(tmp_path)

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["message"] == "API funcionando correctamente"

    app.dependency_overrides.clear()


def test_home_page(tmp_path):
    client = create_test_client(tmp_path)

    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert "Gestión de productos" in response.text

    app.dependency_overrides.clear()


def test_crud_products(tmp_path):
    client = create_test_client(tmp_path)

    create_response = client.post(
        "/products/",
        json={
            "codigo": "P001",
            "nombre": "Martillo",
            "cantidad": 10,
            "valor": 15000.0,
        },
    )
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    list_response = client.get("/products/")
    assert list_response.status_code == 200
    assert len(list_response.json()) == 1

    get_response = client.get(f"/products/{product_id}")
    assert get_response.status_code == 200
    assert get_response.json()["codigo"] == "P001"

    update_response = client.put(f"/products/{product_id}", json={"cantidad": 15})
    assert update_response.status_code == 200
    assert update_response.json()["cantidad"] == 15

    total_response = client.get("/products/total-value")
    assert total_response.status_code == 200
    assert total_response.json()["total"] == 225000.0

    delete_response = client.delete(f"/products/{product_id}")
    assert delete_response.status_code == 204

    missing_response = client.get(f"/products/{product_id}")
    assert missing_response.status_code == 404

    app.dependency_overrides.clear()