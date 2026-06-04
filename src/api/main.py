"""Punto de entrada de la API FastAPI."""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.api.routers.productos import router as productos_router
from src.core.config import settings
from src.web.routers.views import router as web_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Backend API para gestionar el inventario de una ferreteria.",
)

# Archivos estáticos: CSS, imágenes, JS
app.mount("/static", StaticFiles(directory="src/web/static"), name="static")

# Interfaz visual
app.include_router(web_router)

# API de productos
app.include_router(productos_router)


@app.get("/health", tags=["Health"])
def health():
    """Endpoint de verificación del estado de la API."""
    return {"message": "API funcionando correctamente"}