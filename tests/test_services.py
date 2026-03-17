"""
Pruebas unitarias para el servicio de inventario.

Este módulo contiene pruebas destinadas a validar el comportamiento
de la lógica de negocio implementada en la clase `InventarioService`.

Las pruebas cubren los siguientes casos:

- Creación de productos
- Validación de datos de productos
- Búsqueda de productos en el inventario
- Listado de productos
- Cálculo del valor total del inventario
- Actualización de productos
- Eliminación de productos

Para aislar las pruebas de la capa de persistencia, se utiliza
`MagicMock` para simular el comportamiento del almacenamiento.
"""

from unittest.mock import MagicMock

import pytest

from src.ferreteria.exceptions import (
    DatosProductoInvalidosError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
)
from src.ferreteria.models import Producto
from src.ferreteria.services import InventarioService


# Helpers


def make_service(productos=None):
    """
    Crea una instancia de InventarioService utilizando un almacenamiento simulado.

    Este helper utiliza MagicMock para reemplazar la capa de persistencia,
    permitiendo ejecutar las pruebas sin interactuar con archivos reales.

    Args:
        productos (list[Producto] | None):
            Lista inicial de productos que será retornada por el método load().

    Returns:
        InventarioService:
            Instancia del servicio configurada con almacenamiento mockeado.
    """
    mock_storage = MagicMock()
    mock_storage.load.return_value = productos if productos is not None else []
    return InventarioService(mock_storage)


def producto_valido(**kwargs):
    """
    Genera un objeto Producto con datos válidos para pruebas.

    Los valores por defecto pueden ser sobrescritos mediante argumentos
    keyword, lo que permite crear variaciones del producto en los tests.

    Args:
        **kwargs:
            Campos del producto que se desean modificar.

    Returns:
        Producto:
            Instancia de Producto con datos válidos.
    """
    defaults = dict(codigo="P001", nombre="Martillo", cantidad=10, valor=15000.0)
    defaults.update(kwargs)
    return Producto(**defaults)


# CREAR


def test_crear_producto_exitoso():
    """
    Caso normal: crear un producto válido debe guardarlo sin errores.
    """
    service = make_service()

    service.crear_producto(producto_valido())

    service.storage.save.assert_called_once()


def test_crear_producto_codigo_duplicado():
    """
    Caso error: crear un producto con un código ya existente
    debe lanzar la excepción ProductoYaExisteError.
    """
    service = make_service([producto_valido()])

    with pytest.raises(ProductoYaExisteError):
        service.crear_producto(producto_valido())

    service.storage.save.assert_not_called()


def test_crear_producto_nombre_vacio():
    """
    Caso error: si el nombre del producto está vacío,
    debe lanzarse la excepción DatosProductoInvalidosError.
    """
    service = make_service()

    with pytest.raises(DatosProductoInvalidosError):
        service.crear_producto(producto_valido(nombre="   "))


def test_crear_producto_cantidad_negativa():
    """
    Caso extraordinario: una cantidad negativa no es válida
    y debe generar una excepción DatosProductoInvalidosError.
    """
    service = make_service()

    with pytest.raises(DatosProductoInvalidosError):
        service.crear_producto(producto_valido(cantidad=-5))


def test_crear_producto_valor_cero():
    """
    Caso error: si el valor del producto es igual a cero,
    el sistema debe lanzar DatosProductoInvalidosError.
    """
    service = make_service()

    with pytest.raises(DatosProductoInvalidosError):
        service.crear_producto(producto_valido(valor=0))


# LEER


def test_listar_productos_retorna_lista():
    """
    Caso normal: listar productos debe retornar
    todos los productos almacenados en el inventario.
    """
    productos = [
        producto_valido(),
        producto_valido(codigo="P002", nombre="Tornillo"),
    ]

    service = make_service(productos)

    resultado = service.listar_productos()

    assert len(resultado) == 2


def test_buscar_producto_exitoso():
    """
    Caso normal: buscar un producto por un código existente
    debe retornar el producto correcto.
    """
    service = make_service([producto_valido()])

    resultado = service.buscar_producto("P001")

    assert resultado.nombre == "Martillo"


def test_buscar_producto_no_encontrado():
    """
    Caso error: buscar un producto con un código inexistente
    debe lanzar la excepción ProductoNoEncontradoError.
    """
    service = make_service()

    with pytest.raises(ProductoNoEncontradoError):
        service.buscar_producto("XXXX")


def test_calcular_inventario_total():
    """
    Caso normal: el total del inventario debe calcularse
    como la suma de cantidad por valor de cada producto.
    """
    productos = [
        producto_valido(cantidad=2, valor=10000.0),
        producto_valido(codigo="P002", nombre="Pala", cantidad=3, valor=5000.0),
    ]

    service = make_service(productos)

    assert service.calcular_inventario_total() == 35000.0


# ACTUALIZAR


def test_actualizar_producto_exitoso():
    """
    Caso normal: actualizar los datos de un producto existente
    debe modificar su información correctamente.
    """
    service = make_service([producto_valido()])

    service.actualizar_producto(
        "P001",
        nuevo_nombre="Martillo Grande",
        nueva_cantidad=50,
        nuevo_valor=18000.0,
    )

    service.storage.save.assert_called_once()


def test_actualizar_producto_no_encontrado():
    """
    Caso error: intentar actualizar un producto que no existe
    debe lanzar la excepción ProductoNoEncontradoError.
    """
    service = make_service()

    with pytest.raises(ProductoNoEncontradoError):
        service.actualizar_producto("XXXX", nueva_cantidad=10)


# ELIMINAR


def test_eliminar_producto_exitoso():
    """
    Caso normal: eliminar un producto existente
    debe removerlo del almacenamiento.
    """
    service = make_service([producto_valido()])

    service.eliminar_producto("P001")

    service.storage.save.assert_called_once()


def test_eliminar_producto_no_encontrado():
    """
    Caso error: intentar eliminar un producto con código inexistente
    debe lanzar la excepción ProductoNoEncontradoError.
    """
    service = make_service()

    with pytest.raises(ProductoNoEncontradoError):
        service.eliminar_producto("XXXX")