"""CLI opcional para administrar productos desde consola."""

import typer

from src.app.pages.productos import mostrar_productos
from src.core.exceptions import AppError
from src.schemas.producto import ProductoCreate, ProductoUpdate
from src.services.services import ProductoService
from src.storage.storage import JSONProductoRepository

app = typer.Typer(help="CLI opcional para el inventario de ferreteria.")
service = ProductoService(JSONProductoRepository())


@app.command()
def crear(codigo: str, nombre: str, cantidad: int, valor: float) -> None:
    """Registra un nuevo producto."""

    try:
        producto = service.crear_producto(
            ProductoCreate(codigo=codigo, nombre=nombre, cantidad=cantidad, valor=valor)
        )
        typer.echo(f"Producto creado con id {producto.id}")
    except AppError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc


@app.command()
def listar() -> None:
    """Muestra todos los productos."""

    mostrar_productos(service.listar_productos())


@app.command()
def obtener(producto_id: int) -> None:
    """Busca un producto por id."""

    try:
        typer.echo(service.obtener_producto(producto_id))
    except AppError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc


@app.command()
def actualizar(
    producto_id: int,
    codigo: str | None = None,
    nombre: str | None = None,
    cantidad: int | None = None,
    valor: float | None = None,
) -> None:
    """Actualiza uno o varios campos de un producto."""

    try:
        service.actualizar_producto(
            producto_id,
            ProductoUpdate(codigo=codigo, nombre=nombre, cantidad=cantidad, valor=valor),
        )
        typer.echo("Producto actualizado correctamente")
    except AppError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc


@app.command()
def eliminar(producto_id: int) -> None:
    """Elimina un producto por id."""

    try:
        service.eliminar_producto(producto_id)
        typer.echo("Producto eliminado")
    except AppError as exc:
        typer.secho(str(exc), fg=typer.colors.RED)
        raise typer.Exit(code=1) from exc


if __name__ == "__main__":
    app()
