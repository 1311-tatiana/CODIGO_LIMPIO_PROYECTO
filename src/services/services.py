"""Capa de servicios con la logica de negocio de productos."""

from src.core.exceptions import ProductoNoEncontradoError, ProductoYaExisteError
from src.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from src.storage.storage import ProductoRepository


class ProductoService:
    """Servicio principal para gestionar productos del inventario."""

    def __init__(self, repository: ProductoRepository) -> None:
        self.repository = repository

    def listar_productos(self) -> list[ProductoResponse]:
        """Obtiene todos los productos registrados."""

        return self.repository.list()

    def obtener_producto(self, producto_id: int) -> ProductoResponse:
        """Obtiene un producto por su id."""

        producto = self.repository.get_by_id(producto_id)
        if producto is None:
            raise ProductoNoEncontradoError(producto_id)
        return producto

    def buscar_producto_por_codigo(self, codigo: str) -> ProductoResponse:
        """Obtiene un producto por su codigo unico."""

        producto = self.repository.get_by_codigo(codigo)
        if producto is None:
            raise ProductoNoEncontradoError(codigo)
        return producto

    def crear_producto(self, producto: ProductoCreate) -> ProductoResponse:
        """Crea un producto validando que su codigo sea unico."""

        existente = self.repository.get_by_codigo(producto.codigo)
        if existente is not None:
            raise ProductoYaExisteError(producto.codigo)
        return self.repository.create(producto)

    def actualizar_producto(self, producto_id: int, data: ProductoUpdate) -> ProductoResponse:
        """Actualiza un producto existente."""

        actual = self.obtener_producto(producto_id)

        if data.codigo and data.codigo != actual.codigo:
            existente = self.repository.get_by_codigo(data.codigo)
            if existente is not None and existente.id != producto_id:
                raise ProductoYaExisteError(data.codigo)

        actualizado = self.repository.update(producto_id, data)
        if actualizado is None:
            raise ProductoNoEncontradoError(producto_id)
        return actualizado

    def eliminar_producto(self, producto_id: int) -> None:
        """Elimina un producto por id."""

        eliminado = self.repository.delete(producto_id)
        if not eliminado:
            raise ProductoNoEncontradoError(producto_id)

    def calcular_valor_total(self) -> float:
        """Calcula el valor total del inventario."""

        return sum(producto.cantidad * producto.valor for producto in self.listar_productos())


# Alias temporal para compatibilidad con pruebas o imports antiguos.
InventarioService = ProductoService
