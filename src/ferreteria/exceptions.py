# src/ferreteria/exceptions.py


class AppError(Exception):
    """Clase base para todas las excepciones de la aplicación."""

    pass


class ProductoError(AppError):
    """Clase base para excepciones relacionadas con productos."""

    pass


class ProductoNoEncontradoError(ProductoError):
    """Se lanza cuando no se encuentra un producto con el código dado."""

    def __init__(self, codigo: str) -> None:
        self.codigo = codigo
        super().__init__(f"No se encontró ningún producto con el código '{codigo}'")


class ProductoYaExisteError(ProductoError):
    """Se lanza cuando se intenta crear un producto con un código ya registrado."""

    def __init__(self, codigo: str) -> None:
        self.codigo = codigo
        super().__init__(f"Ya existe un producto con el código '{codigo}'")


class DatosProductoInvalidosError(ProductoError):
    """Se lanza cuando los datos de un producto no son válidos."""

    def __init__(self, mensaje: str) -> None:
        super().__init__(mensaje)
