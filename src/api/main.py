"""
Interfaz de línea de comandos (CLI) del sistema de inventario de ferretería.

Este módulo actúa como punto de entrada de la aplicación y define
los comandos disponibles para interactuar con el inventario mediante
una interfaz de línea de comandos.

La CLI está construida utilizando la librería Typer y permite realizar
operaciones CRUD sobre los productos almacenados en el sistema:

- Crear productos
- Consultar productos
- Listar inventario
- Actualizar productos
- Eliminar productos

La lógica de negocio se delega al servicio `InventarioService`, mientras
que la persistencia de datos es gestionada por la implementación
`JSONStorage`.

El archivo de almacenamiento utilizado es:

    data/database.json
"""

from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from core.exceptions import AppError
from src.ferreteria.models import Producto
from services.services import InventarioService
from storage.storage import JSONStorage

app = typer.Typer()
console = Console()

storage = JSONStorage(Path("data/database.json"))
service = InventarioService(storage)


@app.command()
def crear(codigo: str, nombre: str, cantidad: int, valor: float):
    """
    Registra un nuevo producto en el inventario.

    Este comando crea un nuevo producto utilizando los datos
    proporcionados y lo almacena en el sistema.

    Args:
        codigo (str):
            Identificador único del producto.

        nombre (str):
            Nombre del producto.

        cantidad (int):
            Cantidad inicial disponible en inventario.

        valor (float):
            Precio unitario del producto.

    Raises:
        AppError:
            Si ocurre un error de validación o si el producto ya existe.

    Returns:
        None
    """
    try:
        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            cantidad=cantidad,
            valor=valor
        )

        service.crear_producto(producto)
        typer.echo("Producto creado correctamente")

    except AppError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def obtener(codigo: str):
    """
    Busca un producto en el inventario utilizando su código.

    Args:
        codigo (str):
            Código único del producto que se desea consultar.

    Raises:
        AppError:
            Si el producto no existe en el inventario.

    Returns:
        None
    """
    try:
        producto = service.buscar_producto(codigo)
        typer.echo(producto)

    except AppError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def listar():
    """
    Muestra todos los productos registrados en el inventario.

    Los productos se presentan en formato de tabla utilizando
    la librería Rich para mejorar la visualización en consola.

    Returns:
        None
    """
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
        table.add_row(
            str(p.codigo),
            p.nombre,
            str(p.cantidad),
            str(p.valor),
        )

    console.print(table)


@app.command()
def actualizar(codigo: str, nombre: str, cantidad: int, valor: float):
    """
    Actualiza la información de un producto existente.

    Permite modificar el nombre, la cantidad disponible
    y el valor de un producto registrado en el inventario.

    Args:
        codigo (str):
            Código del producto que se desea actualizar.

        nombre (str):
            Nuevo nombre del producto.

        cantidad (int):
            Nueva cantidad disponible.

        valor (float):
            Nuevo precio del producto.

    Raises:
        AppError:
            Si el producto no existe o si los datos proporcionados
            no son válidos.

    Returns:
        None
    """
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
    """
    Elimina un producto del inventario.

    Args:
        codigo (str):
            Código del producto que se desea eliminar.

    Raises:
        AppError:
            Si el producto no existe en el inventario.

    Returns:
        None
    """
    try:
        service.eliminar_producto(codigo)
        typer.echo("Producto eliminado")

    except AppError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


if __name__ == "__main__":
    """
    Punto de entrada de la aplicación CLI.
    """
    app()