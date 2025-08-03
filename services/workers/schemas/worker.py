from datetime import date
from typing import List, Optional

from sqlmodel import SQLModel, Field


# this class uses only for get-requests
class WorkerResponseSchema(SQLModel):
    id: int
    name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    biography: str = Field(max_length=250)
    birth_date: date


class WorkerListResponseSchema(SQLModel):
    items: List[WorkerResponseSchema]


# the same as above but without an id and uses for post-requests

class WorkerCreateSchema(SQLModel):
    name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    biography: str = Field(max_length=250)
    birth_date: date


class WorkerUpdateSchema(SQLModel):
    name: Optional[str] = Field(max_length=20)
    last_name: Optional[str] = Field(max_length=20)
    biography: Optional[str] = Field(max_length=250)
    birth_date: Optional[date]
