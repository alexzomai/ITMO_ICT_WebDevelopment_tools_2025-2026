from datetime import datetime, timezone
from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from categories.models import Category, CategoryRead
from enums import PriorityType, StatusType
from tags.models import TagRead
from tasks.task_tag_models import TaskTag

if TYPE_CHECKING:
    from notifications.models import Notification
    from schedules.models import Schedule
    from tags.models import Tag
    from tasks.history_models import TaskStatusHistory


class TaskCreate(SQLModel):
    title: str
    description: str
    status: StatusType = Field(default=StatusType.to_do)
    deadline: datetime
    priority: PriorityType = Field(default=PriorityType.medium)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[StatusType] = None
    deadline: Optional[datetime] = None
    priority: Optional[PriorityType] = None
    category_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class Task(TaskCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    category: Optional[Category] = Relationship(back_populates="tasks")
    status_history: List["TaskStatusHistory"] = Relationship(back_populates="task")
    notifications: List["Notification"] = Relationship(back_populates="task")
    schedules: List["Schedule"] = Relationship(back_populates="task")
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)


class TaskRead(TaskCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryRead] = None
    tags: List[TagRead] = []
