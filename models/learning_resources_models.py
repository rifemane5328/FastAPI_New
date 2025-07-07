from datetime import datetime
from typing import Optional

from sqlalchemy import Column, VARCHAR, DateTime
from sqlmodel import SQLModel, Field, Relationship

from models.skills_models import Skill


class LearningResource(SQLModel, table=True):
    __tablename__ = "learning_resources"

    id: Optional[int] = Field(primary_key=True)
    title: str = Field(sa_column=Column(VARCHAR(32), nullable=False))
    description: Optional[str] = Field(sa_column=Column(VARCHAR(255)))
    link: str = Field(sa_column=Column(VARCHAR(255), nullable=False))
    created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    skill_id: int = Field(foreign_key="skills.id", nullable=False, ondelete="CASCADE")
    skill: Skill = Relationship(back_populates="learning_resources")
