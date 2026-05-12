"""
Pruebas unitarias para el servicio de inventario.

Este módulo contiene pruebas destinadas a validar el comportamiento
de la lógica de negocio implementada en la clase `InventarioService`.

Las pruebas cubren los siguientes casos:

- Creación de productos
- Validación de datos
- Búsqueda de productos
- Listado de inventario
- Cálculo del valor total
- Actualización de productos
- Eliminación de productos

Para aislar las pruebas de la persistencia, se utiliza
`MagicMock` para simular el almacenamiento.
"""

from unittest.mock import MagicMock

import pytest

from src.core.exceptions import (
    DatosProductoInvalidosError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
)

from src.schemas.producto import Producto
from src.services.services import InventarioService


def make_service(productos=None):
    """
    Crea una instancia del servicio utilizando
    almacenamiento simulado.

    Args:
        productos (list[Producto] | None):
            Lista inicial de productos.

    Returns:
        InventarioService:
            Servicio configurado con mock.
    """

    mock_storage = MagicMock()

    mock_storage.load.return_value = (
        productos if productos is not None else []
    )

    return InventarioService(mock_storage)


def producto_valido(**kwargs):
    """
    Genera un producto válido para pruebas.

    Args:
        **kwargs:
            Valores personalizados del producto.

    Returns:
        Producto:
            Instancia válida de producto.
    """

    defaults = {
        "codigo": "P001",
        "nombre": "Martillo",
        "cantidad": 10,
        "valor": 15000.0,
    }

    defaults.update(kwargs)

    return Producto(**defaults)


def test_crear_producto_exitoso():
    """
    Verifica que un producto válido
    pueda registrarse correctamente.

    Returns:
        None
    """

    service = make_service()

    service.crear_producto(producto_valido())

    service.storage.save.assert_called_once()


def test_crear_producto_codigo_duplicado():
    """
    Verifica que no se permita registrar
    un producto con código duplicado.

    Raises:
        ProductoYaExisteError:
            Si el código ya existe.

    Returns:
        None
    """

    service = make_service([producto_valido()])

    with pytest.raises(ProductoYaExisteError):

        service.crear_producto(producto_valido())

    service.storage.save.assert_not_called()


def test_crear_producto_nombre_vacio():
    """
    Verifica que no se permita crear
    productos con nombre vacío.

    Raises:
        DatosProductoInvalidosError:
            Si el nombre es inválido.

    Returns:
        None
    """

    service = make_service()

    with pytest.raises(DatosProductoInvalidosError):

        service.crear_producto(
            producto_valido(nombre="   ")
        )


def test_crear_producto_cantidad_negativa():
    """
    Verifica que no se permitan
    cantidades negativas.

    Raises:
        DatosProductoInvalidosError:
            Si la cantidad es negativa.

    Returns:
        None
    """

    service = make_service()

    with pytest.raises(DatosProductoInvalidosError):

        service.crear_producto(
            producto_valido(cantidad=-5)
        )


def test_crear_producto_valor_cero():
    """
    Verifica que no se permitan
    valores iguales a cero.

    Raises:
        DatosProductoInvalidosError:
            Si el valor es inválido.

    Returns:
        None
    """

    service = make_service()

    with pytest.raises(DatosProductoInvalidosError):

        service.crear_producto(
            producto_valido(valor=0)
        )

def test_listar_productos_retorna_lista():
    """
    Verifica que el sistema retorne
    todos los productos registrados.

    Returns:
        None
    """

    productos = [
        producto_valido(),

        producto_valido(
            codigo="P002",
            nombre="Tornillo"
        ),
    ]

    service = make_service(productos)

    resultado = service.listar_productos()

    assert len(resultado) == 2


def test_buscar_producto_exitoso():
    """
    Verifica que un producto pueda
    encontrarse mediante su código.

    Returns:
        None
    """

    service = make_service([producto_valido()])

    resultado = service.buscar_producto("P001")

    assert resultado.nombre == "Martillo"


def test_buscar_producto_no_encontrado():
    """
    Verifica que se genere una excepción
    cuando el producto no existe.

    Raises:
        ProductoNoEncontradoError:
            Si el producto no existe.

    Returns:
        None
    """

    service = make_service()

    with pytest.raises(ProductoNoEncontradoError):

        service.buscar_producto("XXXX")


def test_calcular_inventario_total():
    """
    Verifica el cálculo total del inventario.

    Returns:
        None
    """

    productos = [
        producto_valido(
            cantidad=2,
            valor=10000.0
        ),

        producto_valido(
            codigo="P002",
            nombre="Pala",
            cantidad=3,
            valor=5000.0
        ),
    ]

    service = make_service(productos)

    assert service.calcular_inventario_total() == 35000.0

def test_actualizar_producto_exitoso():
    """
    Verifica que un producto existente
    pueda actualizarse correctamente.

    Returns:
        None
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
    Verifica que no se puedan actualizar
    productos inexistentes.

    Raises:
        ProductoNoEncontradoError:
            Si el producto no existe.

    Returns:
        None
    """

    service = make_service()

    with pytest.raises(ProductoNoEncontradoError):

        service.actualizar_producto(
            "XXXX",
            nuevo_nombre="Nuevo",
            nueva_cantidad=10,
            nuevo_valor=1000.0
        )

def test_eliminar_producto_exitoso():
    """
    Verifica que un producto pueda
    eliminarse correctamente.

    Returns:
        None
    """

    service = make_service([producto_valido()])

    service.eliminar_producto("P001")

    service.storage.save.assert_called_once()


def test_eliminar_producto_no_encontrado():
    """
    Verifica que no se puedan eliminar
    productos inexistentes.

    Raises:
        ProductoNoEncontradoError:
            Si el producto no existe.

    Returns:
        None
    """

    service = make_service()

    with pytest.raises(ProductoNoEncontradoError):

        service.eliminar_producto("XXXX")