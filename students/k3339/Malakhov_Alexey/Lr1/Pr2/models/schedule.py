from datetime import datetime
from typing import Optional

from sqlmodel import Field, Relationship, SQLModel

from .enums import RecurrenceType
from .task import Task


class ScheduleCreate(SQLModel):
    task_id: int = Field(foreign_key="task.id")
    recurrence: RecurrenceType
    next_run_at: datetime


class Schedule(ScheduleCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    is_active: bool = Field(default=True)

    task: Optional[Task] = Relationship(back_populates="schedules")


class ScheduleRead(ScheduleCreate):
    id: int
    is_active: bool
