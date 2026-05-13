"""Endpoints HTTP para la gestion de productos."""

from fastapi import APIRouter, Depends, HTTPException, Response, status

from src.api.dependencies import get_producto_service
from src.core.exceptions import ProductoNoEncontradoError, ProductoYaExisteError
from src.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from src.services.services import ProductoService

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("/", response_model=list[ProductoResponse])
def list_products(service: ProductoService = Depends(get_producto_service)):
    """Lista todos los productos."""

    return service.listar_productos()


@router.post("/", response_model=ProductoResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductoCreate,
    service: ProductoService = Depends(get_producto_service),
):
    """Crea un producto."""

    try:
        return service.crear_producto(product)
    except ProductoYaExisteError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.get("/code/{codigo}", response_model=ProductoResponse)
def get_product_by_code(
    codigo: str,
    service: ProductoService = Depends(get_producto_service),
):
    """Consulta un producto por codigo."""

    try:
        return service.buscar_producto_por_codigo(codigo)
    except ProductoNoEncontradoError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/total-value")
def get_total_value(service: ProductoService = Depends(get_producto_service)):
    """Calcula el valor monetario total del inventario."""

    return {"total": service.calcular_valor_total()}


@router.get("/{product_id}", response_model=ProductoResponse)
def get_product(
    product_id: int,
    service: ProductoService = Depends(get_producto_service),
):
    """Consulta un producto por id."""

    try:
        return service.obtener_producto(product_id)
    except ProductoNoEncontradoError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.put("/{product_id}", response_model=ProductoResponse)
def update_product(
    product_id: int,
    updated_data: ProductoUpdate,
    service: ProductoService = Depends(get_producto_service),
):
    """Actualiza total o parcialmente un producto."""

    try:
        return service.actualizar_producto(product_id, updated_data)
    except ProductoNoEncontradoError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except ProductoYaExisteError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc


@router.patch("/{product_id}", response_model=ProductoResponse)
def patch_product(
    product_id: int,
    updated_data: ProductoUpdate,
    service: ProductoService = Depends(get_producto_service),
):
    """Actualiza parcialmente un producto."""

    return update_product(product_id, updated_data, service)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    service: ProductoService = Depends(get_producto_service),
):
    """Elimina un producto."""

    try:
        service.eliminar_producto(product_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except ProductoNoEncontradoError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
