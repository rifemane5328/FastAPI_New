from datetime import date
from typing import Optional, List

from sqlalchemy import Column, String, Date
from sqlmodel import SQLModel, Field, Relationship


class Worker(SQLModel, table=True):
    __tablename__ = "workers"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(sa_column=Column(String(20), nullable=False))
    last_name: str = Field(sa_column=Column(String(20), nullable=False))
    biography: str = Field(sa_column=Column(String(250)))
    birth_date: Optional[date] = Field(sa_column=Column(Date()))
    vacancies: List["Vacancy"] = Relationship(back_populates="worker", cascade_delete=True)
