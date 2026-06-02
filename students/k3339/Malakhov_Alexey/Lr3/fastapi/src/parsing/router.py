import os
from datetime import datetime, timedelta, timezone

import httpx
from celery.result import AsyncResult
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from celery_app import celery
from db.connection import get_session
from enums import PriorityType, StatusType
from parsing.models import ParseRequest, ParseResult, TaskStatusResponse
from parsing.tasks import parse_and_save
from tasks.models import Task, TaskRead

router = APIRouter(prefix="/parse", tags=["parser"])

PARSER_URL = os.getenv("PARSER_URL", "http://parser:8001")
PARSER_TIMEOUT = float(os.getenv("PARSER_TIMEOUT", "30"))

_TASK_OPTIONS = [selectinload(Task.category), selectinload(Task.tags)]  # type: ignore


@router.post("/", response_model=ParseResult)
async def parse_url(payload: ParseRequest) -> ParseResult:
    async with httpx.AsyncClient(timeout=PARSER_TIMEOUT) as client:
        try:
            resp = await client.post(f"{PARSER_URL}/parse", json={"url": str(payload.url)})
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Parser unreachable: {exc}")

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.json().get("detail", resp.text))
    return ParseResult(**resp.json())


@router.post("/task", status_code=201, response_model=TaskRead)
async def parse_url_into_task(
    payload: ParseRequest,
    session: AsyncSession = Depends(get_session),
) -> TaskRead:
    async with httpx.AsyncClient(timeout=PARSER_TIMEOUT) as client:
        try:
            resp = await client.post(f"{PARSER_URL}/parse", json={"url": str(payload.url)})
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Parser unreachable: {exc}")

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.json().get("detail", resp.text))

    data = resp.json()
    title = data["title"] if data["title"] != "Unknown" else str(payload.url)
    description = data["description"]

    existing = (await session.exec(select(Task).where(Task.title == title).options(*_TASK_OPTIONS))).first()
    if existing:
        return existing

    db_task = Task(
        title=title,
        description=description,
        status=StatusType.to_do,
        priority=PriorityType.medium,
        deadline=datetime.utcnow() + timedelta(days=7),
    )
    session.add(db_task)
    await session.commit()
    db_task = (await session.exec(select(Task).where(Task.id == db_task.id).options(*_TASK_OPTIONS))).first()
    return db_task  # type: ignore


@router.post("/task/async", status_code=202)
async def parse_url_into_task_async(payload: ParseRequest) -> dict:
    task = parse_and_save.delay(str(payload.url))
    return {"task_id": task.id}


@router.get("/task/status/{task_id}", response_model=TaskStatusResponse)
async def get_task_status(task_id: str) -> TaskStatusResponse:
    result = AsyncResult(task_id, app=celery)
    result_value = None
    if result.ready():
        result_value = result.result if result.successful() else {"error": str(result.result)}
    return TaskStatusResponse(task_id=task_id, status=result.status, result=result_value)
