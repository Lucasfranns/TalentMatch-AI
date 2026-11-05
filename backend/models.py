from sqlalchemy import (
    String,
    Text,
    JSON,
    Integer,
    ForeignKey,
    DateTime,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


# Clase base para nuestros modelos
class Base(DeclarativeBase):
    pass


# Modelo de ofertas laborales
class JobModel(Base):
    __tablename__ = "jobs"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(120),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    requirements: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )
    

class ResumeModel(Base):
    __tablename__ = "resumes"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    file_path: Mapped[str] = mapped_column(String(500), nullable=False)
    extracted_text: Mapped[str] = mapped_column(Text, nullable=False)


class AnalysisModel(Base):
    __tablename__ = "analyses"

    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
    )

    job_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("jobs.id"),
        nullable=False,
    )

    resume_id: Mapped[str] = mapped_column(
        String(36),
        ForeignKey("resumes.id"),
        nullable=False,
    )

    match_percentage: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    matched_requirements: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    missing_requirements: Mapped[list[str]] = mapped_column(
        JSON,
        nullable=False,
    )

    summary: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )