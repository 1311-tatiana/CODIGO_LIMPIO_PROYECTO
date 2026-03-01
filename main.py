from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from src.ferreteria.exceptions import AppError
from src.ferreteria.models import Producto
from src.ferreteria.services import InventarioService
from src.ferreteria.storage import JSONStorage

app = typer.Typer()
console = Console()

storage = JSONStorage(Path("data/database.json"))
service = InventarioService(storage)


@app.command()
def crear(codigo: str, nombre: str, cantidad: int, valor: float):
    """Registra un nuevo producto en el inventario."""
    try:
        producto = Producto(codigo=codigo, nombre=nombre, cantidad=cantidad, valor=valor)
        service.crear_producto(producto)
        typer.echo("Producto creado correctamente")
    except AppError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def obtener(codigo: str):
    """Busca y muestra un producto por su código."""
    try:
        producto = service.buscar_producto(codigo)
        typer.echo(producto)
    except AppError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def listar():
    """Muestra todos los productos del inventario."""
    productos = service.listar_productos()

    if not productos:
        console.print("No hay productos registrados", style="bold red")
        return

    table = Table(title="Inventario")
    table.add_column("Código", justify="right", style="cyan")
    table.add_column("Nombre", style="magenta")
    table.add_column("Cantidad", style="green")
    table.add_column("Valor", style="yellow")

    for p in productos:
        table.add_row(str(p.codigo), p.nombre, str(p.cantidad), str(p.valor))

    console.print(table)


@app.command()
def actualizar(codigo: str, nombre: str, cantidad: int, valor: float):
    """Actualiza el nombre, cantidad y valor de un producto existente."""
    try:
        service.actualizar_producto(
            codigo=codigo,
            nuevo_nombre=nombre,
            nueva_cantidad=cantidad,
            nuevo_valor=valor,
        )
        typer.echo("Producto actualizado correctamente")
    except AppError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def eliminar(codigo: str):
    """Elimina un producto del inventario por su código."""
    try:
        service.eliminar_producto(codigo)
        typer.echo("Producto eliminado")
    except AppError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()