"""Funciones visuales para la CLI de productos."""

from rich.console import Console
from rich.table import Table

console = Console()


def mostrar_productos(productos) -> None:
    """Imprime una tabla de productos en consola."""

    if not productos:
        console.print("No hay productos registrados", style="bold red")
        return

    table = Table(title="Inventario")
    table.add_column("ID", justify="center")
    table.add_column("Codigo", justify="center", style="cyan")
    table.add_column("Nombre", style="magenta")
    table.add_column("Cantidad", justify="center", style="green")
    table.add_column("Valor", justify="right", style="yellow")

    for producto in productos:
        table.add_row(
            str(producto.id),
            producto.codigo,
            producto.nombre,
            str(producto.cantidad),
            f"${producto.valor:,.2f}",
        )

    console.print(table)
