from fastapi import APIRouter, Depends

from src.schemas.product import Product
from src.services.product_service import ProductService
from src.api.dependencies import get_product_service


router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@router.get("/")
def list_products(
    service: ProductService = Depends(get_product_service)
):
    return service.list_products()


@router.post("/")
def create_product(
    product: Product,
    service: ProductService = Depends(get_product_service)
):
    service.create_product(product)

    return {
        "message": "Producto creado correctamente"
    }


@router.put("/{product_id}")
def update_product(
    product_id: int,
    updated_data: dict,
    service: ProductService = Depends(get_product_service)
):
    service.update_product(
        product_id,
        updated_data
    )

    return {
        "message": "Producto actualizado"
    }


@router.put("/{product_id}/quantity")
def assign_quantity(
    product_id: int,
    quantity: int,
    service: ProductService = Depends(get_product_service)
):
    service.assign_quantity(
        product_id,
        quantity
    )

    return {
        "message": "Cantidad actualizada"
    }