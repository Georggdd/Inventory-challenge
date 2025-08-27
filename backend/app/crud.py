"""
Gestiona operaciones de inventario: productos y movimientos de stock.
Incluye funciones para listar, crear productos, registrar movimientos y ajustar stock.
"""

from sqlalchemy.orm import Session
from sqlalchemy import select
from .models import Product, StockMovement

def list_products(db: Session) -> list[Product]:
    
    # Devuelve todos los productos de la base de datos ordenados por ID ascendente.
    
    return db.execute(select(Product).order_by(Product.id.asc())).scalars().all()

def get_product(db: Session, product_id: int) -> Product | None:
    
    # Recupera un producto por su ID. Devuelve None si no existe.
    
    return db.get(Product, product_id)

def get_product_by_sku(db: Session, sku: str) -> Product | None:
    
    # Recupera un producto por su SKU. Devuelve None si no existe.
    
    return db.execute(select(Product).where(Product.sku == sku)).scalars().first()

def create_product(db: Session, sku: str, ean13: str, name: str, stock_qty: int = 0) -> Product:
    """
    Crea un nuevo producto con el SKU, EAN13, nombre y cantidad inicial de stock.
    Guarda el producto en la base de datos y lo devuelve.
    """
    p = Product(sku=sku, ean13=ean13, name=name, stock_qty=stock_qty)
    db.add(p)
    db.commit()
    db.refresh(p)
    return p

def record_movement(db: Session, product: Product, delta: int, reason: str | None, mtype: str) -> StockMovement:
    """
    Registra un movimiento de stock para un producto.
    - delta: cantidad a sumar (+) o restar (-)
    - reason: motivo del movimiento (opcional)
    - mtype: tipo de movimiento ('IN', 'OUT' o 'ADJUST')
    Actualiza la cantidad de stock del producto y crea un registro en StockMovement.
    """
    before = product.stock_qty
    after = product.stock_qty + delta
    product.stock_qty = after
    m = StockMovement(
        product_id=product.id,
        delta=delta,
        qty_before=before,
        qty_after=after,
        reason=reason,
        type=mtype
    )
    db.add(m)
    db.commit()
    db.refresh(m)
    db.refresh(product)
    return m

def set_stock(db: Session, product: Product, quantity: int, reason: str | None) -> StockMovement:
    """
    Ajusta el stock de un producto a una cantidad exacta.
    Crea un movimiento de tipo 'ADJUST' registrando la diferencia entre el stock actual y la nueva cantidad.
    """
    delta = quantity - product.stock_qty
    return record_movement(db, product, delta=delta, reason=reason, mtype="ADJUST")

def list_movements(db: Session, product_id: int | None = None, limit: int = 100) -> list[StockMovement]:
    """
    Lista movimientos de stock.
    - Se pueden filtrar por ID de producto.
    - Se limita el número de resultados (por defecto 100) ordenados por fecha descendente.
    """
    q = select(StockMovement).order_by(StockMovement.created_at.desc())
    if product_id:
        q = q.where(StockMovement.product_id == product_id)
    q = q.limit(limit)
    return db.execute(q).scalars().all()
