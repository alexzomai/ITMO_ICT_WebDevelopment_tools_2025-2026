# Эндпоинты

## Tasks `/tasks`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/tasks/` | Список задач |
| GET | `/tasks/{id}` | Задача по ID |
| POST | `/tasks/` | Создание задачи |
| PATCH | `/tasks/{id}` | Обновление задачи |
| DELETE | `/tasks/{id}` | Удаление задачи |

## Tags `/tags`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/tags/` | Список тегов |
| GET | `/tags/{id}` | Тег по ID |
| POST | `/tags/` | Создание тега |
| PATCH | `/tags/{id}` | Обновление тега |
| DELETE | `/tags/{id}` | Удаление тега |

## Categories `/categories`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/categories/` | Список категорий |
| GET | `/categories/{id}` | Категория по ID |
| POST | `/categories/` | Создание категории |
| PATCH | `/categories/{id}` | Обновление категории |
| DELETE | `/categories/{id}` | Удаление категории |

## Notifications `/notifications`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/notifications/` | Список уведомлений |
| GET | `/notifications/{id}` | Уведомление по ID |
| POST | `/notifications/` | Создание уведомления |
| PATCH | `/notifications/{id}` | Обновление уведомления |
| DELETE | `/notifications/{id}` | Удаление уведомления |

## Schedules `/schedules`

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/schedules/` | Список расписаний |
| GET | `/schedules/{id}` | Расписание по ID |
| POST | `/schedules/` | Создание расписания |
| PATCH | `/schedules/{id}` | Обновление расписания |
| DELETE | `/schedules/{id}` | Удаление расписания |

## Users `/users`

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/users/register` | Регистрация |
| GET | `/users/` | Список пользователей |
| GET | `/users/me` | Профиль текущего пользователя |
| PATCH | `/users/me/password` | Смена пароля |

## Auth `/auth`

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/auth/token` | Получение JWT-токена |
