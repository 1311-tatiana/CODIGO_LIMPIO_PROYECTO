from dataclasses import dataclass
from ..exceptions import DatosProductoInvalidosError
 
 
@dataclass
class Producto:
    """
    Modelo que representa un producto dentro del inventario de la ferretería.
 
    Este modelo encapsula la información básica de cada producto almacenado
    en el sistema. Cada producto contiene un identificador único, un nombre,
    la cantidad disponible en inventario y el valor unitario.
 
    Attributes
    ----------
    codigo : str
        Identificador único del producto dentro del inventario.
 
    nombre : str
        Nombre descriptivo del producto.
 
    cantidad : int
        Cantidad disponible del producto en el inventario.
 
    valor : float
        Precio unitario del producto.
    """
 
    codigo: str
    nombre: str
    cantidad: int
    valor: float
 
    def __post_init__(self) -> None:
        """
        Método especial de los `dataclass` que se ejecuta automáticamente
        después de inicializar una instancia del modelo.
 
        Se utiliza para validar los valores de los atributos del producto
        y garantizar que los datos almacenados sean consistentes.
        """
        self._validar_codigo()
        self._validar_nombre()
        self._validar_cantidad()
        self._validar_valor()
 
    def _validar_codigo(self) -> None:
        """
        Valida que el código del producto no esté vacío.
 
        Raises
        ------
        DatosProductoInvalidosError
            Si el código del producto es una cadena vacía.
        """
        if not self.codigo:
            raise DatosProductoInvalidosError(
                "El código del producto no puede estar vacío"
            )
 
    def _validar_nombre(self) -> None:
        """
        Valida que el nombre del producto no esté vacío.
 
        Raises
        ------
        DatosProductoInvalidosError
            Si el nombre del producto es una cadena vacía.
        """
        if not self.nombre or not self.nombre.strip():
            raise DatosProductoInvalidosError(
                "El nombre del producto no puede estar vacío"
            )
 
    def _validar_cantidad(self) -> None:
        """
        Valida que la cantidad del producto no sea negativa.
 
        Raises
        ------
        DatosProductoInvalidosError
            Si la cantidad del producto es menor que cero.
        """
        if self.cantidad < 0:
            raise DatosProductoInvalidosError(
                "La cantidad no puede ser negativa"
            )
 
    def _validar_valor(self) -> None:
        """
        Valida que el valor del producto no sea negativo.
 
        Raises
        ------
        DatosProductoInvalidosError
            Si el valor del producto es menor que cero.
        """
        if self.valor <= 0:
            raise DatosProductoInvalidosError(
                "El valor del producto no puede ser negativo"
            )