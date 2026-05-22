# Модели

## Enums

```python
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
```

## Task

```python
class Task(TaskCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    category: Optional[Category] = Relationship(back_populates="tasks")
    status_history: List["TaskStatusHistory"] = Relationship(back_populates="task")
    notifications: List["Notification"] = Relationship(back_populates="task")
    schedules: List["Schedule"] = Relationship(back_populates="task")
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model=TaskTag)
```

## TaskTag (ассоциативная сущность)

```python
class TaskTag(TaskTagCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    added_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```
