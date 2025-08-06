from sqlmodel import SQLModel, Field
from typing import Optional


class VacancyFilter(SQLModel):
    title: Optional[str] = Field(default=None, max_length=64)
