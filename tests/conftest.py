"""Fixtures compartidos para pruebas."""

import pytest

from src.schemas.producto import ProductoCreate
from src.services.services import ProductoService
from src.storage.storage import JSONProductoRepository


@pytest.fixture
def producto_valido() -> ProductoCreate:
    return ProductoCreate(codigo="P001", nombre="Martillo", cantidad=10, valor=15000.0)


@pytest.fixture
def producto_service(tmp_path) -> ProductoService:
    repository = JSONProductoRepository(tmp_path / "database.json")
    return ProductoService(repository)
