"""
Pruebas automatizadas (pytest) de la API de inventario usando FastAPI TestClient y una base de datos SQLite en memoria.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import Base, get_db

# SQLite en memoria compartida entre hilos con StaticPool
TEST_DB_URL = "sqlite:///:memory:"

engine = create_engine(
    TEST_DB_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool  # <- clave para que TestClient vea las tablas
)

TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# Crear todas las tablas antes de tests
Base.metadata.create_all(bind=engine)

# Sobrescribir la dependencia get_db de FastAPI
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def cleanup_db():
    # Limpiar la BD después de cada test
    yield
    # Opcional: si se quieren resetear datos entre tests:
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_inventory_flow():
    # Crear producto
    payload = {"sku":"SKU-XYZ","ean13":"1234567899999","name":"Tester","stock_qty":10}
    r = client.post("/api/products", json=payload)
    assert r.status_code == 200, r.text
    product = r.json()
    pid = product["id"]
    assert product["stock_qty"] == 10

    # Movimiento IN +5
    r = client.post("/api/movements", json={"product_id": pid, "delta": 5})
    assert r.status_code == 200, r.text
    assert r.json()["qty_after"] == 15

    # Ajuste a 7
    r = client.patch(f"/api/products/{pid}/stock", json={"quantity": 7, "reason": "Inventario"})
    assert r.status_code == 200
    assert r.json()["qty_after"] == 7

    # Listar movimientos
    r = client.get(f"/api/movements?product_id={pid}")
    assert r.status_code == 200
    assert len(r.json()) == 2

    # Listar productos
    r = client.get("/api/products")
    assert r.status_code == 200
    assert any(p["id"] == pid for p in r.json())
