from uuid import uuid4

from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.models import JobModel


app = FastAPI(
    title="TalentMatch AI",
    description="API de análisis asistido de CV y ofertas laborales.",
    version="0.1.0",
)


# Datos que recibimos al crear una oferta
class JobCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    description: str = Field(min_length=10, max_length=10000)
    requirements: list[str] = Field(min_length=1, max_length=30)


# Datos que devolveremos
class Job(JobCreate):
    id: str


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