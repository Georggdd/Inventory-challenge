"""
Configuración de la base de datos: motor, sesión y dependencias para SQLAlchemy.
Permite conectarse a PostgreSQL u otra base de datos según la URL definida en el entorno.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# URL de conexión a la base de datos (se puede cambiar con la variable de entorno DATABASE_URL)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/inventory")

class Base(DeclarativeBase):
    """
    Clase base para los modelos de SQLAlchemy.
    Todos los modelos (Product, User, StockMovement, etc.) heredan de esta clase.
    """
    pass

def make_engine(url: str | None = None):
    """
    Crea el motor de SQLAlchemy para conectarse a la base de datos.
    Se activa pool_pre_ping para evitar errores de conexión por timeout.
    """
    return create_engine(url or DATABASE_URL, pool_pre_ping=True)

# Motor de base de datos global
engine = make_engine()

# Fábrica de sesiones para interactuar con la base de datos
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    """
    Dependencia de FastAPI que devuelve una sesión de base de datos.
    Garantiza que la sesión se cierre correctamente después de usarla.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
