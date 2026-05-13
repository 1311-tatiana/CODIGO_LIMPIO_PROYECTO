"""Repositorios para acceder a productos desde JSON local o Supabase."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Protocol

from src.core.config import settings
from src.schemas.producto import ProductoCreate, ProductoResponse, ProductoUpdate
from src.storage.supabase_client import get_supabase_client


class ProductoRepository(Protocol):
    """Contrato de persistencia para productos."""

    def list(self) -> list[ProductoResponse]: ...

    def get_by_id(self, producto_id: int) -> ProductoResponse | None: ...

    def get_by_codigo(self, codigo: str) -> ProductoResponse | None: ...

    def create(self, producto: ProductoCreate) -> ProductoResponse: ...

    def update(self, producto_id: int, data: ProductoUpdate) -> ProductoResponse | None: ...

    def delete(self, producto_id: int) -> bool: ...


def _to_response(data: dict) -> ProductoResponse:
    """Convierte un diccionario en ProductoResponse normalizado."""

    return ProductoResponse(
        id=int(data["id"]),
        codigo=str(data["codigo"]),
        nombre=str(data["nombre"]),
        cantidad=int(data["cantidad"]),
        valor=float(data["valor"]),
    )


class JSONProductoRepository:
    """Repositorio local para pruebas sin credenciales de Supabase."""

    def __init__(self, filepath: Path | None = None) -> None:
        self.filepath = filepath or settings.database_path

    def _read(self) -> list[dict]:
        if not self.filepath.exists():
            return []

        with self.filepath.open("r", encoding="utf-8") as file:
            data = json.load(file)

        normalized = []
        changed = False
        for index, item in enumerate(data, start=1):
            if "id" not in item:
                item["id"] = index
                changed = True
            normalized.append(item)

        if changed:
            self._write(normalized)

        return normalized

    def _write(self, productos: list[dict]) -> None:
        self.filepath.parent.mkdir(parents=True, exist_ok=True)
        with self.filepath.open("w", encoding="utf-8") as file:
            json.dump(productos, file, indent=2, ensure_ascii=False)

    def _next_id(self, productos: list[dict]) -> int:
        if not productos:
            return 1
        return max(int(producto["id"]) for producto in productos) + 1

    def list(self) -> list[ProductoResponse]:
        return [_to_response(producto) for producto in self._read()]

    def get_by_id(self, producto_id: int) -> ProductoResponse | None:
        for producto in self._read():
            if int(producto["id"]) == producto_id:
                return _to_response(producto)
        return None

    def get_by_codigo(self, codigo: str) -> ProductoResponse | None:
        for producto in self._read():
            if producto["codigo"] == codigo:
                return _to_response(producto)
        return None

    def create(self, producto: ProductoCreate) -> ProductoResponse:
        productos = self._read()
        nuevo = producto.model_dump()
        nuevo["id"] = self._next_id(productos)
        productos.append(nuevo)
        self._write(productos)
        return _to_response(nuevo)

    def update(self, producto_id: int, data: ProductoUpdate) -> ProductoResponse | None:
        productos = self._read()
        cambios = data.model_dump(exclude_unset=True, exclude_none=True)

        for index, producto in enumerate(productos):
            if int(producto["id"]) == producto_id:
                producto.update(cambios)
                productos[index] = producto
                self._write(productos)
                return _to_response(producto)

        return None

    def delete(self, producto_id: int) -> bool:
        productos = self._read()
        filtrados = [p for p in productos if int(p["id"]) != producto_id]

        if len(filtrados) == len(productos):
            return False

        self._write(filtrados)
        return True


class SupabaseProductoRepository:
    """Repositorio de productos conectado a Supabase."""

    def __init__(self, table_name: str | None = None) -> None:
        self.client = get_supabase_client()
        self.table_name = table_name or settings.supabase_table_productos

    def _table(self):
        return self.client.table(self.table_name)

    def list(self) -> list[ProductoResponse]:
        response = self._table().select("*").order("id").execute()
        return [_to_response(producto) for producto in response.data or []]

    def get_by_id(self, producto_id: int) -> ProductoResponse | None:
        response = self._table().select("*").eq("id", producto_id).limit(1).execute()
        data = response.data or []
        return _to_response(data[0]) if data else None

    def get_by_codigo(self, codigo: str) -> ProductoResponse | None:
        response = self._table().select("*").eq("codigo", codigo).limit(1).execute()
        data = response.data or []
        return _to_response(data[0]) if data else None

    def create(self, producto: ProductoCreate) -> ProductoResponse:
        response = self._table().insert(producto.model_dump()).execute()
        return _to_response(response.data[0])

    def update(self, producto_id: int, data: ProductoUpdate) -> ProductoResponse | None:
        cambios = data.model_dump(exclude_unset=True, exclude_none=True)
        if not cambios:
            return self.get_by_id(producto_id)

        response = self._table().update(cambios).eq("id", producto_id).execute()
        data_response = response.data or []
        return _to_response(data_response[0]) if data_response else None

    def delete(self, producto_id: int) -> bool:
        response = self._table().delete().eq("id", producto_id).execute()
        return bool(response.data)


def build_producto_repository() -> ProductoRepository:
    """Construye el repositorio adecuado segun la configuracion."""

    if settings.use_supabase and settings.supabase_configured:
        return SupabaseProductoRepository()

    return JSONProductoRepository()
