from datetime import datetime
from typing import List

from sqlmodel import SQLModel, Field


class VacancyResponseSchema(SQLModel):
    id: int
    title: str = Field(max_length=64)
    description: str = Field(max_length=1000)
    created_at: datetime
    salary: float
    worker_id: int


class VacancyListResponseSchema(SQLModel):
    items: List[VacancyResponseSchema]


class VacancyCreateSchema(SQLModel):
    title: str = Field(max_length=64)
    description: str = Field(max_length=1000)
    created_at: datetime
    salary: float
    worker_id: int
