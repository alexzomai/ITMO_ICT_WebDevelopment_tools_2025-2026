from datetime import datetime, timezone
from typing import Optional

from sqlmodel import Field, SQLModel


class TaskTagCreate(SQLModel):
    task_id: int = Field(foreign_key="task.id")
    tag_id: int = Field(foreign_key="tag.id")


class TaskTag(TaskTagCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class TaskTagRead(TaskTagCreate):
    id: int
    added_at: datetime
