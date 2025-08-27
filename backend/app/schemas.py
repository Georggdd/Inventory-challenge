"""
Define los esquemas (Pydantic) para validar datos de usuarios, productos y movimientos de stock.
"""

from datetime import datetime, timedelta
from pydantic import BaseModel, Field, field_validator, EmailStr

# ---------- Autentificación ----------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=128)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

# ---------- Productos ----------
class ProductBase(BaseModel):
    sku: str = Field(min_length=1, max_length=64)
    ean13: str = Field(min_length=13, max_length=13)
    name: str

    @field_validator("ean13")
    @classmethod
    def validate_ean13(cls, v: str):
        if not v.isdigit() or len(v) != 13:
            raise ValueError("EAN13 debe tener 13 dígitos")
        return v

class ProductCreate(ProductBase):
    stock_qty: int = 0

class ProductOut(BaseModel):
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
    product_id: int
    delta: int
    reason: str | None = None

class MovementOut(BaseModel):
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
    quantity: int = Field(ge=0)
    reason: str | None = None
