"""
Capa de persistencia del sistema de inventario.

Este módulo define las interfaces y las implementaciones responsables
de almacenar y recuperar los datos del inventario.

La persistencia se realiza utilizando archivos JSON locales, permitiendo
almacenar los productos registrados en el sistema de manera estructurada
y fácilmente legible.

El módulo implementa una abstracción mediante el protocolo `Storage`,
permitiendo que diferentes mecanismos de almacenamiento puedan ser
utilizados sin modificar la lógica de negocio.
"""
import json
from pathlib import Path
from typing import List, Protocol

from .models import Producto


class Storage(Protocol):
    """
    Protocolo que define la interfaz de almacenamiento del sistema.

    Este protocolo establece los métodos que cualquier implementación
    de almacenamiento debe proporcionar. Permite desacoplar la lógica
    de negocio del mecanismo específico de persistencia.

    Methods:
        load():
            Recupera todos los productos almacenados.

        save(productos):
            Persiste una lista de productos en el sistema de almacenamiento.
    """
    def load(self) -> List[Producto]:
        """
        Carga todos los productos almacenados.

        Returns:
            List[Producto]:
                Lista de productos recuperados del almacenamiento.
        """
        ...

    def save(self, productos: List[Producto]) -> None: 
        """
        Guarda una lista de productos en el almacenamiento.

        Args:
            productos (List[Producto]):
                Lista de productos que se desea persistir.

        Returns:
            None
        """
        ...


class JSONStorage:
    """
    Implementación de almacenamiento basada en archivos JSON.

    Esta clase gestiona la persistencia de los productos utilizando
    un archivo JSON local. Cada producto se serializa como un objeto
    JSON dentro de una lista.

    Attributes:
        filepath (Path):
            Ruta al archivo JSON donde se almacenan los productos.
    """

    def __init__(self, filepath: Path) -> None:
        """
        Inicializa el sistema de almacenamiento JSON.

        Args:
            filepath (Path):
                Ruta del archivo JSON utilizado como base de datos
                del inventario.

        Returns:
            None
        """
        self.filepath = filepath

    def load(self) -> List[Producto]:
        """
        Carga los productos almacenados en el archivo JSON.

        Si el archivo no existe, se retorna una lista vacía,
        permitiendo inicializar el inventario sin errores.

        Returns:
            List[Producto]:
                Lista de objetos `Producto` reconstruidos a partir
                de los datos almacenados en el archivo JSON.
        """
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [Producto(**item) for item in data]

    def save(self, productos: List[Producto]) -> None:
         """
        Guarda los productos en el archivo JSON.

        Cada producto es serializado como un diccionario utilizando
        sus atributos internos. El archivo JSON resultante contiene
        una lista de objetos que representan los productos del
        inventario.

        Args:
            productos (List[Producto]):
                Lista de productos que se desean guardar.

        Returns:
            None
        """
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([p.__dict__ for p in productos], f, indent=2, ensure_ascii=False)
