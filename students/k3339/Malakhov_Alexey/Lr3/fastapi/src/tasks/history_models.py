from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from enums import StatusType

if TYPE_CHECKING:
    from tasks.models import Task


class TaskStatusHistoryCreate(SQLModel):
    task_id: int = Field(foreign_key="task.id")
    status: StatusType


class TaskStatusHistory(TaskStatusHistoryCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    changed_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    task: Optional["Task"] = Relationship(back_populates="status_history")


class TaskStatusHistoryRead(TaskStatusHistoryCreate):
    id: int
    changed_at: datetime
