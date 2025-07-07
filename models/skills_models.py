from datetime import datetime
from typing import Optional, List

from sqlalchemy import Column, VARCHAR, DateTime
from sqlmodel import SQLModel, Field, Relationship

from learning_resources_models import LearningResource


class Skill(SQLModel, table=True):
    __tablename__ = "skills"

    id: Optional[int] = Field(primary_key=True)
    name: str = Field(sa_column=Column(VARCHAR(32), unique=True, nullable=False))
    description: Optional[str] = Field(sa_column=Column(VARCHAR(255)))
    category: Optional[str] = Field(sa_column=Column(VARCHAR(32)))
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    learning_resources: List["LearningResource"] = Relationship(back_populates="skill")
