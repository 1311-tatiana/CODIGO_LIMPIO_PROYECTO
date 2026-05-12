"""
Servicios de lógica de negocio para la gestión del inventario.

Este módulo contiene la capa de servicios del sistema, responsable
de implementar las reglas de negocio relacionadas con la gestión
de productos en el inventario.

La capa de servicios actúa como intermediaria entre la capa de
persistencia (storage) y las interfaces de usuario (CLI).
"""

from typing import List

from src.core.exceptions import (
    DatosProductoInvalidosError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
)

from src.schemas.producto import Producto
from src.storage.storage import Storage


class InventarioService:
    """
    Servicio principal encargado de gestionar la lógica de negocio del inventario.

    Esta clase implementa las operaciones principales sobre los productos,
    incluyendo creación, consulta, actualización y eliminación.

    Attributes:
        storage (Storage):
            Componente responsable de la persistencia de los datos.
    """

    def __init__(self, storage: Storage) -> None:
        """
        Inicializa el servicio de inventario.

        Args:
            storage (Storage):
                Implementación de almacenamiento utilizada para
                cargar y guardar productos.

        Returns:
            None
        """

        self.storage = storage

    def _validar_producto(self, producto: Producto) -> None:
        """
        Valida que los datos del producto sean correctos.

        Args:
            producto (Producto):
                Producto a validar.

        Raises:
            DatosProductoInvalidosError:
                Si algún dato del producto es inválido.

        Returns:
            None
        """

        if not producto.nombre.strip():
            raise DatosProductoInvalidosError(
                "El nombre no puede estar vacío"
            )

        if producto.cantidad < 0:
            raise DatosProductoInvalidosError(
                "La cantidad no puede ser negativa"
            )

        if producto.valor <= 0:
            raise DatosProductoInvalidosError(
                "El valor debe ser mayor que cero"
            )

    def _verificar_codigo_unico(
        self,
        codigo: str,
        productos: List[Producto]
    ) -> None:
        """
        Verifica que el código del producto no exista.

        Args:
            codigo (str):
                Código del producto.

            productos (List[Producto]):
                Lista de productos registrados.

        Raises:
            ProductoYaExisteError:
                Si el código ya existe.

        Returns:
            None
        """

        if any(p.codigo == codigo for p in productos):
            raise ProductoYaExisteError(codigo)

    def crear_producto(self, producto: Producto) -> None:
        """
        Registra un nuevo producto en el inventario.

        Args:
            producto (Producto):
                Producto a registrar.

        Raises:
            ProductoYaExisteError:
                Si ya existe un producto con el mismo código.

            DatosProductoInvalidosError:
                Si los datos son inválidos.

        Returns:
            None
        """

        self._validar_producto(producto)

        productos = self.storage.load()

        self._verificar_codigo_unico(
            producto.codigo,
            productos
        )

        productos.append(producto)

        self.storage.save(productos)

    def listar_productos(self) -> List[Producto]:
        """
        Obtiene todos los productos del inventario.

        Returns:
            List[Producto]:
                Lista de productos registrados.
        """

        return self.storage.load()

    def buscar_producto(self, codigo: str) -> Producto:
        """
        Busca un producto utilizando su código.

        Args:
            codigo (str):
                Código único del producto.

        Returns:
            Producto:
                Producto encontrado.

        Raises:
            ProductoNoEncontradoError:
                Si el producto no existe.
        """

        productos = self.storage.load()

        for producto in productos:

            if producto.codigo == codigo:
                return producto

        raise ProductoNoEncontradoError(codigo)

    def calcular_inventario_total(self) -> float:
        """
        Calcula el valor total del inventario.

        Returns:
            float:
                Valor total del inventario.
        """

        productos = self.storage.load()

        return sum(
            p.cantidad * p.valor
            for p in productos
        )

    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: str,
        nueva_cantidad: int,
        nuevo_valor: float
    ) -> None:
        """
        Actualiza un producto existente.

        Args:
            codigo (str):
                Código del producto.

            nuevo_nombre (str):
                Nuevo nombre del producto.

            nueva_cantidad (int):
                Nueva cantidad disponible.

            nuevo_valor (float):
                Nuevo valor unitario.

        Raises:
            ProductoNoEncontradoError:
                Si el producto no existe.

            DatosProductoInvalidosError:
                Si los nuevos datos son inválidos.

        Returns:
            None
        """

        productos = self.storage.load()

        producto = self.buscar_producto(codigo)

        if not nuevo_nombre.strip():
            raise DatosProductoInvalidosError(
                "El nombre no puede estar vacío"
            )

        if nueva_cantidad < 0:
            raise DatosProductoInvalidosError(
                "La cantidad no puede ser negativa"
            )

        if nuevo_valor <= 0:
            raise DatosProductoInvalidosError(
                "El valor debe ser mayor que cero"
            )

        producto.nombre = nuevo_nombre
        producto.cantidad = nueva_cantidad
        producto.valor = nuevo_valor

        self.storage.save(productos)

    def eliminar_producto(self, codigo: str) -> None:
        """
        Elimina un producto del inventario.

        Args:
            codigo (str):
                Código del producto que se desea eliminar.

        Raises:
            ProductoNoEncontradoError:
                Si el producto no existe.

        Returns:
            None
        """

        productos = self.storage.load()

        filtrados = [
            p for p in productos
            if p.codigo != codigo
        ]

        if len(filtrados) == len(productos):
            raise ProductoNoEncontradoError(codigo)

        self.storage.save(filtrados)