from datetime import datetime, timezone
from typing import List

from connection import get_session, init_db
from fastapi import Depends, FastAPI, HTTPException
from models import Tag, TagCreate, TagRead, Task, TaskCreate, TaskRead, TaskUpdate
from sqlmodel import select

app: FastAPI = FastAPI()


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def hello() -> str:
    return "Hello, [username]!"


@app.get("/tasks_list", response_model=List[TaskRead])
def tasks_list(session=Depends(get_session)):
    return session.exec(select(Task)).all()


@app.get("/task/{task_id}", response_model=TaskRead)
def task_by_id(task_id: int, session=Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.post("/task", status_code=201)
def task_create(task: TaskCreate, session=Depends(get_session)) -> Task:
    task = Task.model_validate(task)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@app.delete("/task/{task_id}", status_code=204)
def task_delete(task_id: int, session=Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    session.delete(db_task)
    session.commit()


@app.patch("/task/{task_id}", response_model=TaskRead)
def task_update(task_id: int, task: TaskUpdate, session=Depends(get_session)):
    db_task = session.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    task_data = task.model_dump(exclude_unset=True)
    tag_ids = task_data.pop("tag_ids", None)
    for key, value in task_data.items():
        setattr(db_task, key, value)
    if tag_ids is not None:
        tags = session.exec(select(Tag).where(Tag.id.in_(tag_ids))).all()  # type: ignore
        db_task.tags = tags
    db_task.updated_at = datetime.now(timezone.utc)
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task


@app.get("/tags_list", response_model=List[TagRead])
def tags_list(session=Depends(get_session)):
    return session.exec(select(Tag)).all()


@app.get("/tag/{tag_id}", response_model=TagRead)
def tag_get(tag_id: int, session=Depends(get_session)):
    return session.get(Tag, tag_id)


@app.post("/tag", status_code=201)
def tag_create(tag: TagCreate, session=Depends(get_session)) -> Tag:
    tag = Tag.model_validate(tag)
    session.add(tag)
    session.commit()
    session.refresh(tag)
    return tag
