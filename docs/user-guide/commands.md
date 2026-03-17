# Comandos de la Aplicación

Esta sección describe cómo utilizar la interfaz de línea de comandos (CLI) para gestionar el inventario de la ferretería.

La aplicación permite realizar diferentes operaciones sobre los productos almacenados en el sistema mediante comandos ejecutados desde la terminal.

## Ejecutar la aplicación
La aplicación se ejecuta mediante el gestor de dependencias **uv**.

```bash
uv run main.py [COMANDO] [PARAMETROS]
```

Donde:

* **COMANDO** indica la operación a realizar
* **PARAMETROS** son los valores necesarios para ejecutar el comando


# Ejemplos disponibles 

## Crear un producto
Permite registrar un nuevo producto en el inventario.

### Comando
```bash
uv run main.py crear CODIGO NOMBRE CANTIDAD VALOR
```

### Parámetros
| Parámetro | Tipo   | Descripción                       |
| --------- | ------ | --------------------------------- |
| CODIGO    | string | Identificador único del producto  |
| NOMBRE    | string | Nombre del producto               |
| CANTIDAD  | int    | Cantidad disponible en inventario |
| VALOR     | float  | Precio unitario del producto      |

### Ejemplo
```bash
uv run main.py crear P001 Martillo 10 15000
```

### Ejemplo de salida
```
Producto creado correctamente
```

## Listar productos
Muestra todos los productos registrados en el inventario.

### Comando
```bash
uv run main.py listar
```

### Ejemplo de salida
```
Inventario
┏━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━┳━━━━━━━━━━┓
┃ Código ┃ Nombre        ┃ Cantidad ┃ Valor    ┃
┡━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━╇━━━━━━━━━━┩
│ P001   │ Martillo      │ 10       │ 15000    │
│ P002   │ Destornillador│ 25       │ 8000     │
└────────┴───────────────┴──────────┴──────────┘
```

## Obtener un producto
Permite consultar la información de un producto específico mediante su código.

### Comando
```bash
uv run main.py obtener CODIGO
```

### Ejemplo
```bash
uv run main.py obtener P001
```

### Ejemplo de salida
```
Producto(codigo='P001', nombre='Martillo', cantidad=10, valor=15000.0)
```

## Actualizar un producto
Permite modificar la información de un producto existente.

### Comando
```bash
uv run main.py actualizar CODIGO NOMBRE CANTIDAD VALOR
```

### Ejemplo
```bash
uv run main.py actualizar P001 MartilloGrande 20 18000
```

### Ejemplo de salida
```
Producto actualizado correctamente
```

## Eliminar un producto
Permite eliminar un producto del inventario mediante su código.

### Comando
```bash
uv run main.py eliminar CODIGO
```

### Ejemplo
```bash
uv run main.py eliminar P001
```

### Ejemplo de salida
```
Producto eliminado
```

## Visualizar comandos disponibles:
```bash
uv run main.py --help
```

Este comando muestra una descripción general de los comandos y parámetros disponibles en la aplicación.