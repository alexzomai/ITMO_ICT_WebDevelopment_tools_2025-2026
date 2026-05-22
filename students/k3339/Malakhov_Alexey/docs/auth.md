# Аутентификация

## Хэширование паролей (`security.py`)

SHA-256 prehash для обхода лимита bcrypt в 72 байта:

```python
def hash_password(password: str) -> str:
    prehash = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.hashpw(prehash, bcrypt.gensalt()).decode("utf-8")

def verify_password(password: str, password_hash: str) -> bool:
    prehash = hashlib.sha256(password.encode("utf-8")).digest()
    return bcrypt.checkpw(prehash, password_hash.encode("utf-8"))
```

## JWT-токены (`security.py`)

```python
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
```

## Dependency (`users/dependencies.py`)

```python
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session),
) -> User:
    payload = decode_token(token)
    user = session.get(User, int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    return user
```
