from uuid import uuid4
from pathlib import Path
from io import BytesIO

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from pypdf import PdfReader

from backend.database import get_db
from backend.models import JobModel, ResumeModel

app = FastAPI(
    title="TalentMatch AI",
    description="API de análisis asistido de CV y ofertas laborales.",
    version="0.1.0",
)

BASE_DIR = Path(__file__).resolve().parent.parent
UPLOAD_DIR = BASE_DIR / "uploads" / "resumes"

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB


# Datos que recibimos al crear una oferta
class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=10000)
    requirements: list[str] = Field(min_length=1, max_length=30)


# Datos que devolveremos
class Job(JobCreate):
    id: str

class ResumeSummary(BaseModel):
    id: str
    filename: str


class ResumeDetail(ResumeSummary):
    extracted_text: str


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "TalentMatch AI",
    }


@app.post("/jobs", response_model=Job, status_code=201)
def create_job(job_data: JobCreate, db: Session = Depends(get_db)):
    job = JobModel(
        id=str(uuid4()),
        **job_data.model_dump(),
    )

    db.add(job)
    db.commit()
    db.refresh(job)

    return job


@app.get("/jobs", response_model=list[Job])
def list_jobs(db: Session = Depends(get_db)):
    return db.query(JobModel).all()


@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str, db: Session = Depends(get_db)):
    job = db.get(JobModel, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Oferta laboral no encontrada",
        )

    return job


@app.put("/jobs/{job_id}", response_model=Job)
def update_job(
    job_id: str,
    job_data: JobCreate,
    db: Session = Depends(get_db),
):
    job = db.get(JobModel, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Oferta laboral no encontrada",
        )

    job.title = job_data.title
    job.description = job_data.description
    job.requirements = job_data.requirements

    db.commit()
    db.refresh(job)

    return job


@app.delete("/jobs/{job_id}", status_code=204)
def delete_job(job_id: str, db: Session = Depends(get_db)):
    job = db.get(JobModel, job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Oferta laboral no encontrada",
        )

    db.delete(job)
    db.commit()

    return None

@app.post("/resumes", status_code=201)
def upload_resume(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    # Validar extensión
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="El archivo debe tener extensión PDF",
        )

    # Leer el archivo y controlar su tamaño
    file_content = file.file.read(MAX_FILE_SIZE + 1)

    if len(file_content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="El archivo supera el límite de 10 MB",
        )

    # Comprobar que realmente tenga estructura PDF
    if not file_content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=400,
            detail="El archivo no es un PDF válido",
        )

    # Extraer texto del PDF
    try:
        reader = PdfReader(BytesIO(file_content))

        if reader.is_encrypted:
            raise HTTPException(
                status_code=400,
                detail="No se admiten PDF protegidos con contraseña",
            )

        extracted_text = "\n".join(
            page.extract_text() or ""
            for page in reader.pages
        ).strip()

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="No se pudo procesar el archivo PDF",
        )

    if not extracted_text:
        raise HTTPException(
            status_code=422,
            detail="No se pudo extraer texto del PDF. Puede ser un documento escaneado.",
        )

    # Generar un identificador único
    resume_id = str(uuid4())

    # Crear la carpeta si todavía no existe
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    # Guardar el archivo con un nombre único
    saved_filename = f"{resume_id}.pdf"
    saved_path = UPLOAD_DIR / saved_filename

    try:
        saved_path.write_bytes(file_content)
    except OSError:
        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar el archivo PDF",
        )
    
    # Registrar los datos en PostgreSQL
    resume = ResumeModel(
        id=resume_id,
        filename=Path(file.filename).name,
        file_path=f"uploads/resumes/{saved_filename}",
        extracted_text=extracted_text,
    )

    try:
        db.add(resume)
        db.commit()
        db.refresh(resume)

    except Exception:
        db.rollback()
        saved_path.unlink(missing_ok=True)
        raise HTTPException(
            status_code=500,
            detail="No se pudo guardar el currículum",
        )

    return {
        "id": resume.id,
        "filename": resume.filename,
        "extracted_text": resume.extracted_text,
    }
    
@app.get("/resumes", response_model=list[ResumeSummary])
def list_resumes(db: Session = Depends(get_db)):
    return db.query(ResumeModel).all()

@app.get("/resumes/{resume_id}", response_model=ResumeDetail)
def get_resume(resume_id: str, db: Session = Depends(get_db)):
    resume = db.get(ResumeModel, resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Currículum no encontrado",
        )

    return resume

@app.delete("/resumes/{resume_id}", status_code=204)
def delete_resume(
    resume_id: str,
    db: Session = Depends(get_db),
):
    resume = db.get(ResumeModel, resume_id)

    if resume is None:
        raise HTTPException(
            status_code=404,
            detail="Currículum no encontrado",
        )

    # Obtener la ubicación del archivo
    file_path = (BASE_DIR / resume.file_path).resolve()
    upload_dir = UPLOAD_DIR.resolve()

    # Verificar que el archivo esté dentro de la carpeta de CV
    if upload_dir not in file_path.parents:
        raise HTTPException(
            status_code=500,
            detail="La ubicación del archivo no es válida",
        )

    # Eliminar el registro de la base de datos
    db.delete(resume)
    db.commit()

    # Eliminar el archivo físico
    file_path.unlink(missing_ok=True)