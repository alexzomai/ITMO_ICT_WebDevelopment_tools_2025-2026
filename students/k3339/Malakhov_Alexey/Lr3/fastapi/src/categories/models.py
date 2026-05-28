from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from tasks.models import Task


class CategoryCreate(SQLModel):
    title: str
    color: Optional[str] = Field(default=None, max_length=7)


class CategoryUpdate(SQLModel):
    title: Optional[str] = None
    color: Optional[str] = None


class Category(CategoryCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="category")


class CategoryRead(CategoryCreate):
    id: int
