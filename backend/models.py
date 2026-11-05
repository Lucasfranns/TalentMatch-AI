from sqlalchemy import String, Text, JSON
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