import os
from datetime import datetime, timedelta

import httpx
from sqlmodel import Session, create_engine, select

import categories.models  # noqa: F401
import notifications.models  # noqa: F401
import schedules.models  # noqa: F401
import tags.models  # noqa: F401
import tasks.history_models  # noqa: F401
import tasks.task_tag_models  # noqa: F401
from celery_app import celery
from enums import PriorityType, StatusType
from tasks.models import Task

_engine = create_engine(os.getenv("DB_URL", ""))

PARSER_URL = os.getenv("PARSER_URL", "http://parser:8001")
PARSER_TIMEOUT = float(os.getenv("PARSER_TIMEOUT", "30"))


@celery.task(bind=True)
def parse_and_save(self, url: str) -> dict:
    with httpx.Client(timeout=PARSER_TIMEOUT) as client:
        resp = client.post(f"{PARSER_URL}/parse", json={"url": url})
        resp.raise_for_status()

    data = resp.json()
    title = data["title"] if data["title"] != "Unknown" else url
    description = data["description"]

    with Session(_engine) as session:
        existing = session.exec(select(Task).where(Task.title == title)).first()
        if existing:
            return {"id": existing.id, "title": existing.title}

        task = Task(
            title=title,
            description=description,
            status=StatusType.to_do,
            priority=PriorityType.medium,
            deadline=datetime.utcnow() + timedelta(days=7),
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return {"id": task.id, "title": task.title}
