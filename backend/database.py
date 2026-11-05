import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session

from backend.models import Base

# Ubicación de la carpeta raíz del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno
load_dotenv(BASE_DIR / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("No se encontró DATABASE_URL en el archivo .env")

# Motor de conexión
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)

# Fábrica de sesiones
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_connection():
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))


def create_tables():
    Base.metadata.create_all(bind=engine)