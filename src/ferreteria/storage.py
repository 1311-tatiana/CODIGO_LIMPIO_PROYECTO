import json
from pathlib import Path
from typing import List, Protocol

from .models import Producto


class Storage(Protocol):
    """Protocolo que define la interfaz de almacenamiento."""

    def load(self) -> List[Producto]: ...

    def save(self, productos: List[Producto]) -> None: ...


class JSONStorage:
    """Implementación de almacenamiento en archivo JSON local."""

    def __init__(self, filepath: Path) -> None:
        """Inicializa el almacenamiento con la ruta del archivo JSON.

        Args:
            filepath: Ruta al archivo JSON de base de datos.
        """
        self.filepath = filepath

    def load(self) -> List[Producto]:
        """Carga y retorna todos los productos desde el archivo JSON.

        Returns:
            Lista de objetos Producto. Lista vacía si el archivo no existe.
        """
        if not self.filepath.exists():
            return []

        with open(self.filepath, "r", encoding="utf-8") as f:
            data = json.load(f)

        return [Producto(**item) for item in data]

    def save(self, productos: List[Producto]) -> None:
        """Guarda la lista de productos en el archivo JSON.

        Args:
            productos: Lista de objetos Producto a persistir.
        """
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump([p.__dict__ for p in productos], f, indent=2, ensure_ascii=False)
