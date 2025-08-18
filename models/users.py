from sqlalchemy import Column, VARCHAR
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(primary_key=True)
    first_name: str = Field(sa_column=Column(VARCHAR(32), nullable=False))
    last_name: str = Field(sa_column=Column(VARCHAR(32), nullable=False))
    email: str = Field(unique=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    vacancies: List["Vacancy"] = Relationship(back_populates="user", cascade_delete=True)
