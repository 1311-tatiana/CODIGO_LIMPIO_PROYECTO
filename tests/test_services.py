# tests/test_services.py
import pytest
from unittest.mock import MagicMock

from src.ferreteria.exceptions import (
    DatosProductoInvalidosError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
)
from src.ferreteria.models import Producto
from src.ferreteria.services import InventarioService


#  Helpers

def make_service(productos=None):
    """Crea un InventarioService con storage mockeado."""
    mock_storage = MagicMock()
    mock_storage.load.return_value = productos if productos is not None else []
    return InventarioService(mock_storage)


def producto_valido(**kwargs):
    """Retorna un Producto con datos válidos, sobreescribibles por kwargs."""
    defaults = dict(codigo="P001", nombre="Martillo", cantidad=10, valor=15000.0)
    defaults.update(kwargs)
    return Producto(**defaults)


#  CREAR 

def test_crear_producto_exitoso():
    """Caso normal: crear un producto válido debe guardarlo sin errores."""
    service = make_service()
    service.crear_producto(producto_valido())
    service.storage.save.assert_called_once()


def test_crear_producto_codigo_duplicado():
    """Caso error: crear con código ya existente lanza ProductoYaExisteError."""
    service = make_service([producto_valido()])
    with pytest.raises(ProductoYaExisteError):
        service.crear_producto(producto_valido())
    service.storage.save.assert_not_called()


def test_crear_producto_nombre_vacio():
    """Caso error: nombre vacío lanza DatosProductoInvalidosError."""
    service = make_service()
    with pytest.raises(DatosProductoInvalidosError):
        service.crear_producto(producto_valido(nombre="   "))


def test_crear_producto_cantidad_negativa():
    """Caso extraordinario: cantidad negativa lanza DatosProductoInvalidosError."""
    service = make_service()
    with pytest.raises(DatosProductoInvalidosError):
        service.crear_producto(producto_valido(cantidad=-5))


def test_crear_producto_valor_cero():
    """Caso error: valor igual a 0 lanza DatosProductoInvalidosError."""
    service = make_service()
    with pytest.raises(DatosProductoInvalidosError):
        service.crear_producto(producto_valido(valor=0))


# ──────────────── LEER ────────────────

def test_listar_productos_retorna_lista():
    """Caso normal: listar debe retornar todos los productos almacenados."""
    productos = [producto_valido(), producto_valido(codigo="P002", nombre="Tornillo")]
    service = make_service(productos)
    resultado = service.listar_productos()
    assert len(resultado) == 2


def test_buscar_producto_exitoso():
    """Caso normal: buscar por código existente retorna el producto correcto."""
    service = make_service([producto_valido()])
    resultado = service.buscar_producto("P001")
    assert resultado.nombre == "Martillo"


def test_buscar_producto_no_encontrado():
    """Caso error: buscar código inexistente lanza ProductoNoEncontradoError."""
    service = make_service()
    with pytest.raises(ProductoNoEncontradoError):
        service.buscar_producto("XXXX")


def test_calcular_inventario_total():
    """Caso normal: el total debe ser la suma de cantidad x valor de cada producto."""
    productos = [
        producto_valido(cantidad=2, valor=10000.0),
        producto_valido(codigo="P002", nombre="Pala", cantidad=3, valor=5000.0),
    ]
    service = make_service(productos)
    assert service.calcular_inventario_total() == 35000.0


# ──────────────── ACTUALIZAR ────────────────

def test_actualizar_producto_exitoso():
    """Caso normal: actualizar nombre, cantidad y valor de un producto existente."""
    service = make_service([producto_valido()])
    service.actualizar_producto(
        "P001",
        nuevo_nombre="Martillo Grande",
        nueva_cantidad=50,
        nuevo_valor=18000.0,
    )
    service.storage.save.assert_called_once()


def test_actualizar_producto_no_encontrado():
    """Caso error: actualizar código inexistente lanza ProductoNoEncontradoError."""
    service = make_service()
    with pytest.raises(ProductoNoEncontradoError):
        service.actualizar_producto("XXXX", nueva_cantidad=10)


# ──────────────── ELIMINAR ────────────────

def test_eliminar_producto_exitoso():
    """Caso normal: eliminar un producto existente lo remueve del almacenamiento."""
    service = make_service([producto_valido()])
    service.eliminar_producto("P001")
    service.storage.save.assert_called_once()


def test_eliminar_producto_no_encontrado():
    """Caso error: eliminar código inexistente lanza ProductoNoEncontradoError."""
    service = make_service()
    with pytest.raises(ProductoNoEncontradoError):
        service.eliminar_producto("XXXX")
