# Uso de la API

## Ejecutar servidor

```bash
uv run uvicorn src.api.main:app --reload
```

## Endpoints

| Metodo | Ruta | Descripcion |
| --- | --- | --- |
| GET | `/products/` | Lista productos |
| POST | `/products/` | Crea un producto |
| GET | `/products/{product_id}` | Consulta por id |
| GET | `/products/code/{codigo}` | Consulta por codigo |
| PUT | `/products/{product_id}` | Actualiza un producto |
| PATCH | `/products/{product_id}` | Actualiza parcialmente |
| DELETE | `/products/{product_id}` | Elimina un producto |
| GET | `/products/total-value` | Calcula valor total |

## Ejemplo de creacion

```bash
curl -X POST http://127.0.0.1:8000/products/ \
  -H "Content-Type: application/json" \
  -d '{"codigo":"P001","nombre":"Martillo","cantidad":10,"valor":15000}'
```
