# Referencia de la API

Esta sección contiene la documentación técnica generada automáticamente
a partir de los *docstrings* del código fuente del proyecto.

La documentación incluye la descripción de los modelos, servicios,
excepciones y componentes de almacenamiento utilizados en el sistema.

## Excepciones

::: ferreteria.exceptions.AppError
options:
show_root_heading: true
show_source: false

::: ferreteria.exceptions.ProductoError
options:
show_root_heading: true
show_source: false

::: ferreteria.exceptions.ProductoNoEncontradoError
options:
show_root_heading: true
show_source: false

::: ferreteria.exceptions.ProductoYaExisteError
options:
show_root_heading: true
show_source: false

::: ferreteria.exceptions.DatosProductoInvalidosError
options:
show_root_heading: true
show_source: false


## Modelos

::: ferreteria.models.producto.Producto
options:
show_root_heading: true
show_source: false
members:
- post_init
- _validar_codigo
- _validar_nombre
- _validar_cantidad
- _validar_valor

## Servicios

::: ferreteria.services.InventarioService
options:
show_root_heading: true
show_source: false
members:
- init
- crear_producto
- listar_productos
- buscar_producto
- calcular_inventario_total
- actualizar_producto
- eliminar_producto

## Almacenamiento

::: ferreteria.storage.Storage
options:
show_root_heading: true
show_source: false
members:
- load
- save