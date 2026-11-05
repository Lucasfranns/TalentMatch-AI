
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
from backend.models import Base, ResumeModel


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

def test_update_existing_job(client):
    payload = {
        "title": "Backend Junior",
        "description": "Desarrollo de APIs para aplicaciones web.",
        "requirements": ["Python"],
    }

    created = client.post("/jobs", json=payload).json()

    updated_payload = {
        "title": "Backend Developer Semi Senior",
        "description": "Desarrollo de microservicios y APIs REST.",
        "requirements": ["Python", "PostgreSQL", "Docker"],
    }

    response = client.put(
        f"/jobs/{created['id']}",
        json=updated_payload,
    )

    assert response.status_code == 200
    assert response.json()["title"] == updated_payload["title"]
    assert response.json()["requirements"] == updated_payload["requirements"]


def test_update_missing_job(client):
    payload = {
        "title": "Backend Junior",
        "description": "Desarrollo de aplicaciones web.",
        "requirements": ["Python"],
    }

    response = client.put("/jobs/id-inexistente", json=payload)

    assert response.status_code == 404


def test_delete_existing_job(client):
    payload = {
        "title": "Backend Junior",
        "description": "Desarrollo de aplicaciones web.",
        "requirements": ["Python"],
    }

    created = client.post("/jobs", json=payload).json()

    response = client.delete(f"/jobs/{created['id']}")

    assert response.status_code == 204

    get_response = client.get(f"/jobs/{created['id']}")
    assert get_response.status_code == 404


def test_delete_missing_job(client):
    response = client.delete("/jobs/id-inexistente")

    assert response.status_code == 404
    
def test_list_resumes(client):
    db = TestingSessionLocal()

    resumes = [
        ResumeModel(
            id="resume-1",
            filename="cv_juan.pdf",
            file_path="uploads/resumes/resume-1.pdf",
            extracted_text="Experiencia en Python y SQL.",
        ),
        ResumeModel(
            id="resume-2",
            filename="cv_maria.pdf",
            file_path="uploads/resumes/resume-2.pdf",
            extracted_text="Experiencia en Java y PostgreSQL.",
        ),
    ]

    db.add_all(resumes)
    db.commit()
    db.close()

    response = client.get("/resumes")

    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_existing_resume(client):
    db = TestingSessionLocal()

    resume = ResumeModel(
        id="resume-123",
        filename="cv_juan.pdf",
        file_path="uploads/resumes/resume-123.pdf",
        extracted_text="Experiencia en Python y SQL.",
    )

    db.add(resume)
    db.commit()
    db.close()

    response = client.get("/resumes/resume-123")

    assert response.status_code == 200
    assert response.json()["filename"] == "cv_juan.pdf"
    assert response.json()["extracted_text"] == "Experiencia en Python y SQL."


def test_get_missing_resume(client):
    response = client.get("/resumes/id-inexistente")

    assert response.status_code == 404


def test_reject_non_pdf_resume(client):
    response = client.post(
        "/resumes",
        files={
            "file": (
                "documento.txt",
                b"Este archivo no es un PDF.",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El archivo debe tener extensión PDF"
    
def test_reject_invalid_pdf_content(client):
    response = client.post(
        "/resumes",
        files={
            "file": (
                "curriculum.pdf",
                b"Este contenido no es un PDF real.",
                "application/pdf",
            )
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "El archivo no es un PDF válido"
   
# Verificar que se pueda eliminar un currículum existente 
def test_delete_existing_resume(client, tmp_path, monkeypatch):
    import backend.main as main

    # Simular la estructura de carpetas del proyecto
    upload_dir = tmp_path / "uploads" / "resumes"
    upload_dir.mkdir(parents=True)

    # Redirigir las rutas a la carpeta temporal
    monkeypatch.setattr(main, "BASE_DIR", tmp_path)
    monkeypatch.setattr(main, "UPLOAD_DIR", upload_dir)

    pdf_path = upload_dir / "resume-123.pdf"
    pdf_path.write_bytes(b"PDF de prueba")

    db = TestingSessionLocal()

    resume = ResumeModel(
        id="resume-123",
        filename="cv_juan.pdf",
        file_path="uploads/resumes/resume-123.pdf",
        extracted_text="Experiencia en Python.",
    )

    db.add(resume)
    db.commit()
    db.close()

    response = client.delete("/resumes/resume-123")

    assert response.status_code == 204
    assert not pdf_path.exists()

    response = client.get("/resumes")

    assert response.status_code == 200
    assert len(response.json()) == 0
    
# Verificar que no se pueda eliminar un currículum inexistente
def test_delete_missing_resume(client):
    response = client.delete("/resumes/id-inexistente")

    assert response.status_code == 404
    assert response.json()["detail"] == "Currículum no encontrado"