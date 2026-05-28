import os
from datetime import datetime, timedelta, timezone

import httpx
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, HttpUrl
from sqlmodel import Session, select

from db.connection import get_session
from enums import PriorityType, StatusType
from tasks.models import Task, TaskRead

router = APIRouter(prefix="/parse", tags=["parser"])

PARSER_URL = os.getenv("PARSER_URL", "http://parser:8001")
PARSER_TIMEOUT = float(os.getenv("PARSER_TIMEOUT", "30"))


class ParseRequest(BaseModel):
    url: HttpUrl


class ParseResult(BaseModel):
    url: HttpUrl
    title: str
    description: str


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
    session: Session = Depends(get_session),
) -> TaskRead:
    async with httpx.AsyncClient(timeout=PARSER_TIMEOUT) as client:
        try:
            resp = await client.post(f"{PARSER_URL}/parse", json={"url": str(payload.url)})
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Parser unreachable: {exc}")

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.json().get("detail", resp.text))

    data = resp.json()
    title = data["title"]
    description = data["description"]

    existing = session.exec(select(Task).where(Task.title == title)).first()
    if existing:
        return existing

    db_task = Task(
        title=title,
        description=description,
        status=StatusType.to_do,
        priority=PriorityType.medium,
        deadline=datetime.now(timezone.utc) + timedelta(days=7),
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
