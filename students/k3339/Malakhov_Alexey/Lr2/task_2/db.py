import os

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlmodel import Session, SQLModel, create_engine

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.db")

# Синхронный движок — для threading и multiprocessing
SYNC_URL = f"sqlite:///{DB_PATH}"
engine = create_engine(SYNC_URL, echo=False, connect_args={"check_same_thread": False})

# Асинхронный движок — для async-парсера
ASYNC_URL = f"sqlite+aiosqlite:///{DB_PATH}"
async_engine = create_async_engine(ASYNC_URL, echo=False)
AsyncSessionLocal: async_sessionmaker[AsyncSession] = async_sessionmaker(
    async_engine, expire_on_commit=False
)


def init_db() -> None:
    """Создаёт таблицы через синхронный движок (вызывается один раз перед запуском парсеров)."""
    SQLModel.metadata.create_all(engine)


def make_engine():
    """Создаёт новый движок для дочерних процессов (нельзя делиться пулом соединений)."""
    return create_engine(SYNC_URL, echo=False, connect_args={"check_same_thread": False})
