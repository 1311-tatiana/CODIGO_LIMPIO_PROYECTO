## Descripción del proyecto
Este proyecto consiste en un sistema de gestión de inventario, inicialmente enfocado en una ferretería, el cual nos va a permitir administrar productos y registrar los datos básicos de los productos que se tienen en el establecimiento, ofreciendo funcionalidades para crear, consultar, actualizar y eliminar información relacionada con el inventario.

## Propósito del proyecto
El propósito principal de este proyecto es facilitar el control de inventarios de manera organizada y estructurada, permitiendo el registro, consulta y actualización de los productos disponibles.

## Alcance
El sistema está diseñado para administrar productos dentro de un inventario básico. Permite crear productos con un código único, registrar su cantidad disponible y valor unitario. También permite listar productos, actualizar información en caso de que los precios o la disponibilidad cambien, y eliminar registros cuando sea necesario.

## Guía de instalación
Para este proyecto seguiremos los siguientes pasos para una correcta instalación de la app y manejo desde la terminal.

## Instalación
uv venv
uv pip install typer rich pytest

## Uso
Crear un producto (codigo, nombre, cantidad, valor)
uv run python main.py crear P001 "Martillo" 10 15000

Listar todos los productos
uv run python main.py listar

Actualizar un producto (codigo, nuevo_nombre, nueva_cantidad, nuevo_valor)
uv run python main.py actualizar P001 "Martillo Grande" 20 18000

Eliminar un producto
uv run python main.py eliminar P001

## Testing
uv run pytest
