
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


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


# Almacenamiento temporal en memoria
jobs: dict[str, Job] = {}


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "project": "TalentMatch AI",
    }


@app.post("/jobs", response_model=Job, status_code=201)
def create_job(job_data: JobCreate):
    job_id = str(uuid4())

    job = Job(
        id=job_id,
        **job_data.model_dump(),
    )

    jobs[job_id] = job
    return job


@app.get("/jobs", response_model=list[Job])
def list_jobs():
    return list(jobs.values())


@app.get("/jobs/{job_id}", response_model=Job)
def get_job(job_id: str):
    job = jobs.get(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Oferta laboral no encontrada",
        )

    return job
