from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from categories.models import Category, CategoryCreate, CategoryRead, CategoryUpdate
from db.connection import get_session

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=List[CategoryRead])
def categories_list(session: Session = Depends(get_session)) -> List[CategoryRead]:
    return session.exec(select(Category)).all()


@router.get("/{category_id}", response_model=CategoryRead)
def category_get(category_id: int, session: Session = Depends(get_session)) -> CategoryRead:
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    return db_category


@router.post("/", status_code=201, response_model=CategoryRead)
def category_create(category: CategoryCreate, session: Session = Depends(get_session)) -> CategoryRead:
    db_category = Category.model_validate(category)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.patch("/{category_id}", response_model=CategoryRead)
def category_update(
    category_id: int, category: CategoryUpdate, session: Session = Depends(get_session)
) -> CategoryRead:
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    category_data = category.model_dump(exclude_unset=True)
    for key, value in category_data.items():
        setattr(db_category, key, value)
    session.add(db_category)
    session.commit()
    session.refresh(db_category)
    return db_category


@router.delete("/{category_id}", status_code=204)
def category_delete(category_id: int, session: Session = Depends(get_session)) -> None:
    db_category = session.get(Category, category_id)
    if not db_category:
        raise HTTPException(status_code=404, detail="Category not found")
    session.delete(db_category)
    session.commit()
