# Docker и оркестрация

## Dockerfile для FastAPI-приложения

Базовый образ `python:3.12-slim`, зависимости ставятся через `uv` по `uv.lock` (воспроизводимая сборка). Миграции Alembic не запускаются на старте — первая миграция проекта написана как `ALTER TABLE`, а схема изначально создаётся через `SQLModel.metadata.create_all()` в `lifespan`-хуке `init_db()`.

```dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev curl \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY src ./src
WORKDIR /app/src

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Dockerfile для парсера

Минимальный, без системных пакетов — `aiohttp` и `beautifulsoup4` ставятся как чистые wheel'ы.

```dockerfile
FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    UV_LINK_MODE=copy \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH"

COPY --from=ghcr.io/astral-sh/uv:0.5.11 /uv /usr/local/bin/uv

WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY parser_service ./parser_service

EXPOSE 8001
CMD ["uvicorn", "parser_service.main:app", "--host", "0.0.0.0", "--port", "8001"]
```

## docker-compose.yml

Три сервиса в одной сети `lr3_default`:

```yaml
services:
  db:
    image: postgres:16
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: "123"
      POSTGRES_DB: tasks_db
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d tasks_db"]
      interval: 5s
      timeout: 5s
      retries: 10

  parser:
    build:
      context: ./parser
    ports:
      - "8001:8001"
    restart: unless-stopped

  api:
    build:
      context: ./fastapi
    environment:
      DB_URL: postgresql+psycopg2://postgres:123@db:5432/tasks_db
      SECRET_KEY: ${SECRET_KEY:-dev-secret-change-me}
      ALGORITHM: HS256
      PARSER_URL: http://parser:8001
    depends_on:
      db:
        condition: service_healthy
      parser:
        condition: service_started
    ports:
      - "8000:8000"
    restart: unless-stopped

volumes:
  postgres_data:
```

## Ключевые моменты

- **`depends_on: condition: service_healthy`** — `api` стартует только когда healthcheck Postgres проходит, иначе `init_db()` падает на подключении.
- **`PARSER_URL=http://parser:8001`** — docker-compose поднимает DNS внутри сети, поэтому `api` обращается к парсеру по имени сервиса.
- **Volume `postgres_data`** — данные БД переживают `docker compose down`. Удалить: `docker compose down -v`.
- **`.dockerignore`** в обоих сервисах исключает `.venv`, `__pycache__`, локальные `.db`-файлы и `task_1/`, `task_2/` из парсера — это код ЛР2, в сервис не попадает.
