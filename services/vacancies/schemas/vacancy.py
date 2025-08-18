from datetime import datetime
from typing import List, Optional

from sqlmodel import SQLModel, Field


class VacancyResponseSchema(SQLModel):
    id: int
    title: str = Field(max_length=64)
    description: str = Field(max_length=1000)
    created_at: datetime
    salary: float
    worker_id: int
    user_id: int


class VacancyListResponseSchema(SQLModel):
    items: List[VacancyResponseSchema]


class VacancyCreateSchema(SQLModel):
    title: str = Field(max_length=64)
    description: str = Field(max_length=1000)
    created_at: datetime
    salary: float
    worker_id: int
    user_id: int


class VacancyUpdateSchema(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
    description: Optional[str] = Field(default=None, max_length=1000)
    created_at: Optional[datetime] = Field(default=None)
    salary: Optional[float] = Field(default=None)
    worker_id: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None)
