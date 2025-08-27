"""
Define los esquemas Pydantic para validar y serializar datos de usuarios, productos y movimientos de stock.
Incluye validaciones, formatos de salida y estructuras para creación y lectura.
"""

from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator, EmailStr

# ---------- Autenticación ----------
class Token(BaseModel):
    # Representa un token JWT devuelto al login
    access_token: str
    token_type: str = "bearer"  # Tipo de token, siempre "bearer"

class UserCreate(BaseModel):
    # Datos requeridos para registrar un usuario
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)  # Validación de longitud mínima y máxima

class UserOut(BaseModel):
    # Esquema de salida para usuario
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # Permite crear desde modelos SQLAlchemy

# ---------- Productos ----------
class ProductBase(BaseModel):
    # Campos básicos de un producto
    sku: str = Field(min_length=1, max_length=64)
    ean13: str = Field(min_length=13, max_length=13)
    name: str

    @field_validator("ean13")
    @classmethod
    def validate_ean13(cls, v: str):
        # Valida que EAN13 tenga 13 dígitos numéricos
        if not v.isdigit() or len(v) != 13:
            raise ValueError("EAN13 debe tener 13 dígitos")
        return v

class ProductCreate(ProductBase):
    # Datos para crear un producto, incluye cantidad inicial en stock
    stock_qty: int = 0

class ProductOut(BaseModel):
    # Esquema de salida de un producto
    id: int
    sku: str
    ean13: str
    name: str
    stock_qty: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True

# ---------- Movimientos ----------
class MovementCreate(BaseModel):
    # Datos necesarios para registrar un movimiento de stock
    product_id: int
    delta: int
    reason: str | None = None

class MovementOut(BaseModel):
    # Esquema de salida para un movimiento de stock
    id: int
    product_id: int
    delta: int
    qty_before: int
    qty_after: int
    reason: str | None
    type: str
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- Ajustes ----------
class StockAdjust(BaseModel):
    # Datos para ajustar el stock a una cantidad exacta
    quantity: int = Field(ge=0)  # No se permite valor negativo
    reason: str | None = None
