# src/ferreteria/exceptions.py
"""
Módulo de excepciones personalizadas del sistema de ferretería.

Este módulo define las excepciones utilizadas en la aplicación para
gestionar errores relacionados con la lógica de negocio del sistema,
especialmente en las operaciones relacionadas con productos.

Las excepciones permiten separar claramente los errores de dominio
de otros tipos de errores del sistema.
"""

class AppError(Exception):
    """
    Excepción base para todos los errores específicos de la aplicación.

    Esta clase sirve como punto de partida para todas las excepciones
    personalizadas del sistema. Permite capturar errores de dominio
    de manera centralizada sin interferir con otras excepciones
    del sistema o de librerías externas.

    Raises:
        Exception: Hereda de la excepción base de Python.
    """

    pass


class ProductoError(AppError):
    """
    Excepción base para errores relacionados con productos.

    Todas las excepciones asociadas a operaciones sobre productos
    deben heredar de esta clase. Esto permite manejar errores de
    productos de forma específica dentro de la capa de servicios.

    Raises:
        AppError: Si ocurre un error relacionado con la gestión de productos.
    """

    pass


class ProductoNoEncontradoError(ProductoError):
    """
    Excepción lanzada cuando un producto no existe en el sistema.

    Esta excepción se genera cuando se intenta acceder a un producto
    mediante su código y este no se encuentra registrado en el
    sistema de almacenamiento.

    Args:
        codigo (str): Código único del producto que se intentó buscar.

    Attributes:
        codigo (str): Código del producto que no fue encontrado.

    Raises:
        ProductoError: Cuando el producto solicitado no existe.
    """

    def __init__(self, codigo: str) -> None:
         """
        Inicializa la excepción con el código del producto no encontrado.

        Args:
            codigo (str): Código único del producto que no fue encontrado.

        Returns:
            None
        """
        self.codigo = codigo
        super().__init__(f"No se encontró ningún producto con el código '{codigo}'")


class ProductoYaExisteError(ProductoError):
        """
    Excepción lanzada cuando se intenta registrar un producto que ya existe.

    Esta excepción se genera cuando se intenta crear o registrar un producto
    utilizando un código que ya está presente en el sistema.

    Args:
        codigo (str): Código del producto que ya está registrado.

    Attributes:
        codigo (str): Código duplicado que provocó el error.

    Raises:
        ProductoError: Cuando se intenta registrar un producto duplicado.
    """

    def __init__(self, codigo: str) -> None:
        """
        Inicializa la excepción indicando el código duplicado.

        Args:
            codigo (str): Código del producto que ya existe en el sistema.

        Returns:
            None
        """
        self.codigo = codigo
        super().__init__(f"Ya existe un producto con el código '{codigo}'")


class DatosProductoInvalidosError(ProductoError):
    """
    Excepción lanzada cuando los datos proporcionados para un producto son inválidos.

    Esta excepción se utiliza para indicar que los datos recibidos
    para crear o actualizar un producto no cumplen con las reglas
    de validación definidas por la aplicación.

    Args:
        mensaje (str): Descripción del error de validación.

    Raises:
        ProductoError: Cuando los datos del producto no cumplen con
        los criterios de validación establecidos.
    """

    def __init__(self, mensaje: str) -> None:
                """
        Inicializa la excepción con un mensaje descriptivo del error.

        Args:
            mensaje (str): Descripción del problema detectado en los datos.

        Returns:
            None
        """
        super().__init__(mensaje)
