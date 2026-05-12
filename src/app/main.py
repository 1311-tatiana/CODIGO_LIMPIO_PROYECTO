"""
Interfaz de línea de comandos (CLI) del sistema de inventario de ferretería.

Este módulo actúa como punto de entrada de la aplicación y define
los comandos disponibles para interactuar con el inventario mediante
una interfaz de línea de comandos.
"""

from pathlib import Path

import typer

from src.core.exceptions import AppError
from src.app.pages.products import mostrar_productos
from src.ferreteria.models import Producto
from services.services import InventarioService
from storage.storage import JSONStorage


app = typer.Typer()

storage = JSONStorage(Path("data/database.json"))
service = InventarioService(storage)


@app.command()
def crear(
    codigo: str,
    nombre: str,
    cantidad: int,
    valor: float
):
    """
    Registra un nuevo producto en el inventario.
    """

    try:
        producto = Producto(
            codigo=codigo,
            nombre=nombre,
            cantidad=cantidad,
            valor=valor
        )

        service.crear_producto(producto)

        typer.echo(
            "Producto creado correctamente"
        )

    except AppError as e:
        typer.secho(
            str(e),
            fg=typer.colors.RED
        )

        raise typer.Exit(code=1)


@app.command()
def obtener(codigo: str):
    """
    Busca un producto por código.
    """

    try:
        producto = service.buscar_producto(codigo)

        typer.echo(producto)

    except AppError as e:
        typer.secho(
            str(e),
            fg=typer.colors.RED
        )

        raise typer.Exit(code=1)


@app.command()
def listar():
    """
    Muestra todos los productos registrados.
    """

    productos = service.listar_productos()

    mostrar_productos(productos)


@app.command()
def actualizar(
    codigo: str,
    nombre: str,
    cantidad: int,
    valor: float
):
    """
    Actualiza un producto existente.
    """

    try:
        service.actualizar_producto(
            codigo=codigo,
            nuevo_nombre=nombre,
            nueva_cantidad=cantidad,
            nuevo_valor=valor,
        )

        typer.echo(
            "Producto actualizado correctamente"
        )

    except AppError as e:
        typer.secho(
            str(e),
            fg=typer.colors.RED
        )

        raise typer.Exit(code=1)


@app.command()
def eliminar(codigo: str):
    """
    Elimina un producto del inventario.
    """

    try:
        service.eliminar_producto(codigo)

        typer.echo(
            "Producto eliminado"
        )

    except AppError as e:
        typer.secho(
            str(e),
            fg=typer.colors.RED
        )

        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()