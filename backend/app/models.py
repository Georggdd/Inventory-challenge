"""
Define los modelos de la base de datos: usuarios, productos y movimientos de stock.
Incluye relaciones entre productos y sus movimientos y restricciones de integridad.
"""

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .database import Base

class User(Base):
    # Modelo de usuario con email único y hash de contraseña
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Product(Base):
    # Modelo de producto con SKU, EAN13, nombre y cantidad en stock
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(64), unique=True, index=True, nullable=False)
    ean13: Mapped[str] = mapped_column(String(13), unique=True, index=True, nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    stock_qty: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    movements: Mapped[list["StockMovement"]] = relationship(
        back_populates="product", cascade="all, delete-orphan"
    )  # Relación a los movimientos de stock

class StockMovement(Base):
    # Modelo de movimiento de stock: registra entradas, salidas o ajustes
    __tablename__ = "stock_movements"
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"), index=True, nullable=False)
    delta: Mapped[int] = mapped_column(Integer, nullable=False)  # Cantidad agregada (+) o retirada (-)
    qty_before: Mapped[int] = mapped_column(Integer, nullable=False)
    qty_after: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)  # Motivo del movimiento
    type: Mapped[str] = mapped_column(String(16), nullable=False)  # IN / OUT / ADJUST
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    product: Mapped["Product"] = relationship(back_populates="movements")  # Relación inversa a producto

    __table_args__ = (
        CheckConstraint("type in ('IN','OUT','ADJUST')", name="movement_type_check"),  # Restricción de tipo
    )
