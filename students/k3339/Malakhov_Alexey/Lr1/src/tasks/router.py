from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db.connection import get_session
from tags.models import Tag
from tasks.models import Task
from tasks.models import TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskRead])
def tasks_list(session: Session = Depends(get_session)) -> List[TaskRead]:
    return session.exec(select(Task)).all()


@router.get("/{task_id}", response_model=TaskRead)
def task_by_id(task_id: int, session: Session = Depends(get_session)) -> TaskRead:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.post("/", status_code=201, response_model=TaskRead)
def task_create(task: TaskCreate, session: Session = Depends(get_session)) -> TaskRead:
    db_task = Task.model_validate(task)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=204)
def task_delete(task_id: int, session: Session = Depends(get_session)) -> None:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(db_task)
    session.commit()


@router.patch("/{task_id}", response_model=TaskRead)
def task_update(task_id: int, task: TaskUpdate, session: Session = Depends(get_session)) -> TaskRead:
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    tag_ids = task_data.pop("tag_ids", None)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    if tag_ids is not None:
        db_task.tags = list(session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all())  # pyright: ignore
    db_task.updated_at = datetime.now(timezone.utc)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
