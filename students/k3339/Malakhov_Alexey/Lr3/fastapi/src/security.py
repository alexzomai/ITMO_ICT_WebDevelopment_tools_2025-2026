import hashlib
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()


SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")


def hash_password(password: str) -> str:
    prehash = hashlib.sha256(password.encode("utf-8")).digest()  # чтобы обойти лимит bcrypt в 72 байта
    return bcrypt.hashpw(prehash, bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    prehash = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.checkpw(prehash, password_hash.encode("utf-8"))


def create_token(data: dict) -> str:
    payload = data.copy()
    payload["exp"] = datetime.now(timezone.utc) + timedelta(hours=24)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
