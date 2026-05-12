"""
Pruebas de integración para los routers.

Este módulo contiene pruebas básicas para validar
las rutas principales de la aplicación.
"""

from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_root():
    """
    Verifica que la ruta principal responda correctamente.
    """

    response = client.get("/")

    assert response.status_code == 200