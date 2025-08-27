"""Pequeño script de seed para crear tablas y datos de ejemplo en la base de datos."""

import os
from sqlalchemy.orm import Session

from .database import Base, engine, SessionLocal
from .models import Product, User
from .auth import hash_password

def seed(db: Session):
    """Crea datos iniciales si no existen usuarios o productos"""

    # Crear un usuario administrador si no existe ninguno
    if not db.query(User).first():
        u = User(email="admin@example.com", password_hash=hash_password("admin123"))
        db.add(u)

    # Crear productos de ejemplo si la tabla está vacía
    if not db.query(Product).first():
        items = [
            ("SKU-001", "1234567890123", "Perfume A", 50),
            ("SKU-002", "1234567890124", "Perfume B", 20),
            ("SKU-003", "1234567890125", "Perfume C", 0),
        ]
        for sku, ean, name, qty in items:
            db.add(Product(sku=sku, ean13=ean, name=name, stock_qty=qty))
    db.commit()  # Guardar los cambios en la base de datos

def main():
    """Crea las tablas y ejecuta el seed"""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed(db)
        print("Seed completado.")  # Confirmación por consola
    finally:
        db.close()  # Cierra la sesión para liberar recursos

if __name__ == "__main__":
    main()  # Ejecuta el script si se llama directamente
