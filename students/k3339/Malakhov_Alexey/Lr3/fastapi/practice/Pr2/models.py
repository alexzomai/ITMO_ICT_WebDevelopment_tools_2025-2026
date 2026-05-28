from datetime import datetime, timezone
from enum import Enum
from typing import List, Optional

from sqlmodel import Field, Relationship, SQLModel


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


class NotificationType(str, Enum):
    deadline_reminder = "deadline_reminder"
    overdue = "overdue"


class RecurrenceType(str, Enum):
    daily = "daily"
    weekly = "weekly"


# --- Tag ---

class TagDefault(SQLModel):
    name: str


class Tag(TagDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    task_tags: List["TaskTag"] = Relationship(back_populates="tag")


# --- Category ---

class CategoryDefault(SQLModel):
    title: str
    color: Optional[str] = Field(default=None, max_length=7)


class Category(CategoryDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="category")


# --- Task ---

class TaskDefault(SQLModel):
    title: str
    description: str
    status: StatusType = Field(default=StatusType.to_do)
    deadline: datetime
    priority: PriorityType = Field(default=PriorityType.medium)
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")


class Task(TaskDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    category: Optional[Category] = Relationship(back_populates="tasks")
    status_history: List["TaskStatusHistory"] = Relationship(back_populates="task")
    notifications: List["Notification"] = Relationship(back_populates="task")
    schedules: List["Schedule"] = Relationship(back_populates="task")
    task_tags: List["TaskTag"] = Relationship(back_populates="task")


# --- TaskTag ---

class TaskTagDefault(SQLModel):
    task_id: int = Field(foreign_key="task.id")
    tag_id: int = Field(foreign_key="tag.id")


class TaskTag(TaskTagDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    task: Optional[Task] = Relationship(back_populates="task_tags")
    tag: Optional[Tag] = Relationship(back_populates="task_tags")


# --- TaskStatusHistory (без Base — создаётся внутренне) ---

class TaskStatusHistory(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id")
    status: StatusType
    changed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    task: Optional[Task] = Relationship(back_populates="status_history")


# --- Notification ---

class NotificationDefault(SQLModel):
    task_id: int = Field(foreign_key="task.id")
    type: NotificationType = Field(default=NotificationType.deadline_reminder)
    notify_at: datetime


class Notification(NotificationDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_sent: bool = Field(default=False)

    task: Optional[Task] = Relationship(back_populates="notifications")


# --- Schedule ---

class ScheduleDefault(SQLModel):
    task_id: int = Field(foreign_key="task.id")
    recurrence: RecurrenceType
    next_run_at: datetime


class Schedule(ScheduleDefault, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)

    task: Optional[Task] = Relationship(back_populates="schedules")
