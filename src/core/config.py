"""
Módulo de configuración global del sistema.

Este módulo centraliza las constantes y configuraciones
utilizadas por la aplicación de inventario de ferretería.

Actualmente incluye:

- Ruta del archivo de almacenamiento JSON.
- Nombre de la aplicación.

Estas configuraciones permiten evitar valores
hardcodeados en múltiples módulos del sistema.
"""

from pathlib import Path


# Ruta del archivo de almacenamiento JSON
DATABASE_PATH = Path("data/database.json")


# Nombre de la aplicación
APP_NAME = "Sistema de Inventario Ferreteria"