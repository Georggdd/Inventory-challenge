import os
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db

# Usamos SQLite en memoria para tests
TEST_DB_URL = "sqlite+pysqlite:///:memory:"

engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

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
