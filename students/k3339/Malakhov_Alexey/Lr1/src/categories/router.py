from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from categories.models import Category, CategoryCreate, CategoryRead, CategoryUpdate
from db.connection import get_session

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryRead])
async def categories_list(session: AsyncSession = Depends(get_session)) -> List[CategoryRead]:
    return (await session.exec(select(Category))).all()


@router.get("/{category_id}", response_model=CategoryRead)
async def category_get(category_id: int, session: AsyncSession = Depends(get_session)) -> CategoryRead:
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.post("/", status_code=201, response_model=CategoryRead)
async def category_create(category: CategoryCreate, session: AsyncSession = Depends(get_session)) -> CategoryRead:
    db_category = Category.model_validate(category)
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category


@router.patch("/{category_id}", response_model=CategoryRead)
async def category_update(
    category_id: int, category: CategoryUpdate, session: AsyncSession = Depends(get_session)
) -> CategoryRead:
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    for key, value in category.model_dump(exclude_unset=True).items():
        setattr(db_category, key, value)
    session.add(db_category)
    await session.commit()
    await session.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=204)
async def category_delete(category_id: int, session: AsyncSession = Depends(get_session)) -> None:
    db_category = await session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    await session.delete(db_category)
    await session.commit()
