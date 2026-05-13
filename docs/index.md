# Ferreteria Inventario API

Backend para administrar productos de una ferreteria usando FastAPI, Pydantic y una capa de persistencia preparada para Supabase.

## Funcionalidades

- CRUD completo de productos.
- Documentacion automatica en `/docs` y `/redoc`.
- Validacion de datos con Pydantic.
- Separacion de responsabilidades por capas.
- Modo local con JSON y modo real con Supabase.

## Capas principales

```text
api/       Endpoints HTTP y routers de FastAPI
schemas/   Contratos Pydantic de entrada y salida
services/  Logica de negocio
storage/   Repositorios JSON/Supabase
core/      Configuracion y excepciones
```
