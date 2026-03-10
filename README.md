#  Ferretería — Sistema de Inventario y Ventas

Sistema de gestión de inventario para una ferretería, desarrollado en Python con arquitectura limpia, interfaz de línea de comandos con **Typer** y **Rich**, y persistencia local en JSON.


## Descripción del proyecto

Este proyecto consiste en un sistema de gestión de inventario, inicialmente enfocado en una ferretería, el cual nos va a permitir administrar productos y registrar los datos básicos de los productos que se tienen en el establecimiento, ofreciendo funcionalidades para crear, consultar, actualizar y eliminar información relacionada con el inventario.

## Propósito del proyecto
El propósito principal de este proyecto es facilitar el control de inventarios de manera organizada y estructurada, permitiendo el registro, consulta y actualización de los productos disponibles.



**Alcance funcional:**
- Registrar productos con código único, nombre, cantidad y valor.
- Consultar el listado completo del inventario con totales por producto.
- Buscar un producto específico por su código.
- Ver el valor monetario total del inventario.
- Actualizar nombre, cantidad y/o valor de un producto (el código no se puede modificar).
- Eliminar productos del inventario.



## 🗂 Estructura del proyecto

ferreteria-inventario/
├── .github/
│   └── workflows/
│       └── tests.yml         # CI: tests y lint automático en GitHub 
        └── docs.yml          # CI: tests y lint automático en GitHub
Actions
├── data/
│   └── database.json         # Base de datos local (JSON)
|──docs/
    └── referencia/
        └── api.md            #archivo de documentacion  
    ├─guia_usuario.md         #archivo de documentacion(guia)
    ├─index.md                #archivo de documentacion(presentacion)
├── src/
│   └── ferreteria/
│       ├── __init__.py
│       ├── models.py         # Dataclass Producto
│       ├── services.py       # Lógica de negocio (CRUD + validaciones)
│       ├── storage.py        # Lectura/escritura del archivo JSON
│       └── exceptions.py     # Excepciones personalizadas
├── tests/
│   ├── __init__.py
│   └── test_services.py      # 13 casos de prueba con Pytest
├── main.py                   # Interfaz CLI (Typer + Rich)
├── mkdocs.yml                # Archivo de configuración
├── .gitignore
├── pyproject.toml
└── README.md


## Guía de instalación

**Requisitos:** Python 3.12+ y [uv](https://docs.astral.sh/uv/) instalado.

# 1. Clonar el repositorio
git clone https://github.com/1311-tatiana/CODIGO_LIMPIO_PROYECTO.git
cd CODIGO_LIMPIO_PROYECTO

# 2. Crear entorno virtual con uv
uv venv

# 3. Instalar dependencias
uv pip install typer rich pytest ruff


## Manual de la CLI

### Crear un producto

uv run python main.py crear P001 "Martillo" 10 15000
#                           ^    ^           ^   ^
#                        codigo nombre   cantidad valor


### Listar todos los productos
uv run python main.py listar


### Buscar un producto por código

uv run python main.py buscar P001


### Ver valor total del inventario
uv run python main.py total


### Actualizar un producto

# Actualizar solo la cantidad
uv run python main.py actualizar P001 --cantidad 25

# Actualizar solo el valor
uv run python main.py actualizar P001 --valor 18000

# Actualizar nombre y cantidad
uv run python main.py actualizar P001 --nombre "Martillo Grande" --cantidad 5


### Eliminar un producto
uv run python main.py eliminar P001

# Se pedirá confirmación antes de eliminar


##  Instrucciones de Testing
uv run pytest


Los tests cubren los siguientes escenarios:

| # | Tipo | Descripción |
|---|------|-------------|
| 1 | Normal | Crear producto válido |
| 2 | Error | Crear producto con código duplicado |
| 3 | Error | Crear producto con nombre vacío |
| 4 | Extraordinario | Crear producto con cantidad negativa |
| 5 | Error | Crear producto con valor cero |
| 6 | Normal | Listar productos retorna lista completa |
| 7 | Normal | Buscar producto por código existente |
| 8 | Error | Buscar código inexistente |
| 9 | Normal | Calcular valor total del inventario |
| 10 | Normal | Actualizar cantidad y valor |
| 11 | Error | Actualizar producto inexistente |
| 12 | Normal | Eliminar producto existente |
| 13 | Error | Eliminar código inexistente |

## 🛠 Tecnologías utilizadas

- **Python 3.12+**
- **Typer** — CLI declarativa
- **Rich** — tablas y colores en terminal
- **Pytest** — pruebas unitarias
- **Ruff** — linter y formateador
- **uv** — gestión de dependencias y entorno