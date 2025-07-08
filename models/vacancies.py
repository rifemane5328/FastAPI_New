from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime
from sqlmodel import SQLModel, Field, Relationship

from models import Worker


class Vacancy(SQLModel, table=True):
    __tablename__ = "vacancies"

    id: Optional[int] = Field(primary_key=True)
    title: str = Field(sa_column=Column(String(64), nullable=False))
    description: Optional[str] = Field(sa_column=Column(String(1000), nullable=False))
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True)))
    salary: int = Field(sa_column=Column(String(10)))
    worker_id: int = Field(foreign_key="workers.id", nullable=False, ondelete="CASCADE")
    worker: Worker = Relationship(back_populates="vacancies")
