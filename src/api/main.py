from fastapi import FastAPI

from src.api.routers.products import router as products_router

app = FastAPI(
    title="Inventario Ferreteria"
)

app.include_router(products_router)


@app.get("/")
def home():
    return {
        "message": "API funcionando correctamente"
    }