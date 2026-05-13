# Primeros pasos

## Requisitos

- Python 3.12 o superior.
- uv instalado.

## Instalacion

```bash
git clone https://github.com/1311-tatiana/CODIGO_LIMPIO_PROYECTO.git
cd CODIGO_LIMPIO_PROYECTO
uv sync --all-extras
```

## Variables de entorno

```bash
cp .env.example .env
```

Para desarrollo local puedes dejar `USE_SUPABASE=false`. Para conectarte a Supabase, completa `SUPABASE_URL`, `SUPABASE_KEY` y cambia `USE_SUPABASE=true`.

## Ejecutar API

```bash
uv run uvicorn src.api.main:app --reload
```

Abre la documentacion automatica en:

```text
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```

## Ejecutar pruebas

```bash
uv run pytest -v
```
