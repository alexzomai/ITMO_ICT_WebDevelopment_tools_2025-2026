from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db.connection import get_session
from security import hash_password
from users.dependencies import get_current_user
from users.models import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


# Регистрация нового пользователя.
# Хэширует пароль и сохраняет пользователя в БД.
@router.post("/register", status_code=201, response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)) -> UserRead:
    db_check_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_check_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = hash_password(user.password)

    db_user = User(
        username=user.username,
        email=user.email,
        password_hash=password_hash,
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# Возвращает список всех пользователей.
@router.get("/", response_model=List[UserRead])
def users_list(session: Session = Depends(get_session)):
    pass


# Возвращает профиль текущего авторизованного пользователя.
# Требует валидный JWT-токен.
@router.get("/me", response_model=UserRead)
def get_me(current_user: User = Depends(get_current_user)) -> UserRead:
    pass


# Смена пароля текущего авторизованного пользователя.
# Проверяет текущий пароль и устанавливает новый.
@router.patch("/me/password", response_model=UserRead)
def change_password(user: UserUpdate, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)) -> UserRead:
    pass
