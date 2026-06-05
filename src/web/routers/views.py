import csv
import io
from urllib.parse import quote

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


def redirigir_inicio(mensaje: str = "", error: str = "") -> RedirectResponse:
    """Redirige al inicio con mensaje de éxito o error."""
    if mensaje:
        url = f"/?mensaje={quote(mensaje)}"
    elif error:
        url = f"/?error={quote(error)}"
    else:
        url = "/"

    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


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
    try:
        productos = service.listar_productos()
        total = service.calcular_valor_total()
    except Exception as exc:
        productos = []
        total = 0
        error = f"Error al cargar productos: {exc}"

    if q:
        productos_filtrados = [
            producto
            for producto in productos
            if q.lower() in producto.nombre.lower()
            or q.lower() in producto.codigo.lower()
        ]
    else:
        productos_filtrados = productos

    unidades_totales = sum(producto.cantidad for producto in productos)
    productos_stock_bajo = sum(
        1 for producto in productos if 0 < producto.cantidad <= 5
    )
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
    try:
        producto = ProductoCreate(
            codigo=codigo,
            nombre=nombre,
            cantidad=cantidad,
            valor=valor,
        )

        service.crear_producto(producto)

        return redirigir_inicio(mensaje="Producto registrado correctamente")

    except ProductoYaExisteError:
        return redirigir_inicio(error="Ya existe un producto con ese código")

    except Exception as exc:
        return redirigir_inicio(error=f"Error inesperado al crear producto: {exc}")


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
        return redirigir_inicio(error="Producto no encontrado")

    except Exception as exc:
        return redirigir_inicio(error=f"Error inesperado al cargar producto: {exc}")

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
    try:
        datos_actualizados = ProductoUpdate(
            codigo=codigo,
            nombre=nombre,
            cantidad=cantidad,
            valor=valor,
        )

        service.actualizar_producto(producto_id, datos_actualizados)

        return redirigir_inicio(mensaje="Producto actualizado correctamente")

    except ProductoYaExisteError:
        mensaje_error = quote("Ya existe un producto con ese código")
        url = f"/productos/{producto_id}/editar?error={mensaje_error}"

        return RedirectResponse(
            url,
            status_code=status.HTTP_303_SEE_OTHER,
        )

    except ProductoNoEncontradoError:
        return redirigir_inicio(error="Producto no encontrado")

    except Exception as exc:
        return redirigir_inicio(error=f"Error inesperado al actualizar producto: {exc}")


@router.post("/productos/{producto_id}/sumar-stock")
def sumar_stock_producto(
    producto_id: int,
    cantidad_agregar: int = Form(...),
    service: ProductoService = Depends(get_producto_service),
):
    try:
        if cantidad_agregar == 0:
            return redirigir_inicio(error="La cantidad debe ser diferente de cero")

        producto = service.obtener_producto(producto_id)

        nueva_cantidad = producto.cantidad + cantidad_agregar

        if nueva_cantidad < 0:
            return redirigir_inicio(
                error="No puedes retirar más unidades de las disponibles"
            )

        service.actualizar_producto(
            producto_id,
            ProductoUpdate(cantidad=nueva_cantidad),
        )

        if cantidad_agregar > 0:
            mensaje = "Cantidad agregada correctamente"
        else:
            mensaje = "Cantidad descontada correctamente"

        return redirigir_inicio(mensaje=mensaje)

    except ProductoNoEncontradoError:
        return redirigir_inicio(error="Producto no encontrado")

    except Exception as exc:
        return redirigir_inicio(error=f"Error inesperado al ajustar stock: {exc}")


@router.post("/productos/{producto_id}/eliminar")
def eliminar_producto(
    producto_id: int,
    service: ProductoService = Depends(get_producto_service),
):
    try:
        service.eliminar_producto(producto_id)

        return redirigir_inicio(mensaje="Producto eliminado correctamente")

    except ProductoNoEncontradoError:
        return redirigir_inicio(error="Producto no encontrado")

    except Exception as exc:
        return redirigir_inicio(error=f"Error inesperado al eliminar producto: {exc}")


@router.get("/productos/exportar")
def exportar_productos_csv(
    service: ProductoService = Depends(get_producto_service),
):
    try:
        productos = service.listar_productos()

        output = io.StringIO()

        # Punto y coma para que Excel en español lo abra en columnas.
        writer = csv.writer(output, delimiter=";")

        writer.writerow(
            ["ID", "Código", "Nombre", "Cantidad", "Valor unitario", "Valor total"]
        )

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
            content=output.getvalue().encode("utf-8-sig"),
            media_type="text/csv; charset=utf-8",
            headers={
                "Content-Disposition": "attachment; filename=inventario_productos.csv"
            },
        )

    except Exception as exc:
        return Response(
            content=f"Error al exportar productos: {exc}",
            media_type="text/plain",
            status_code=500,
        )