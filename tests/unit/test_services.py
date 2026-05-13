"""Pruebas unitarias del servicio de productos."""

import pytest

from src.core.exceptions import ProductoNoEncontradoError, ProductoYaExisteError
from src.schemas.producto import ProductoCreate, ProductoUpdate


def test_crear_producto_exitoso(producto_service, producto_valido):
    producto = producto_service.crear_producto(producto_valido)

    assert producto.id == 1
    assert producto.codigo == "P001"
    assert producto.nombre == "Martillo"


def test_crear_producto_codigo_duplicado(producto_service, producto_valido):
    producto_service.crear_producto(producto_valido)

    with pytest.raises(ProductoYaExisteError):
        producto_service.crear_producto(producto_valido)


def test_listar_productos(producto_service, producto_valido):
    producto_service.crear_producto(producto_valido)

    productos = producto_service.listar_productos()

    assert len(productos) == 1
    assert productos[0].codigo == "P001"


def test_obtener_producto_por_id(producto_service, producto_valido):
    creado = producto_service.crear_producto(producto_valido)

    encontrado = producto_service.obtener_producto(creado.id)

    assert encontrado.codigo == "P001"


def test_obtener_producto_inexistente(producto_service):
    with pytest.raises(ProductoNoEncontradoError):
        producto_service.obtener_producto(999)


def test_actualizar_producto(producto_service, producto_valido):
    creado = producto_service.crear_producto(producto_valido)

    actualizado = producto_service.actualizar_producto(
        creado.id,
        ProductoUpdate(nombre="Martillo Grande", cantidad=5),
    )

    assert actualizado.nombre == "Martillo Grande"
    assert actualizado.cantidad == 5
    assert actualizado.valor == 15000.0


def test_eliminar_producto(producto_service, producto_valido):
    creado = producto_service.crear_producto(producto_valido)

    producto_service.eliminar_producto(creado.id)

    with pytest.raises(ProductoNoEncontradoError):
        producto_service.obtener_producto(creado.id)


def test_calcular_valor_total(producto_service):
    producto_service.crear_producto(
        ProductoCreate(codigo="P001", nombre="Martillo", cantidad=10, valor=15000.0)
    )
    producto_service.crear_producto(
        ProductoCreate(codigo="P002", nombre="Taladro", cantidad=2, valor=100000.0)
    )

    assert producto_service.calcular_valor_total() == 350000.0
