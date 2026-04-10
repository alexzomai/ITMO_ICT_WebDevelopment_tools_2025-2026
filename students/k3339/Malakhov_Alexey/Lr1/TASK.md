# Лабораторная работа 1. Реализация серверного приложения FastAPI

## Тема: Разработка программы-тайм-менеджера

---

## Задание на 9 баллов

- [x] Таблицы через ORM SQLModel + PostgreSQL
- [x] CRUD для всех сущностей
- [x] GET-запросы с вложенными объектами (many-to-many, one-to-many)
- [x] Миграции через Alembic
- [x] Аннотация типов в API-методах
- [x] Файловая структура по модулям

### Критерии модели данных

- [x] 5+ таблиц (task, tag, category, schedule, notification, tasktag, taskstatushistory)
- [x] Связи many-to-many (Task ↔ Tag через TaskTag)
- [x] Связи one-to-many (Category → Task, Task → Notification, Task → Schedule)
- [x] Ассоциативная сущность с доп. полем (TaskTag.added_at)

---

## Задание на 15 баллов

- [x] Модель User (users/models.py)
- [x] Миграция для User
- [x] Регистрация (POST /users/register)
- [x] Авторизация (POST /auth/token) — возвращает JWT
- [x] Генерация и валидация JWT-токенов (вручную, без сторонних библиотек авторизации)
- [x] Аутентификация по JWT (dependency get_current_user)
- [x] Хэширование паролей (passlib/bcrypt)
- [ ] GET /users/me — профиль текущего пользователя
- [ ] GET /users — список пользователей
- [ ] PATCH /users/me/password — смена пароля

---

## Практики

- [x] Практика 1.1 — базовое FastAPI приложение (practice/Pr1)
- [x] Практика 1.2 — SQLModel, ORM, CRUD (practice/Pr2)
- [x] Практика 1.3 — Alembic, .env, .gitignore (practice/Pr3)

---

## Отчет

Предоставляется в формате GitHub Pages. Должен содержать:
- все реализованные эндпоинты
- модели
- код соединения с БД
- ссылки на папки/коммиты/ветки практик
