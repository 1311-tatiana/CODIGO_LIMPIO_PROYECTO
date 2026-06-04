import csv
import io

from fastapi import APIRouter, Depends, Form, Query, Request
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from starlette import status

from src.api.dependencies import get_producto_service
from src.core.exceptions import ProductoNoEncontradoError, ProductoYaExisteError
from src.schemas.producto import ProductoCreate, ProductoUpdate
from src.services.services import ProductoService

router = APIRouter(tags=["Interfaz Web"])

templates = Jinja2Templates(directory="src/web/templates")


def obtener_estado_stock(cantidad: int) -> str:
    if cantidad == 0:
        return "Agotado"
    if cantidad <= 5:
        return "Stock bajo"
    return "Disponible"


@router.get("/", response_class=HTMLResponse)
def inicio(
    request: Request,
    q: str = Query(default=""),
    mensaje: str = Query(default=""),
    error: str = Query(default=""),
    service: ProductoService = Depends(get_producto_service),
):
    productos = service.listar_productos()

    if q:
        productos_filtrados = [
            producto
            for producto in productos
            if q.lower() in producto.nombre.lower()
            or q.lower() in producto.codigo.lower()
        ]
    else:
        productos_filtrados = productos

    total = service.calcular_valor_total()
    unidades_totales = sum(producto.cantidad for producto in productos)
    productos_stock_bajo = sum(1 for producto in productos if 0 < producto.cantidad <= 5)
    productos_agotados = sum(1 for producto in productos if producto.cantidad == 0)

    return templates.TemplateResponse(
        request=request,
        name="productos.html",
        context={
            "productos": productos_filtrados,
            "total": total,
            "q": q,
            "mensaje": mensaje,
            "error": error,
            "unidades_totales": unidades_totales,
            "productos_stock_bajo": productos_stock_bajo,
            "productos_agotados": productos_agotados,
            "estado_stock": obtener_estado_stock,
        },
    )


@router.post("/productos/crear")
def crear_producto(
    codigo: str = Form(...),
    nombre: str = Form(...),
    cantidad: int = Form(...),
    valor: float = Form(...),
    service: ProductoService = Depends(get_producto_service),
):
    producto = ProductoCreate(
        codigo=codigo,
        nombre=nombre,
        cantidad=cantidad,
        valor=valor,
    )

    try:
        service.crear_producto(producto)
        return RedirectResponse(
            "/?mensaje=Producto registrado correctamente",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except ProductoYaExisteError:
        return RedirectResponse(
            "/?error=Ya existe un producto con ese código",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/productos/{producto_id}/editar", response_class=HTMLResponse)
def formulario_editar_producto(
    producto_id: int,
    request: Request,
    error: str = Query(default=""),
    service: ProductoService = Depends(get_producto_service),
):
    try:
        producto = service.obtener_producto(producto_id)
    except ProductoNoEncontradoError:
        return RedirectResponse(
            "/?error=Producto no encontrado",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    return templates.TemplateResponse(
        request=request,
        name="editar_producto.html",
        context={
            "producto": producto,
            "error": error,
        },
    )


@router.post("/productos/{producto_id}/editar")
def editar_producto(
    producto_id: int,
    codigo: str = Form(...),
    nombre: str = Form(...),
    cantidad: int = Form(...),
    valor: float = Form(...),
    service: ProductoService = Depends(get_producto_service),
):
    datos_actualizados = ProductoUpdate(
        codigo=codigo,
        nombre=nombre,
        cantidad=cantidad,
        valor=valor,
    )

    try:
        service.actualizar_producto(producto_id, datos_actualizados)
        return RedirectResponse(
            "/?mensaje=Producto actualizado correctamente",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except ProductoYaExisteError:
        return RedirectResponse(
            f"/productos/{producto_id}/editar?error=Ya existe un producto con ese código",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except ProductoNoEncontradoError:
        return RedirectResponse(
            "/?error=Producto no encontrado",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.post("/productos/{producto_id}/eliminar")
def eliminar_producto(
    producto_id: int,
    service: ProductoService = Depends(get_producto_service),
):
    try:
        service.eliminar_producto(producto_id)
        return RedirectResponse(
            "/?mensaje=Producto eliminado correctamente",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    except ProductoNoEncontradoError:
        return RedirectResponse(
            "/?error=Producto no encontrado",
            status_code=status.HTTP_303_SEE_OTHER,
        )


@router.get("/productos/exportar")
def exportar_productos_csv(
    service: ProductoService = Depends(get_producto_service),
):
    productos = service.listar_productos()

    output = io.StringIO()
    writer = csv.writer(output)

    writer.writerow(["ID", "Código", "Nombre", "Cantidad", "Valor unitario", "Valor total"])

    for producto in productos:
        writer.writerow(
            [
                producto.id,
                producto.codigo,
                producto.nombre,
                producto.cantidad,
                producto.valor,
                producto.cantidad * producto.valor,
            ]
        )

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=inventario_productos.csv"
        },
    )


@router.post("/productos/{producto_id}/sumar-stock")
def sumar_stock_producto(
    producto_id: int,
    cantidad_agregar: int = Form(...),
    service: ProductoService = Depends(get_producto_service),
):
    try:
        producto = service.obtener_producto(producto_id)

        nueva_cantidad = producto.cantidad + cantidad_agregar

        service.actualizar_producto(
            producto_id,
            ProductoUpdate(cantidad=nueva_cantidad),
        )

        return RedirectResponse(
            "/?mensaje=Cantidad agregada correctamente",
            status_code=status.HTTP_303_SEE_OTHER,
        )

    except ProductoNoEncontradoError:
        return RedirectResponse(
            "/?error=Producto no encontrado",
            status_code=status.HTTP_303_SEE_OTHER,
        )