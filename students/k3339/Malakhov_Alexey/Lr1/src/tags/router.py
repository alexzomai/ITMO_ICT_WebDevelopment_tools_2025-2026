from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.connection import get_session
from tags.models import Tag, TagCreate, TagRead, TagUpdate

router = APIRouter(prefix="/tags", tags=["tags"])


@router.get("/", response_model=List[TagRead])
async def tags_list(session: AsyncSession = Depends(get_session)) -> List[TagRead]:
    return (await session.exec(select(Tag))).all()


@router.get("/{tag_id}", response_model=TagRead)
async def tag_get(tag_id: int, session: AsyncSession = Depends(get_session)) -> TagRead:
    db_tag = await session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag


@router.post("/", status_code=201, response_model=TagRead)
async def tag_create(tag: TagCreate, session: AsyncSession = Depends(get_session)) -> TagRead:
    db_tag = Tag.model_validate(tag)
    session.add(db_tag)
    await session.commit()
    await session.refresh(db_tag)
    return db_tag


@router.patch("/{tag_id}", response_model=TagRead)
async def tag_update(tag_id: int, tag: TagUpdate, session: AsyncSession = Depends(get_session)) -> TagRead:
    db_tag = await session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    for key, value in tag.model_dump(exclude_unset=True).items():
        setattr(db_tag, key, value)
    session.add(db_tag)
    await session.commit()
    await session.refresh(db_tag)
    return db_tag


@router.delete("/{tag_id}", status_code=204)
async def tag_delete(tag_id: int, session: AsyncSession = Depends(get_session)) -> None:
    db_tag = await session.get(Tag, tag_id)
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    await session.delete(db_tag)
    await session.commit()
