from datetime import datetime
from typing import Optional

from sqlalchemy import Column, String, DateTime, DECIMAL
from sqlmodel import SQLModel, Field, Relationship

from models import Worker, User


class Vacancy(SQLModel, table=True):
    __tablename__ = "vacancies"

    id: Optional[int] = Field(primary_key=True)
    title: str = Field(sa_column=Column(String(64), nullable=False))
    description: Optional[str] = Field(sa_column=Column(String(1000), nullable=False))
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True)))
    salary: float = Field(sa_column=Column(DECIMAL(10, 2)))
    worker_id: int = Field(foreign_key="workers.id", nullable=False, ondelete="CASCADE")
    worker: Worker = Relationship(back_populates="vacancies")
    user_id: Optional[int] = Field(foreign_key="users.id", ondelete="CASCADE")
    user: User = Relationship(back_populates="vacancies")
