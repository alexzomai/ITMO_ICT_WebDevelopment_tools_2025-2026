# Эндпоинт `/parse` в основном API

Новый модуль `fastapi/src/parsing/router.py` экспонирует два эндпоинта:

| Метод | Путь | Назначение |
|-------|------|------------|
| POST | `/parse/` | Проксирует запрос парсер-сервису, возвращает результат клиенту |
| POST | `/parse/task` | То же + сохраняет результат как новый `Task` в Postgres |

Адрес парсера читается из `PARSER_URL` (в docker-compose задано `http://parser:8001`). HTTP-клиент — `httpx.AsyncClient` (идёт в комплекте `fastapi[all]`).

## Код

```python
PARSER_URL = os.getenv("PARSER_URL", "http://parser:8001")
PARSER_TIMEOUT = float(os.getenv("PARSER_TIMEOUT", "30"))

@router.post("/", response_model=ParseResult)
async def parse_url(payload: ParseRequest) -> ParseResult:
    async with httpx.AsyncClient(timeout=PARSER_TIMEOUT) as client:
        try:
            resp = await client.post(f"{PARSER_URL}/parse", json={"url": str(payload.url)})
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=502, detail=f"Parser unreachable: {exc}")

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code,
                            detail=resp.json().get("detail", resp.text))
    return ParseResult(**resp.json())


@router.post("/task", status_code=201, response_model=TaskRead)
async def parse_url_into_task(
    payload: ParseRequest,
    session: Session = Depends(get_session),
) -> TaskRead:
    # ... тот же вызов парсера ...
    title, description = data["title"], data["description"]

    existing = session.exec(select(Task).where(Task.title == title)).first()
    if existing:
        return existing

    db_task = Task(
        title=title,
        description=description,
        status=StatusType.to_do,
        priority=PriorityType.medium,
        deadline=datetime.now(timezone.utc) + timedelta(days=7),
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task
```

Регистрация в `main.py`:

```python
from parsing.router import router as parsing_router
...
app.include_router(parsing_router)
```

## Пример вызова

```bash
# просто распарсить
curl -X POST http://localhost:8000/parse/ \
  -H "content-type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/Kubernetes"}'

# распарсить и создать Task
curl -X POST http://localhost:8000/parse/task \
  -H "content-type: application/json" \
  -d '{"url":"https://en.wikipedia.org/wiki/SQLite"}'
```

Ответ `/parse/task`:

```json
{
  "id": 1,
  "title": "SQLite",
  "description": "...",
  "status": "to_do",
  "priority": "medium",
  "deadline": "2026-05-29T15:22:48.424911",
  "category": null,
  "tags": []
}
```

## Что важно

- Запрос блокирующе ждёт ответа парсера (нет очереди — это будет в подзадаче 3 с Celery).
- Дедупликация по `title`: если статья с таким же заголовком уже есть, повторно не создаётся, возвращается старая.
- Все 5xx от парсера маппятся в `502 Bad Gateway` на стороне API — клиенту понятно, что отказ внешний.
