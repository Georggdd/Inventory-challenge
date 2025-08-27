"""
Define la API de inventario: rutas para productos y movimientos, gestión de stock y autenticación.
"""

import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from .database import Base, engine, get_db
from .models import Product
from .schemas import ProductOut, MovementCreate, MovementOut, StockAdjust, ProductCreate
from .crud import list_products, get_product, record_movement, set_stock, create_product, list_movements
from .auth import router as auth_router
from .deps import RequireAuth

CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173")

# Crear tablas al iniciar la aplicación (para mayor simplicidad en las pruebas)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in CORS_ORIGINS.split(",")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/health")
def health():
    return {"status": "ok"}

# ------- Productos -------
@app.get("/api/products", response_model=list[ProductOut], tags=["inventory"])
def api_list_products(db: Session = Depends(get_db), _auth=Depends(RequireAuth)):
    return list_products(db)

@app.post("/api/products", response_model=ProductOut, tags=["inventory"])
def api_create_product(payload: ProductCreate, db: Session = Depends(get_db), _auth=Depends(RequireAuth)):
    return create_product(db, sku=payload.sku, ean13=payload.ean13, name=payload.name, stock_qty=payload.stock_qty)

@app.patch("/api/products/{product_id}/stock", response_model=MovementOut, tags=["inventory"])
def api_adjust_stock(product_id: int, payload: StockAdjust, db: Session = Depends(get_db), _auth=Depends(RequireAuth)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    movement = set_stock(db, product, quantity=payload.quantity, reason=payload.reason)
    return movement

# ------- Movimientos -------
@app.post("/api/movements", response_model=MovementOut, tags=["inventory"])
def api_create_movement(payload: MovementCreate, db: Session = Depends(get_db), _auth=Depends(RequireAuth)):
    product = get_product(db, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    mtype = "IN" if payload.delta >= 0 else "OUT"
    movement = record_movement(db, product, delta=payload.delta, reason=payload.reason, mtype=mtype)
    return movement

@app.get("/api/movements", response_model=list[MovementOut], tags=["inventory"])
def api_list_movements(product_id: int | None = None, limit: int = 100, db: Session = Depends(get_db), _auth=Depends(RequireAuth)):
    return list_movements(db, product_id=product_id, limit=limit)
