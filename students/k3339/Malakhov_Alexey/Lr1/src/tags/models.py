from typing import TYPE_CHECKING, List, Optional

from sqlmodel import Field, Relationship, SQLModel

from tasks.task_tag_models import TaskTag

if TYPE_CHECKING:
    from tasks.models import Task


class TagCreate(SQLModel):
    name: str


class Tag(TagCreate, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tasks: List["Task"] = Relationship(back_populates="tags", link_model=TaskTag)


class TagRead(TagCreate):
    id: int
