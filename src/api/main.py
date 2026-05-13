"""Punto de entrada de la API FastAPI."""

from fastapi import FastAPI

from src.api.routers.productos import router as productos_router
from src.core.config import settings

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API para gestionar el inventario de una ferreteria.",
)

app.include_router(productos_router)


@app.get("/", tags=["Health"])
def home():
    """Endpoint de verificacion del estado de la API."""

    return {"message": "API funcionando correctamente"}
