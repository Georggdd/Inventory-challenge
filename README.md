# Inventory Challenge — FastAPI + React + PostgreSQL

Prueba técnica completa con **FastAPI** (Python), **React (Vite)** y **PostgreSQL**. Incluye:
- Listado y actualización de stock (ajuste y movimientos IN/OUT).
- Historial de movimientos de stock.
- API REST con **FastAPI** y **SQLAlchemy**.
- **PostgreSQL** como base de datos (vía Docker).
- **JWT** y **tests** básicos de API con `pytest`.
- Frontend en **React (Vite)**.

> Diseñado para correr rápido con `docker compose` (solo la base de datos) y dos terminales locales para backend y frontend. 

---

## 1) Requisitos
- Python 3.11+
- Node 18+ y pnpm o npm
- Docker y Docker Compose

## 2) Variables de entorno
Copia el ejemplo:
```bash
cp .env.example .env
```
Modifica lo que necesites. Por defecto: usuario `postgres`/`postgres`, db `inventory` en `localhost:5432`.

Para habilitar autenticación JWT:

REQUIRE_AUTH=true
JWT_SECRET=un_secreto_largo

## 3) Arrancar PostgreSQL con Docker
```bash
docker compose up -d db
```

## 4) Backend (FastAPI)
En una terminal:
```bash
cd backend
python -m venv .venv
source .venv\Scripts\activate #Windows
pip install -r requirements.txt

# Crea tablas y datos de ejemplo (usuarios y productos)
python -m app.seed

# Arrancar API
uvicorn app.main:app --reload
```
Por defecto expone en `http://localhost:8000` y docs en `http://localhost:8000/docs`.

### Tests 
```bash
pytest -q
```

## 5) Frontend (React + Vite)
En otra terminal:
```bash
cd frontend
npm install
npm run dev
```
Vite sirve la app en `http://localhost:5173`.

## 6) Mini-flujo de prueba de la API (Postman)


## Verificar que el servidor está vivo
Método: GET
URL: http://localhost:8000/health
Body: ninguno

Respuesta esperada:
{"status":"ok"}


## Obtener token (si auth activada)
Método: POST
URL: http://localhost:8000/auth/login
Body (JSON):
{
  "username": "admin@example.com",
  "password": "admin123"
}

Respuesta esperada:
{
  "access_token": "<tu_token>",
  "token_type": "bearer"
}


## Listar productos
Método: GET
URL: http://localhost:8000/api/products
Headers:
Authorization: Bearer <tu_token>


Respuesta: array con productos existentes.


## Crear un producto
Método: POST
URL: http://localhost:8000/api/products
Headers: igual que antes
Body (JSON):
{
  "sku": "PROD001",
  "ean13": "1234567890123",
  "name": "Producto de prueba",
  "stock_qty": 50
}

Respuesta: producto creado con id.


## Ajustar stock
Método: PATCH
URL: http://localhost:8000/api/products/<product_id>/stock
Body (JSON):
{
  "quantity": 10,
  "reason": "Ajuste inicial"
}

Respuesta: detalles del movimiento de stock:
{
  "id": 1,
  "product_id": 4,
  "delta": -40,
  "qty_after": 10,
  "reason": "Ajuste inicial",
  "timestamp": "2025-08-27T12:34:56.789Z"
}


## Listar movimientos
Método: GET
URL: http://localhost:8000/api/movements
Respuesta: lista con todos los movimientos de stock.


## 7) Flujos en la UI
```
Inventario: ver SKU, EAN13, nombre y cantidad.
Actualizar stock:
- Ajustar: establece cantidad absoluta → registra movimiento ADJUST.
- Movimiento: aplica delta positivo/negativo → registra IN/OUT.
Historial: lista de movimientos recientes, con filtros por producto.

```
## 8) Endpoints principales 
```
- GET /api/products
- POST /api/products
- PATCH /api/products/{id}/stock (ajuste absoluto, crea movimiento)
- GET /api/movements?product_id=&limit=

Todos requieren token JWT (excepto /health).

```

## 9) Estructura
```
inventory-challenge/
├─ backend/
│  ├─ app/
│  │  ├─ main.py
│  │  ├─ database.py
│  │  ├─ models.py
│  │  ├─ schemas.py
│  │  ├─ auth.py
│  │  ├─ crud.py
│  │  ├─ deps.py
│  │  └─ seed.py
│  ├─ tests/
│  │  └─ test_api.py
│  │  └─ test_db.py
│  └─ requirements.txt
├─ frontend/
│  ├─ index.html
│  ├─ package.json
│  ├─ vite.config.js
│  └─ src/
│     ├─ main.jsx
│     ├─ App.jsx
│     ├─ api.js
│     └─ components/
│        ├─ InventoryTable.jsx
│        ├─ Movements.jsx
│        └─ Login.jsx
├─ docker-compose.yml
├─ .env.example
└─ .env  (lo creas tú)
```

