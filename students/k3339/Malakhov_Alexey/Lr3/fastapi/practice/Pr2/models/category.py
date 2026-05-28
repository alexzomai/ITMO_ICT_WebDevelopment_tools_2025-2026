from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .task import Task


class CategoryCreate(SQLModel):
    title: str
    color: Optional[str] = Field(default=None, max_length=7)


class Category(CategoryCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="category")


class CategoryRead(CategoryCreate):
    id: int
