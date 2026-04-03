from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from enums import NotificationType
from tasks.models import Task


class NotificationCreate(SQLModel):
    task_id: int = Field(foreign_key="task.id")
    type: NotificationType = Field(default=NotificationType.deadline_reminder)
    notify_at: datetime


class Notification(NotificationCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_sent: bool = Field(default=False)

    task: Optional[Task] = Relationship(back_populates="notifications")


class NotificationRead(NotificationCreate):
    id: int
    is_sent: bool
