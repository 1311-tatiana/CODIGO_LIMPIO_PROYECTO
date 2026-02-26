from pathlib import Path
import typer
from rich.console import Console
from rich.table import Table

from src.mi_app.exceptions import AppError

from src.mi_app.models import User
from src.mi_app.services import UserService
from src.mi_app.storage import JSONStorage

app = typer.Typer()
console = Console()

storage = JSONStorage(Path("data/database.json"))
service = UserService(storage)


@app.command()
def create(id: int, name: str, email: str):
    try:
        user = User(id=id, name=name, email=email)
        service.create_user(user)
        typer.echo("User created successfully")
    except AppError as e:
        typer.secho(str(e), fg=typer.colors.RED)
        raise typer.Exit(code=1)


@app.command()
def get(id: int):
    user = service.get_user(id)
    typer.echo(user)


@app.command()
def list():
    """Show all users using rich tables"""
    users = service.storage.load()
    if not users:
        console.print("No users found", style="bold red")
        return
    table = Table(title="Users")
    table.add_column("ID", justify="right", style="cyan")
    table.add_column("Name", style="magenta")
    table.add_column("Email", style="green")
    for user in users:
        table.add_row(str(user.id), user.name, user.email)
    console.print(table)


@app.command()
def delete(id: int):
    service.delete_user(id)
    typer.echo("User deleted")


if __name__ == "__main__":
    app()
