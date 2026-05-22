# Подключение к БД и миграции

## Подключение (`db/connection.py`)

```python
import os
from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

load_dotenv()

db_url = os.getenv("DB_URL", "")
engine = create_engine(db_url, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

## Миграции (Alembic)

Конфигурация миграций — `migrations/env.py`. Все модели импортируются для автогенерации:

```python
import categories.models
import notifications.models
import schedules.models
import tags.models
import tasks.history_models
import tasks.models
import tasks.task_tag_models
import users.models

target_metadata = SQLModel.metadata
```

Команды:

```bash
uv run alembic revision --autogenerate -m "описание"
uv run alembic upgrade head
```
