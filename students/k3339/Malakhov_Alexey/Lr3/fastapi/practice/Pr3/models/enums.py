from enum import Enum


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
