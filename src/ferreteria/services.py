from typing import List

from .exceptions import (
    DatosProductoInvalidosError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
)
from .models import Producto
from .storage import Storage


class InventarioService:
    """Servicio principal que gestiona la lógica de negocio del inventario."""

    def __init__(self, storage: Storage) -> None:
        self.storage = storage

    #CREAR 
    def crear_producto(self, producto: Producto) -> None:

        self._validar_producto(producto)

        productos = self.storage.load()

        if any(p.codigo == producto.codigo for p in productos):
            raise ProductoYaExisteError(producto.codigo)

        productos.append(producto)
        self.storage.save(productos)

    # LEER 
    def listar_productos(self) -> List[Producto]:
        return self.storage.load()

    def buscar_producto(self, codigo: str) -> Producto:

        productos = self.storage.load()
        for producto in productos:
            if producto.codigo == codigo:
                return producto
        raise ProductoNoEncontradoError(codigo)

    # ACTUALIZAR

    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: str = None,
        nueva_cantidad: int = None,
        nuevo_valor: float = None,
    ) -> None:

        productos = self.storage.load()
        encontrado = False

        for producto in productos:
            if producto.codigo == codigo:
                if nuevo_nombre is not None:
                    if not nuevo_nombre.strip():
                        raise DatosProductoInvalidosError(
                            "El nombre del producto no puede estar vacío"
                        )
                    producto.nombre = nuevo_nombre.strip()

                if nueva_cantidad is not None:
                    if nueva_cantidad < 0:
                        raise DatosProductoInvalidosError(
                            "La cantidad no puede ser negativa"
                        )
                    producto.cantidad = nueva_cantidad

                if nuevo_valor is not None:
                    if nuevo_valor <= 0:
                        raise DatosProductoInvalidosError(
                            "El valor del producto debe ser mayor a cero"
                        )
                    producto.valor = nuevo_valor

                encontrado = True
                break

        if not encontrado:
            raise ProductoNoEncontradoError(codigo)

        self.storage.save(productos)

    #ELIMINAR

    def eliminar_producto(self, codigo: str) -> None:
        """Elimina un producto del inventario por su código"""
        productos = self.storage.load()
        filtrados = [p for p in productos if p.codigo != codigo]

        if len(filtrados) == len(productos):
            raise ProductoNoEncontradoError(codigo)

        self.storage.save(filtrados)

    # VALIDACIÓN 

    def _validar_producto(self, producto: Producto) -> None:
        """Valida los campos de un producto antes de persistirlo."""

        if not producto.codigo.strip():
            raise DatosProductoInvalidosError("El código del producto no puede estar vacío")

        if not producto.nombre.strip():
            raise DatosProductoInvalidosError("El nombre del producto no puede estar vacío")

        if producto.cantidad < 0:
            raise DatosProductoInvalidosError("La cantidad no puede ser negativa")

        if producto.valor <= 0:
            raise DatosProductoInvalidosError(
                "El valor del producto debe ser mayor a cero"
            )
