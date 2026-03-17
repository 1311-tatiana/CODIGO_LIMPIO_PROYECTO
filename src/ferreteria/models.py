# src/ferreteria/models.py
"""
Modelos de dominio del sistema de ferretería.

Este módulo define las estructuras de datos principales utilizadas
en la aplicación. Los modelos representan las entidades del dominio
del negocio y son utilizados por las capas de servicios y persistencia
para manipular y almacenar información.
"""

from dataclasses import dataclass


@dataclass
class Producto:
        """
    Representa un producto dentro del inventario de la ferretería.

    Este modelo encapsula la información básica asociada a un producto
    almacenado en el sistema. Se utiliza en la capa de servicios para
    realizar operaciones de negocio y en la capa de almacenamiento para
    serializar y persistir los datos en archivos JSON.

    Attributes:
        codigo (str):
            Identificador único del producto dentro del sistema.
            Se maneja como cadena para permitir identificadores
            alfanuméricos o códigos con ceros a la izquierda.

        nombre (str):
            Nombre descriptivo del producto.

        cantidad (int):
            Cantidad disponible del producto en el inventario.

        valor (float):
            Precio unitario del producto en el inventario.
    """
    codigo: str
    nombre: str
    cantidad: int
    valor: float
