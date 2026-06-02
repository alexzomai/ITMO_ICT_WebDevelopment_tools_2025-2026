from pydantic import BaseModel, HttpUrl


class ParseRequest(BaseModel):
    url: HttpUrl


class ParseResult(BaseModel):
    url: HttpUrl
    title: str
    description: str


class TaskStatusResponse(BaseModel):
    task_id: str
    status: str
    result: dict | None = None
