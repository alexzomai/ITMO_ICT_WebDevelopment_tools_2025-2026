import aiohttp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl

from parser_service.parser import fetch_and_parse

app = FastAPI(title="Wikipedia Parser Service")


class ParseRequest(BaseModel):
    url: HttpUrl


class ParseResponse(BaseModel):
    url: HttpUrl
    title: str
    description: str


@app.get("/")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/parse", response_model=ParseResponse)
async def parse(payload: ParseRequest) -> ParseResponse:
    try:
        title, description = await fetch_and_parse(str(payload.url))
    except aiohttp.ClientResponseError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream returned {exc.status}")
    except aiohttp.ClientError as exc:
        raise HTTPException(status_code=502, detail=f"Fetch failed: {exc}")

    return ParseResponse(url=payload.url, title=title, description=description)
