from fastapi_users import schemas
from typing import Optional, List
from sqlmodel import SQLModel, Field
from services import VacancyResponseSchema, VacancyUpdateSchema


class UserRead(schemas.BaseUser[int]):
    first_name: str
    last_name: str


class UserCreate(schemas.BaseUserCreate):
    first_name: str
    last_name: str


class UserUpdate(schemas.BaseUserUpdate):
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserResponseSchema(SQLModel):
    id: int
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    vacancies: List[VacancyResponseSchema]


class UserCreateSchema(SQLModel):
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    vacancies: List[VacancyResponseSchema]


class UserUpdateSchema(SQLModel):
    first_name: str = Field(max_length=32)
    last_name: str = Field(max_length=32)
    email: str
    hashed_password: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    vacancies: List[VacancyUpdateSchema]
