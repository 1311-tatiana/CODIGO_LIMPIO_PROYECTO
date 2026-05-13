"""Dependencias reutilizables de FastAPI."""

from src.services.services import ProductoService
from src.storage.storage import ProductoRepository, build_producto_repository


def get_producto_repository() -> ProductoRepository:
    """Retorna el repositorio configurado para productos."""

    return build_producto_repository()


def get_producto_service() -> ProductoService:
    """Retorna el servicio de productos usado por los routers."""

    return ProductoService(get_producto_repository())
