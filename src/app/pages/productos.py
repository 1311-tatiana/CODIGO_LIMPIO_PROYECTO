"""
Funciones visuales relacionadas con productos.

Este módulo contiene utilidades para mostrar información
de productos en consola utilizando Rich.
"""

from rich.console import Console
from rich.table import Table


console = Console()


def mostrar_productos(productos):
    """
    Muestra una lista de productos en formato tabla.

    Args:
        productos (list):
            Lista de productos del inventario.
    """

    if not productos:
        console.print(
            "No hay productos registrados",
            style="bold red"
        )
        return

    table = Table(title="Inventario")

    table.add_column(
        "Código",
        justify="center",
        style="cyan"
    )

    table.add_column(
        "Nombre",
        style="magenta"
    )

    table.add_column(
        "Cantidad",
        justify="center",
        style="green"
    )

    table.add_column(
        "Valor",
        justify="right",
        style="yellow"
    )

    for producto in productos:
        table.add_row(
            str(producto.codigo),
            producto.nombre,
            str(producto.cantidad),
            f"${producto.valor}"
        )

    console.print(table)