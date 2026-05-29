from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.connection import get_session
from security import hash_password, verify_password
from users.dependencies import get_current_user
from users.models import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/register", status_code=201, response_model=UserRead)
async def register(user: UserCreate, session: AsyncSession = Depends(get_session)) -> UserRead:
    if (await session.exec(select(User).where(User.email == user.email))).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    db_user = User(username=user.username, email=user.email, password_hash=hash_password(user.password))
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user


@router.get("/", response_model=List[UserRead])
async def users_list(session: AsyncSession = Depends(get_session)):
    return (await session.exec(select(User))).all()


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    return current_user


@router.patch("/me/password", response_model=UserRead)
async def change_password(
    user: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    if not verify_password(user.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.password_hash = hash_password(user.new_password)
    session.add(current_user)
    await session.commit()
    await session.refresh(current_user)
    return current_user
