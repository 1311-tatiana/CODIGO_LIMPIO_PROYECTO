# src/ferreteria/models.py
from dataclasses import dataclass


@dataclass
class Producto:
    """Representa un producto del inventario de la ferretería."""

    codigo: str
    nombre: str
    cantidad: int
    valor: float
