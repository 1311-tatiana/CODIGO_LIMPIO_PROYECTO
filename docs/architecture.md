# Estructura del proyecto

El proyecto utiliza el patrón src layout, donde todo el código fuente se encuentra dentro de la carpeta src.

src/
└── ferreteria/
    |models/
        ├──producto.py
    ├── services.py
    ├── storage.py
    └── exceptions.py

Esta estructura ayuda a separar claramente el código del proyecto de otros archivos como pruebas, documentación o configuraciones.

# Capas del sistema

El sistema se divide en las siguientes capas:

# Modelos

Los modelos representan las entidades principales del sistema.
En este caso, el modelo principal es Producto, el cual describe los datos de un producto dentro del inventario. Los modelos se implementan utilizando dataclasses, lo que permite definir estructuras de datos de forma clara y concisa. Además, las validaciones se realizan dentro del método __post_init__, garantizando que los datos del modelo siempre sean válidos.

# Servicios

La capa de servicios contiene la lógica del negocio de la aplicación. Aquí se implementan operaciones como:

-crear productos

-listar productos

-actualizar productos

-eliminar productos

Esta capa actúa como intermediaria entre la interfaz de usuario (CLI) y la capa de almacenamiento.

# Almacenamiento

La capa de almacenamiento se encarga de la persistencia de datos.
Los productos se guardan en un archivo JSON que funciona como una base de datos simple.
El módulo storage.py maneja:

-lectura de datos

-escritura de datos

-serialización de objetos

Esto permite mantener separada la lógica de negocio de la lógica de persistencia.

# Excepciones

El módulo exceptions.py define errores personalizados que permiten manejar situaciones excepcionales de forma clara.

Esto mejora la legibilidad del código y facilita el manejo de errores dentro de la aplicación.

# Flujo del sistema

El flujo de funcionamiento del sistema es el siguiente:

CLI (main.py)
     ↓
Servicios (services.py)
     ↓
Modelos (producto.py)
     ↓
Almacenamiento (storage.py)
     ↓
Archivo JSON

De esta manera, cada componente cumple un rol específico dentro del sistema.
Principios de código limpio aplicados

# principios de código limpio:

-Separación de responsabilidades: cada módulo cumple una función específica.
-Modelos claros: uso de dataclasses para representar entidades.
-Validaciones centralizadas: implementadas en los modelos mediante __post_init__.
-Organización modular: división del sistema en componentes independientes.
-Legibilidad del código: nombres claros para variables, funciones y clases.

