from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from auth.models import TokenRequest, TokenResponse
from db.connection import get_session
from security import create_token, verify_password
from users.models import User

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def login(credentials: TokenRequest, session: AsyncSession = Depends(get_session)):
    db_user = (await session.exec(select(User).where(User.email == credentials.email))).first()
    if not db_user or not verify_password(credentials.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Email or password is incorrect")
    return TokenResponse(access_token=create_token({"sub": str(db_user.id)}))
