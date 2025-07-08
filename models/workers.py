from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, String, DateTime
from sqlmodel import SQLModel, Field, Relationship


class Worker(SQLModel, table=True):
    __tablename__ = "workers"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(sa_column=Column(String(20), nullable=False))
    last_name: str = Field(sa_column=Column(String(20), nullable=False))
    biography: str = Field(sa_column=Column(String(250)))
    birth_date: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True)))
    vacancies_list: List["Vacancy"] = Relationship(back_populates="workers")
