from typing import Optional

from pydantic import EmailStr
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    username: Optional[str] = None
    email: Optional[str] = None
    current_password: str
    new_password: str


class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: EmailStr = Field(unique=True)
    password_hash: str


class UserRead(UserBase):
    id: int
