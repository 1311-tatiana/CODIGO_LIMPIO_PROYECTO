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
    Servicio principal encargado de gestionar la lógica
    de negocio del inventario.

    Esta clase implementa las operaciones principales
    sobre los productos, incluyendo creación, consulta,
    actualización y eliminación. También aplica las
    reglas de validación antes de persistir los datos.

    Attributes:
        storage (Storage):
            Componente responsable de la persistencia
            de los datos del inventario.
    """

    def __init__(self, storage: Storage) -> None:
        """
        Inicializa el servicio de inventario.

        Args:
            storage (Storage):
                Implementación de almacenamiento utilizada
                para cargar y guardar los productos.

        Returns:
            None
        """

        self.storage = storage

    # ==================================================
    # VALIDADORES PRIVADOS
    # ==================================================

    def _validar_producto(self, producto: Producto) -> None:
        """
        Valida que los datos del producto sean correctos.

        Args:
            producto (Producto):
                Producto a validar.

        Raises:
            DatosProductoInvalidosError:
                Si algún campo no es válido.

        Returns:
            None
        """

        if not producto.nombre or not producto.nombre.strip():

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
        Verifica que no exista otro producto
        con el mismo código.

        Args:
            codigo (str):
                Código a verificar.

            productos (List[Producto]):
                Lista actual de productos.

        Raises:
            ProductoYaExisteError:
                Si el código ya está registrado.

        Returns:
            None
        """

        if any(p.codigo == codigo for p in productos):

            raise ProductoYaExisteError(codigo)

    def _actualizar_nombre(
        self,
        producto: Producto,
        nuevo_nombre: str | None
    ) -> None:
        """
        Actualiza el nombre del producto si se
        proporcionó uno nuevo.

        Args:
            producto (Producto):
                Producto a modificar.

            nuevo_nombre (str | None):
                Nuevo nombre del producto.

        Raises:
            DatosProductoInvalidosError:
                Si el nombre está vacío.

        Returns:
            None
        """

        if nuevo_nombre is not None:

            if not nuevo_nombre.strip():

                raise DatosProductoInvalidosError(
                    "El nombre no puede estar vacío"
                )

            producto.nombre = nuevo_nombre

    def _actualizar_cantidad(
        self,
        producto: Producto,
        nueva_cantidad: int | None
    ) -> None:
        """
        Actualiza la cantidad del producto si se
        proporcionó un valor nuevo.

        Args:
            producto (Producto):
                Producto a modificar.

            nueva_cantidad (int | None):
                Nueva cantidad del producto.

        Raises:
            DatosProductoInvalidosError:
                Si la cantidad es negativa.

        Returns:
            None
        """

        if nueva_cantidad is None:
            return

        if nueva_cantidad < 0:

            raise DatosProductoInvalidosError(
                "La cantidad no puede ser negativa"
            )

        producto.cantidad = nueva_cantidad

    def _actualizar_valor(
        self,
        producto: Producto,
        nuevo_valor: float | None
    ) -> None:
        """
        Actualiza el valor del producto si se
        proporcionó un valor nuevo.

        Args:
            producto (Producto):
                Producto a modificar.

            nuevo_valor (float | None):
                Nuevo valor del producto.

        Raises:
            DatosProductoInvalidosError:
                Si el valor es cero o negativo.

        Returns:
            None
        """

        if nuevo_valor is None:
            return

        if nuevo_valor <= 0:

            raise DatosProductoInvalidosError(
                "El valor debe ser mayor que cero"
            )

        producto.valor = nuevo_valor

    def _aplicar_cambios(
        self,
        producto: Producto,
        nuevo_nombre: str | None,
        nueva_cantidad: int | None,
        nuevo_valor: float | None,
    ) -> None:
        """
        Aplica cambios parciales a un producto existente.

        Args:
            producto (Producto):
                Producto a modificar.

            nuevo_nombre (str | None):
                Nuevo nombre del producto.

            nueva_cantidad (int | None):
                Nueva cantidad disponible.

            nuevo_valor (float | None):
                Nuevo valor unitario.

        Raises:
            DatosProductoInvalidosError:
                Si alguno de los nuevos valores no es válido.

        Returns:
            None
        """

        self._actualizar_nombre(
            producto,
            nuevo_nombre
        )

        self._actualizar_cantidad(
            producto,
            nueva_cantidad
        )

        self._actualizar_valor(
            producto,
            nuevo_valor
        )

    # ==================================================
    # CREAR
    # ==================================================

    def crear_producto(self, producto: Producto) -> None:
        """
        Registra un nuevo producto en el inventario.

        Args:
            producto (Producto):
                Instancia del producto que se desea registrar.

        Raises:
            ProductoYaExisteError:
                Si ya existe un producto registrado
                con el mismo código.

            DatosProductoInvalidosError:
                Si los datos del producto no son válidos.

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

    # ==================================================
    # LEER
    # ==================================================

    def listar_productos(self) -> List[Producto]:
        """
        Obtiene la lista completa de productos
        registrados en el inventario.

        Returns:
            List[Producto]:
                Lista con todos los productos almacenados.
        """

        return self.storage.load()

    def buscar_producto(self, codigo: str) -> Producto:
        """
        Busca un producto en el inventario
        utilizando su código.

        Args:
            codigo (str):
                Código único del producto.

        Returns:
            Producto:
                Producto encontrado en el inventario.

        Raises:
            ProductoNoEncontradoError:
                Si no existe un producto con el código
                proporcionado.
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

    # ==================================================
    # ACTUALIZAR
    # ==================================================

    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: str | None = None,
        nueva_cantidad: int | None = None,
        nuevo_valor: float | None = None,
    ) -> None:
        """
        Actualiza la información de un producto existente.

        Args:
            codigo (str):
                Código del producto que se desea actualizar.

            nuevo_nombre (str | None):
                Nuevo nombre del producto.

            nueva_cantidad (int | None):
                Nueva cantidad disponible.

            nuevo_valor (float | None):
                Nuevo valor unitario.

        Raises:
            ProductoNoEncontradoError:
                Si el producto no existe.

            DatosProductoInvalidosError:
                Si alguno de los nuevos valores no es válido.

        Returns:
            None
        """

        productos = self.storage.load()

        producto = self.buscar_producto(codigo)

        self._aplicar_cambios(
            producto,
            nuevo_nombre,
            nueva_cantidad,
            nuevo_valor
        )

        self.storage.save(productos)

    # ==================================================
    # ELIMINAR
    # ==================================================

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

        filtrados = [
            p for p in productos
            if p.codigo != codigo
        ]

        if len(filtrados) == len(productos):

            raise ProductoNoEncontradoError(codigo)

        self.storage.save(filtrados)