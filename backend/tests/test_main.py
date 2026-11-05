
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1].parent))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from backend.main import app
from backend.database import get_db
from backend.models import Base


# Base de datos SQLite temporal para las pruebas
TEST_DATABASE_URL = "sqlite://"

test_engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autoflush=False,
    autocommit=False,
)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client():
    Base.metadata.create_all(bind=test_engine)

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_health_check(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_job(client):
    payload = {
        "title": "Desarrollador Backend Junior",
        "description": "Buscamos un desarrollador junior para crear APIs REST.",
        "requirements": ["Python", "SQL"],
    }

    response = client.post("/jobs", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["id"]


def test_list_jobs(client):
    payload = {
        "title": "Desarrollador Python",
        "description": "Desarrollo de servicios backend con Python.",
        "requirements": ["Python", "APIs REST"],
    }

    client.post("/jobs", json=payload)

    response = client.get("/jobs")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_existing_job(client):
    payload = {
        "title": "Backend Junior",
        "description": "Desarrollo de APIs para aplicaciones web.",
        "requirements": ["Python"],
    }

    created = client.post("/jobs", json=payload).json()
    response = client.get(f"/jobs/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_job(client):
    response = client.get("/jobs/id-inexistente")

    assert response.status_code == 404


def test_reject_invalid_job(client):
    payload = {
        "title": "AB",
        "description": "Corta",
        "requirements": [],
    }

    response = client.post("/jobs", json=payload)

    assert response.status_code == 422
