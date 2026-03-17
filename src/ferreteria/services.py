"""
Servicios de lógica de negocio para la gestión del inventario.

Este módulo contiene la capa de servicios del sistema, responsable
de implementar las reglas de negocio relacionadas con la gestión
de productos en el inventario.

La capa de servicios actúa como intermediaria entre la capa de
persistencia (storage) y las interfaces de usuario (CLI).
"""

from typing import List

from .exceptions import (
    DatosProductoInvalidosError,
    ProductoNoEncontradoError,
    ProductoYaExisteError,
)
from .models import Producto
from .storage import Storage


class InventarioService:
    """
    Servicio principal encargado de gestionar la lógica de negocio del inventario.

    Esta clase implementa las operaciones principales sobre los productos,
    incluyendo creación, consulta, actualización y eliminación. También
    aplica las reglas de validación antes de persistir los datos.

    Attributes:
        storage (Storage):
            Componente responsable de la persistencia de los datos del inventario.
    """

    def __init__(self, storage: Storage) -> None:
        """
        Inicializa el servicio de inventario.

        Args:
            storage (Storage):
                Implementación de almacenamiento utilizada para
                cargar y guardar los productos.
        """
        self.storage = storage

    # CREAR
    def crear_producto(self, producto: Producto) -> None:
        """
        Registra un nuevo producto en el inventario.

        Antes de guardar el producto se validan sus datos y se
        verifica que no exista otro producto con el mismo código.

        Args:
            producto (Producto):
                Instancia del producto que se desea registrar.

        Raises:
            DatosProductoInvalidosError:
                Si alguno de los datos del producto no cumple
                con las reglas de validación.

            ProductoYaExisteError:
                Si ya existe un producto registrado con el mismo código.

        Returns:
            None
        """
        self._validar_producto(producto)

        productos = self.storage.load()

        if any(p.codigo == producto.codigo for p in productos):
            raise ProductoYaExisteError(producto.codigo)

        productos.append(producto)
        self.storage.save(productos)

    # LEER
    def listar_productos(self) -> List[Producto]:
        """
        Obtiene la lista completa de productos registrados en el inventario.

        Returns:
            List[Producto]:
                Lista con todos los productos almacenados.
        """
        return self.storage.load()

    def buscar_producto(self, codigo: str) -> Producto:
        """
        Busca un producto en el inventario utilizando su código.

        Args:
            codigo (str):
                Código único del producto.

        Returns:
            Producto:
                Producto encontrado en el inventario.

        Raises:
            ProductoNoEncontradoError:
                Si no existe un producto con el código proporcionado.
        """
        productos = self.storage.load()

        for producto in productos:
            if producto.codigo == codigo:
                return producto

        raise ProductoNoEncontradoError(codigo)

    def calcular_inventario_total(self) -> float:
        """
        Calcula el valor total del inventario.

        El cálculo se realiza multiplicando la cantidad disponible
        de cada producto por su valor unitario.

        Returns:
            float:
                Valor total del inventario.
        """
        productos = self.storage.load()
        return sum(p.cantidad * p.valor for p in productos)

    # ACTUALIZAR
    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: str | None = None,
        nueva_cantidad: int | None = None,
        nuevo_valor: float | None = None,
    ) -> None:
        """
        Actualiza la información de un producto existente.

        Permite modificar el nombre, la cantidad o el valor del
        producto de forma parcial.

        Args:
            codigo (str):
                Código del producto que se desea actualizar.

            nuevo_nombre (str | None):
                Nuevo nombre del producto.

            nueva_cantidad (int | None):
                Nueva cantidad disponible del producto.

            nuevo_valor (float | None):
                Nuevo valor unitario del producto.

        Raises:
            ProductoNoEncontradoError:
                Si el producto con el código indicado no existe.

            DatosProductoInvalidosError:
                Si alguno de los nuevos valores no es válido.

        Returns:
            None
        """
        productos = self.storage.load()

        producto = None
        for p in productos:
            if p.codigo == codigo:
                producto = p
                break

        if producto is None:
            raise ProductoNoEncontradoError(codigo)

        if nuevo_nombre is not None:
            producto.nombre = nuevo_nombre

        if nueva_cantidad is not None:
            if nueva_cantidad < 0:
                raise DatosProductoInvalidosError("La cantidad no puede ser negativa")
            producto.cantidad = nueva_cantidad

        if nuevo_valor is not None:
            if nuevo_valor <= 0:
                raise DatosProductoInvalidosError("El valor debe ser mayor que cero")
            producto.valor = nuevo_valor

        self.storage.save(productos)

    # ELIMINAR
    def eliminar_producto(self, codigo: str) -> None:
        """
        Elimina un producto del inventario.

        Args:
            codigo (str):
                Código del producto que se desea eliminar.

        Raises:
            ProductoNoEncontradoError:
                Si el producto no existe en el inventario.

        Returns:
            None
        """
        productos = self.storage.load()

        filtrados = [p for p in productos if p.codigo != codigo]

        if len(filtrados) == len(productos):
            raise ProductoNoEncontradoError(codigo)

        self.storage.save(filtrados)

    # VALIDACIÓN
    def _validar_producto(self, producto: Producto) -> None:
        """
        Valida los datos de un producto antes de almacenarlo.

        Args:
            producto (Producto):
                Producto que se desea validar.

        Raises:
            DatosProductoInvalidosError:
                Si alguno de los campos del producto es inválido.

        Returns:
            None
        """
        if not producto.codigo.strip():
            raise DatosProductoInvalidosError(
                "El código del producto no puede estar vacío"
            )

        if not producto.nombre.strip():
            raise DatosProductoInvalidosError(
                "El nombre del producto no puede estar vacío"
            )

        if producto.cantidad < 0:
            raise DatosProductoInvalidosError(
                "La cantidad no puede ser negativa"
            )

        if producto.valor <= 0:
            raise DatosProductoInvalidosError(
                "El valor del producto debe ser mayor a cero"
            )