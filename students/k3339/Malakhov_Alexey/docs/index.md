# Лабораторная работа 1. Тайм-менеджер на FastAPI

**Студент:** Малахов Алексей, группа K3339  
**Тема:** Разработка программы-тайм-менеджера  
**Стек:** Python 3.10+, FastAPI, SQLModel, PostgreSQL, Alembic, PyJWT, bcrypt

## Структура проекта

```
Lr1/src/
├── main.py
├── enums.py
├── security.py
├── db/
│   ├── __init__.py
│   └── connection.py
├── tasks/
│   ├── models.py
│   ├── router.py
│   ├── task_tag_models.py
│   └── history_models.py
├── tags/
│   ├── models.py
│   └── router.py
├── categories/
│   ├── models.py
│   └── router.py
├── notifications/
│   ├── models.py
│   └── router.py
├── schedules/
│   ├── models.py
│   └── router.py
├── users/
│   ├── models.py
│   ├── router.py
│   └── dependencies.py
├── auth/
│   ├── models.py
│   └── router.py
└── migrations/
    ├── env.py
    └── versions/
```

## Таблицы

| Таблица | Описание |
|---------|----------|
| `task` | Задачи |
| `tag` | Теги |
| `category` | Категории |
| `schedule` | Расписания |
| `notification` | Уведомления |
| `tasktag` | Связь задача–тег (many-to-many) |
| `taskstatushistory` | История статусов задач |
| `user` | Пользователи |

## Связи

- **Many-to-many:** `Task` ↔ `Tag` через `TaskTag` (доп. поле `added_at`)
- **One-to-many:** `Category` → `Task`, `Task` → `Notification`, `Task` → `Schedule`, `Task` → `TaskStatusHistory`
