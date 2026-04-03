from contextlib import asynccontextmanager

from fastapi import FastAPI

import categories.models  # noqa: F401
import notifications.models  # noqa: F401
import schedules.models  # noqa: F401
import tags.models  # noqa: F401
import tasks.history_models  # noqa: F401
import tasks.models  # noqa: F401
import tasks.task_tag_models  # noqa: F401
from db import init_db
from tags.router import router as tags_router
from tasks.router import router as tasks_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(tasks_router)
app.include_router(tags_router)


@app.get("/")
def hello() -> str:
    return "Hello, [username]!"
