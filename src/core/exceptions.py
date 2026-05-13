"""Excepciones de dominio para productos e inventario."""


class AppError(Exception):
    """Excepcion base de la aplicacion."""


class ProductoError(AppError):
    """Error base relacionado con productos."""


class ProductoNoEncontradoError(ProductoError):
    """Se lanza cuando no existe el producto solicitado."""

    def __init__(self, identificador: int | str) -> None:
        self.identificador = identificador
        super().__init__(f"No se encontro un producto con identificador '{identificador}'")


class ProductoYaExisteError(ProductoError):
    """Se lanza cuando el codigo de producto ya esta registrado."""

    def __init__(self, codigo: str) -> None:
        self.codigo = codigo
        super().__init__(f"Ya existe un producto con codigo '{codigo}'")


class DatosProductoInvalidosError(ProductoError):
    """Se lanza cuando los datos de producto no cumplen las reglas del negocio."""
