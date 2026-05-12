"""
Configuración compartida para las pruebas unitarias.

Este módulo contiene fixtures reutilizables para simplificar
la creación de productos y servicios mockeados durante
la ejecución de los tests.
"""

from unittest.mock import MagicMock

import pytest

from src.schemas.producto import Producto
from src.services.services import InventarioService


@pytest.fixture
def producto_valido():
    """
    Retorna un producto válido para pruebas.

    Returns:
        Producto:
            Instancia válida de producto.
    """

    return Producto(
        codigo="P001",
        nombre="Martillo",
        cantidad=10,
        valor=15000.0
    )


@pytest.fixture
def mock_storage():
    """
    Crea un almacenamiento simulado.

    Returns:
        MagicMock:
            Mock del sistema de almacenamiento.
    """

    storage = MagicMock()
    storage.load.return_value = []

    return storage


@pytest.fixture
def inventario_service(mock_storage):
    """
    Crea una instancia del servicio de inventario.

    Args:
        mock_storage (MagicMock):
            Mock del almacenamiento.

    Returns:
        InventarioService:
            Servicio configurado para pruebas.
    """

    return InventarioService(mock_storage)