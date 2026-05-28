from datetime import datetime, timezone
from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class StatusType(str, Enum):
    to_do = "to_do"
    in_progress = "in_progress"
    paused = "paused"
    done = "done"
    archived = "archived"


class PriorityType(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"


class Category(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    color: Optional[str] = Field(default=None, max_length=7)


class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: StatusType = Field(default=StatusType.to_do)
    deadline: datetime
    priority: PriorityType = Field(default=PriorityType.medium)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
