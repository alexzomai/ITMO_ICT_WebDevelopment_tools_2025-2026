from datetime import datetime, timezone
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.connection import get_session
from tags.models import Tag
from tasks.models import Task, TaskCreate, TaskRead, TaskUpdate

router = APIRouter(prefix="/tasks", tags=["tasks"])

_TASK_OPTIONS = [selectinload(Task.category), selectinload(Task.tags)]  # type: ignore


@router.get("/", response_model=List[TaskRead])
async def tasks_list(session: AsyncSession = Depends(get_session)) -> List[TaskRead]:
    return (await session.exec(select(Task).options(*_TASK_OPTIONS))).all()


@router.get("/{task_id}", response_model=TaskRead)
async def task_by_id(task_id: int, session: AsyncSession = Depends(get_session)) -> TaskRead:
    db_task = await session.get(Task, task_id, options=_TASK_OPTIONS)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.post("/", status_code=201, response_model=TaskRead)
async def task_create(task: TaskCreate, session: AsyncSession = Depends(get_session)) -> TaskRead:
    db_task = Task.model_validate(task)
    session.add(db_task)
    await session.commit()
    db_task = await session.get(Task, db_task.id, options=_TASK_OPTIONS)
    return db_task  # type: ignore


@router.delete("/{task_id}", status_code=204)
async def task_delete(task_id: int, session: AsyncSession = Depends(get_session)) -> None:
    db_task = await session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    await session.delete(db_task)
    await session.commit()


@router.patch("/{task_id}", response_model=TaskRead)
async def task_update(task_id: int, task: TaskUpdate, session: AsyncSession = Depends(get_session)) -> TaskRead:
    db_task = await session.get(Task, task_id, options=_TASK_OPTIONS)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    tag_ids = task_data.pop("tag_ids", None)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    if tag_ids is not None:
        db_task.tags = list((await session.exec(select(Tag).where(Tag.id.in_(tag_ids)))).all())  # pyright: ignore
    db_task.updated_at = datetime.now(timezone.utc)
    session.add(db_task)
    await session.commit()
    db_task = await session.get(Task, db_task.id, options=_TASK_OPTIONS)
    return db_task  # type: ignore
