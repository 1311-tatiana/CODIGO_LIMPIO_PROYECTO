# Arquitectura

El proyecto usa una estructura modular basada en capas para separar responsabilidades.

```text
Cliente HTTP
   ↓
api/routers
   ↓
services
   ↓
storage/repositories
   ↓
Supabase o JSON local
```

## API

La capa `api` contiene la aplicacion FastAPI, las dependencias y los routers. Su responsabilidad es recibir peticiones HTTP, validar los datos con Pydantic y responder con codigos HTTP adecuados.

## Schemas

La capa `schemas` define los contratos de datos con Pydantic:

- `ProductoCreate`
- `ProductoUpdate`
- `ProductoResponse`

## Services

La capa `services` contiene la logica de negocio, por ejemplo validar que no existan codigos duplicados y calcular el valor total del inventario.

## Storage

La capa `storage` contiene el contrato de repositorio y dos implementaciones:

- `JSONProductoRepository` para pruebas locales.
- `SupabaseProductoRepository` para usar la base de datos real.
