from sqlmodel import SQLModel, Field
from typing import Optional


class WorkerFilter(SQLModel):
    name: Optional[str] = Field(default=None, max_length=20)
