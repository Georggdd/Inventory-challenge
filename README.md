# Inventory Challenge — FastAPI + React + PostgreSQL

Prueba técnica completa con **FastAPI** (Python), **React (Vite)** y **PostgreSQL**. Incluye:
- Listado y actualización de stock (ajuste y movimientos IN/OUT).
- Historial de movimientos de stock.
- API REST con **FastAPI** y **SQLAlchemy**.
- **PostgreSQL** como base de datos (vía Docker).
- **JWT** opcional (bonus) y **tests** básicos de API con `pytest` (bonus).
- Frontend en **React (Vite)**.

> Diseñado para correr rápido con `docker compose` (solo la base de datos) y dos terminales locales para backend y frontend. También puedes dockerizar todo si quieres, pero aquí prima la claridad y velocidad de ejecución.

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

## 3) Arrancar PostgreSQL con Docker
```bash
docker compose up -d db
# Espera unos segundos a que la base de datos esté lista
```

## 4) Backend (FastAPI)
En una terminal:
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # en Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Crea tablas y datos de ejemplo (usuarios y productos)
# Se ejecuta automáticamente al levantar, pero puedes forzarlo con:
python -m app.seed

# Arrancar API
uvicorn app.main:app --reload
```
Por defecto expone en `http://localhost:8000` y docs en `http://localhost:8000/docs`.

### Tests (bonus)
```bash
pytest -q
```

## 5) Frontend (React + Vite)
En otra terminal:
```bash
cd frontend
pnpm install  # o: npm install
pnpm dev      # o: npm run dev
```
Vite sirve la app en `http://localhost:5173`.

## 6) Flujos en la UI
- **Inventario**: ver SKU, EAN13, nombre y cantidad.
- **Actualizar stock**: dos opciones en cada fila:
  - **Ajustar**: establece una cantidad absoluta (p.ej., 120). Registra movimiento tipo `ADJUST`.
  - **Movimiento**: aplica un delta positivo/negativo (p.ej., +20 entrada, -5 salida). Registra `IN`/`OUT`.
- **Historial**: lista de movimientos más recientes con filtros por producto.

## 7) Auth (bonus, opcional)
Por defecto **NO es obligatorio**. Actívalo poniendo en `.env`:
```
REQUIRE_AUTH=true
JWT_SECRET=un_secreto_largo
```
Endpoints:
- `POST /auth/register` { email, password }
- `POST /auth/login` { email, password } → `access_token` (Bearer)

## 8) Estructura
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

## 9) Endpoints principales
- `GET /api/products`
- `PATCH /api/products/{id}/stock`  (ajuste absoluto)
- `POST /api/movements`  (delta positivo/negativo)
- `GET /api/movements?product_id=&limit=`

## 10) Notas
- Los tests usan SQLite en memoria para ir rápido.
- La API valida EAN13 sencillamente (13 dígitos).
- Todo el código es didáctico y está documentado.
- Si quieres dockerizar también backend/frontend, añade servicios al `docker-compose.yml` o crea Dockerfiles (dejé comentarios en el README y en el código para ello).
