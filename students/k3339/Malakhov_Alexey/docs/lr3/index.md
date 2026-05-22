# Лабораторная работа 3. Docker, парсер-сервис и интеграция с API

**Студент:** Малахов Алексей, группа K3339
**Срок сдачи:** 2 июня 2026

## Цель

Упаковать FastAPI-приложение из ЛР1, парсер из ЛР2 и базу данных в Docker, связать их через docker-compose и научить основное API дёргать парсер как отдельный сервис.

## Что сделано

- [x] Парсер обёрнут в отдельное FastAPI-приложение с эндпоинтом `POST /parse`.
- [x] Dockerfile для основного API (`fastapi/`) и для парсера (`parser/`).
- [x] `docker-compose.yml` в корне `Lr3/` оркестрирует три сервиса: `db`, `parser`, `api`.
- [x] В основном API добавлены эндпоинты `POST /parse/` (проксирует запрос парсеру) и `POST /parse/task` (парсит + сохраняет результат как `Task` в БД).

Celery + Redis (подзадача 3) — в работе, в этой версии не вошло.

## Структура

```
Lr3/
├── docker-compose.yml          # db + parser + api
├── fastapi/                    # код из ЛР1
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── uv.lock
│   └── src/
│       ├── main.py
│       ├── parsing/
│       │   └── router.py       # /parse и /parse/task
│       └── ...                 # tasks, tags, users, auth, ...
└── parser/                     # код из ЛР2
    ├── Dockerfile
    ├── pyproject.toml
    ├── uv.lock
    └── parser_service/
        ├── main.py             # FastAPI app
        └── parser.py           # aiohttp + BeautifulSoup
```

## Запуск

```bash
cd students/k3339/Malakhov_Alexey/Lr3
docker compose up -d --build
```

- API: <http://localhost:8000>
- Parser: <http://localhost:8001>
- Postgres: `localhost:5432`, БД `tasks_db`, пользователь `postgres` / пароль `123`
