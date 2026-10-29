
from fastapi.testclient import TestClient

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from main import app, jobs


client = TestClient(app)


def setup_function():
    # Cada prueba comienza con la lista de ofertas vacía.
    jobs.clear()


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_create_job():
    payload = {
        "title": "Desarrollador Backend Junior",
        "description": (
            "Buscamos un desarrollador junior para crear APIs REST."
        ),
        "requirements": [
            "Conocimientos de Python",
            "Conocimientos de SQL",
        ],
    }

    response = client.post("/jobs", json=payload)

    assert response.status_code == 201

    data = response.json()
    assert data["title"] == payload["title"]
    assert data["id"]


def test_list_jobs():
    payload = {
        "title": "Desarrollador Python",
        "description": "Desarrollo de servicios backend con Python.",
        "requirements": ["Python", "APIs REST"],
    }

    client.post("/jobs", json=payload)

    response = client.get("/jobs")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_existing_job():
    payload = {
        "title": "Backend Junior",
        "description": "Desarrollo de APIs para aplicaciones web.",
        "requirements": ["Python"],
    }

    created = client.post("/jobs", json=payload).json()
    response = client.get(f"/jobs/{created['id']}")

    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_missing_job():
    response = client.get("/jobs/id-inexistente")

    assert response.status_code == 404


def test_reject_invalid_job():
    payload = {
        "title": "AB",
        "description": "Corta",
        "requirements": [],
    }

    response = client.post("/jobs", json=payload)

    assert response.status_code == 422
