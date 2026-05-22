# Лабораторная работа 2. Параллелизм в Python

**Студент:** Малахов Алексей, группа K3339  
**Срок сдачи:** 12 мая 2026

## Цель

Изучить и сравнить три подхода к параллельному выполнению задач в Python:

| Подход | Модуль | Параллелизм |
|--------|--------|-------------|
| threading | `threading` | Потоки, GIL ограничивает CPU |
| multiprocessing | `multiprocessing` | Процессы, истинный параллелизм |
| async | `asyncio` + `aiohttp` | Кооперативная многозадачность |

## Структура проекта

```
Lr2/
├── main.py                    # Задание 1: сравнение суммы чисел
├── threading_sum.py
├── multiprocessing_sum.py
├── async_sum.py
└── task_2/
    ├── models.py              # SQLModel: Task
    ├── db.py                  # Синхронный + async движки SQLite
    ├── utils.py               # Парсинг Wikipedia + сохранение в БД
    ├── threading_parser.py
    ├── multiprocessing_parser.py
    ├── async_parser.py
    └── main.py                # Запуск всех трёх и сравнение
```

## Зависимости

```toml
dependencies = [
    "aiohttp>=3.9",
    "aiosqlite>=0.22",
    "beautifulsoup4>=4.12",
    "requests>=2.31",
    "sqlmodel>=0.0.21",
    "sqlalchemy[asyncio]",
]
```
