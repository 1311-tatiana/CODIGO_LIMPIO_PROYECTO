# Persistencia de Datos
Esta sección explica cómo la aplicación guarda y recupera la información del inventario.

La persistencia permite que los datos de los productos se mantengan almacenados incluso después de cerrar la aplicación.

## Archivo JSON
El sistema utiliza un archivo JSON para almacenar la información del inventario.

El archivo se encuentra en la siguiente ubicación del proyecto:

```
data/database.json
```

Este archivo funciona como una pequeña base de datos donde se guardan todos los productos registrados.

Si el archivo no existe, el sistema lo crea automáticamente cuando se guarda el primer producto.

## Estructura de los datos

Los datos dentro del archivo JSON se almacenan como una lista de objetos.
Cada objeto representa un producto del inventario.

### Ejemplo del contenido del archivo:

```json
[
  {
    "codigo": "P001",
    "nombre": "Martillo",
    "cantidad": 10,
    "valor": 15000.0
  },
  {
    "codigo": "P002",
    "nombre": "Destornillador",
    "cantidad": 25,
    "valor": 8000.0
  }
]
```
Cada producto contiene la siguiente información:

| Campo    | Descripción                       |
| -------- | --------------------------------- |
| codigo   | Identificador único del producto  |
| nombre   | Nombre del producto               |
| cantidad | Cantidad disponible en inventario |
| valor    | Precio unitario del producto      |

## Serialización de los modelos

Dentro de la aplicación, los productos se manejan mediante el modelo `Producto`.

Antes de guardarlos en el archivo JSON, estos objetos deben convertirse a un formato que pueda ser almacenado en el archivo.
Este proceso se conoce como **serialización**.

Durante la serialización, cada objeto `Producto` se convierte en un diccionario que contiene sus atributos. Luego, este diccionario se guarda en el archivo JSON.

De forma similar, cuando la aplicación carga los datos del archivo, cada registro se convierte nuevamente en un objeto `Producto`. Esto permite que el sistema pueda trabajar con los productos utilizando estructuras de datos propias del programa.