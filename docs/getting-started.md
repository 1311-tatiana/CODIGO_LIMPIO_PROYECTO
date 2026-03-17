# Requisitos
Antes de ejecutar el proyecto, asegúrate de tener instalado:
1-Python 3.10 o superior
2-uv (gestor de dependencias)

luego Puedes obtener el proyecto de dos formas:

Opción 1: Clonar con git
git clone https://github.com/1311-tatiana/CODIGO_LIMPIO_PROYECTO.git
cd CODIGO_LIMPIO_PROYECTO

Opción 2: Descargar como ZIP

Ir al repositorio en GitHub
Clic en Code → Download ZIP
Extraer el archivo
Abrir la carpeta en Visual Studio Code

# Instalación de dependencias

Dentro del proyecto ejecuta:
uv sync
Este comando instalará todas las dependencias necesarias.

# Ejecutar el proyecto

Para ver los comandos disponibles en la CLI:
uv run main.py --help

Ejemplo de uso:
uv run main.py crear
uv run main.py listar

Esto permitirá interactuar con el sistema de gestión de productos.

# Ejecutar pruebas

Para correr los tests del proyecto:
uv run pytest (Verificar calidad del código)

Para medir la complejidad ciclomática:
uv run radon cc src -a

El resultado esperado es:

Average complexity: A

# Estructura básica
src/        Código fuente
docs/       Documentación
tests/      Pruebas
data/       Persistencia en JSON