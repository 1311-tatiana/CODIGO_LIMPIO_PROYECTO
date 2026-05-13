"""Schemas Pydantic para la entidad Producto."""

from pydantic import BaseModel, ConfigDict, Field


class ProductoBase(BaseModel):
    """Campos comunes de un producto."""

    codigo: str = Field(..., min_length=1, max_length=50, examples=["P001"])
    nombre: str = Field(..., min_length=1, max_length=120, examples=["Martillo"])
    cantidad: int = Field(..., ge=0, examples=[10])
    valor: float = Field(..., gt=0, examples=[15000.0])


class ProductoCreate(ProductoBase):
    """Datos requeridos para crear un producto."""


class ProductoUpdate(BaseModel):
    """Datos permitidos para actualizar un producto parcialmente."""

    codigo: str | None = Field(default=None, min_length=1, max_length=50)
    nombre: str | None = Field(default=None, min_length=1, max_length=120)
    cantidad: int | None = Field(default=None, ge=0)
    valor: float | None = Field(default=None, gt=0)


class ProductoResponse(ProductoBase):
    """Respuesta enviada por la API al consultar productos."""

    model_config = ConfigDict(from_attributes=True)

    id: int
