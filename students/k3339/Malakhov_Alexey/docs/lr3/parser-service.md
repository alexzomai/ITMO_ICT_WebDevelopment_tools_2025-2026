# Парсер-сервис

Парсер из ЛР2 переведён из CLI-скрипта в самостоятельное FastAPI-приложение. Слушает порт **8001**, отдаёт один полезный эндпоинт `POST /parse`.

## Модули

```
parser/parser_service/
├── __init__.py
├── main.py          # FastAPI app + эндпоинт
└── parser.py        # aiohttp-загрузка + BeautifulSoup-парсинг
```

## `parser.py`

Унаследовано из `Lr2/task_2/utils.py`: тот же BeautifulSoup, та же логика выбора первого осмысленного абзаца. Отличие — функция теперь сразу делает HTTP-запрос:

```python
async def fetch_and_parse(url: str) -> tuple[str, str]:
    async with aiohttp.ClientSession() as http:
        async with http.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
            resp.raise_for_status()
            html = await resp.text()
    return extract_title_description(html)
```

## `main.py`

```python
class ParseRequest(BaseModel):
    url: HttpUrl

class ParseResponse(BaseModel):
    url: HttpUrl
    title: str
    description: str

@app.post("/parse", response_model=ParseResponse)
async def parse(payload: ParseRequest) -> ParseResponse:
    try:
        title, description = await fetch_and_parse(str(payload.url))
    except aiohttp.ClientResponseError as exc:
        raise HTTPException(status_code=502, detail=f"Upstream returned {exc.status}")
    except aiohttp.ClientError as exc:
        raise HTTPException(status_code=502, detail=f"Fetch failed: {exc}")
    return ParseResponse(url=payload.url, title=title, description=description)
```

Сервис чистый, без БД и без побочных эффектов: даёшь URL → возвращает `{url, title, description}`. Записывает в БД уже основное приложение.

## Пример

```bash
curl -X POST http://localhost:8001/parse \
  -H "content-type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Redis"}'
```

```json
{
  "url": "https://en.wikipedia.org/wiki/Redis",
  "title": "Redis",
  "description": "Redis (/ˈrɛdɪs/; Remote Dictionary Server) is an in-memory key–value database..."
}
```
