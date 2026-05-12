"""
Capa de persistencia del sistema de inventario.

Este módulo define las interfaces y las implementaciones responsables
de almacenar y recuperar los datos del inventario.

La persistencia se realiza utilizando archivos JSON locales,
permitiendo almacenar los productos registrados en el sistema
de manera estructurada y fácilmente legible.

El módulo implementa una abstracción mediante el protocolo
`Storage`, permitiendo utilizar diferentes mecanismos de
almacenamiento sin modificar la lógica de negocio.
"""

import json

from pathlib import Path
from typing import List, Protocol

from src.schemas.producto import Producto


class Storage(Protocol):
    """
    Protocolo que define la interfaz de almacenamiento del sistema.

    Este protocolo establece los métodos que cualquier implementación
    de almacenamiento debe proporcionar.

    Methods:
        load():
            Recupera todos los productos almacenados.

        save(productos):
            Guarda los productos en el almacenamiento.
    """

    def load(self) -> List[Producto]:
        """
        Carga todos los productos almacenados.

        Returns:
            List[Producto]:
                Lista de productos recuperados.
        """

        ...

    def save(self, productos: List[Producto]) -> None:
        """
        Guarda una lista de productos.

        Args:
            productos (List[Producto]):
                Productos a almacenar.

        Returns:
            None
        """

        ...


class JSONStorage:
    """
    Implementación de almacenamiento basada en archivos JSON.

    Esta clase permite guardar y recuperar productos desde
    un archivo JSON local.

    Attributes:
        filepath (Path):
            Ruta del archivo JSON.
    """

    def __init__(self, filepath: Path) -> None:
        """
        Inicializa el almacenamiento JSON.

        Args:
            filepath (Path):
                Ruta del archivo JSON utilizado
                como base de datos.

        Returns:
            None
        """

        self.filepath = filepath

    def load(self) -> List[Producto]:
        """
        Carga los productos almacenados.

        Si el archivo no existe, retorna una lista vacía.

        Returns:
            List[Producto]:
                Lista de productos recuperados
                desde el archivo JSON.
        """

        if not self.filepath.exists():
            return []

        with open(
            self.filepath,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return [
            Producto(**item)
            for item in data
        ]

    def save(self, productos: List[Producto]) -> None:
        """
        Guarda productos en el archivo JSON.

        Args:
            productos (List[Producto]):
                Lista de productos a guardar.

        Returns:
            None
        """

        self.filepath.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        with open(
            self.filepath,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                [p.__dict__ for p in productos],
                file,
                indent=2,
                ensure_ascii=False
            )