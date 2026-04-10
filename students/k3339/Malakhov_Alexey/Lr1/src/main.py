from contextlib import asynccontextmanager

from fastapi import FastAPI

import categories.models  # noqa: F401
import notifications.models  # noqa: F401
import schedules.models  # noqa: F401
import tags.models  # noqa: F401
import tasks.history_models  # noqa: F401
import tasks.models  # noqa: F401
import tasks.task_tag_models  # noqa: F401
import users.models  # noqa: F401
from categories.router import router as categories_router
from db import init_db
from notifications.router import router as notifications_router
from schedules.router import router as schedules_router
from tags.router import router as tags_router
from tasks.router import router as tasks_router
from auth.router import router as auth_router
from users.router import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router)
app.include_router(tags_router)
app.include_router(categories_router)
app.include_router(notifications_router)
app.include_router(schedules_router)
app.include_router(users_router)
app.include_router(auth_router)


@app.get("/")
def hello() -> str:
    return "Hello, [username]!"
