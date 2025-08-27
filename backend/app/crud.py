"""
Gestiona la autenticación de usuarios y la generación de tokens JWT.
Incluye registro, login, verificación de contraseñas y dependencia condicional de autenticación.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Product, StockMovement

def list_products(db: Session) -> list[Product]:
    return db.execute(select(Product).order_by(Product.id.asc())).scalars().all()

def get_product(db: Session, product_id: int) -> Product | None:
    return db.get(Product, product_id)

def get_product_by_sku(db: Session, sku: str) -> Product | None:
    return db.execute(select(Product).where(Product.sku == sku)).scalars().first()

def create_product(db: Session, sku: str, ean13: str, name: str, stock_qty: int = 0) -> Product:
    p = Product(sku=sku, ean13=ean13, name=name, stock_qty=stock_qty)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def record_movement(db: Session, product: Product, delta: int, reason: str | None, mtype: str) -> StockMovement:
    before = product.stock_qty
    after = product.stock_qty + delta
    product.stock_qty = after
    m = StockMovement(product_id=product.id, delta=delta, qty_before=before, qty_after=after, reason=reason, type=mtype)
    db.add(m)
    db.commit()
    db.refresh(m)
    db.refresh(product)
    return m

def set_stock(db: Session, product: Product, quantity: int, reason: str | None) -> StockMovement:
    delta = quantity - product.stock_qty
    return record_movement(db, product, delta=delta, reason=reason, mtype="ADJUST")

def list_movements(db: Session, product_id: int | None = None, limit: int = 100) -> list[StockMovement]:
    q = select(StockMovement).order_by(StockMovement.created_at.desc())
    if product_id:
        q = q.where(StockMovement.product_id == product_id)
    q = q.limit(limit)
    return db.execute(q).scalars().all()
