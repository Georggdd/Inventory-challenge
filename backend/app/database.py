"""
Configuración de la base de datos: motor, sesión y dependencias para SQLAlchemy.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/inventory")

class Base(DeclarativeBase):
    pass

def make_engine(url: str | None = None):
    return create_engine(url or DATABASE_URL, pool_pre_ping=True)

engine = make_engine()
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
