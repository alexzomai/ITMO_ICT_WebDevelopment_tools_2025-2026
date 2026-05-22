# Задание 2 — Параллельный парсинг Wikipedia

Задача: параллельно загрузить 8 статей Wikipedia, распарсить заголовок и первый абзац, сохранить в SQLite через SQLModel.

## Архитектура

### Модель (`models.py`)

```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    description: str
    status: StatusType = Field(default=StatusType.to_do)
    priority: PriorityType = Field(default=PriorityType.medium)
    deadline: datetime
    category_id: Optional[int] = Field(default=None, foreign_key="category.id")
```

### Подключение к БД (`db.py`)

Два движка к одному файлу `tasks.db`:

```python
# Синхронный — для threading и multiprocessing
engine = create_engine("sqlite:///tasks.db", connect_args={"check_same_thread": False})

# Асинхронный — для async-парсера
async_engine = create_async_engine("sqlite+aiosqlite:///tasks.db")
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False)
```

### Парсинг (`utils.py`)

```python
def parse_wikipedia(html: str) -> tuple[str, str]:
    soup = BeautifulSoup(html, "html.parser")
    for sup in soup.find_all("sup"):
        sup.decompose()                          # убираем [1], [2]
    title = soup.find("h1", id="firstHeading").get_text(strip=True)
    for p in soup.select("#mw-content-text .mw-parser-output > p"):
        if len(p.get_text(strip=True)) > 80:
            return title, p.get_text(strip=True)[:500]
    return title, "No description available."
```

## threading

8 потоков, один на URL. Все HTTP-запросы идут параллельно (GIL снимается на IO). Запись в БД сериализована через `threading.Lock()`.

```python
_db_lock = threading.Lock()

def parse_and_save(url: str) -> None:
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    title, description = parse_wikipedia(resp.text)
    with _db_lock:
        with Session(engine) as session:
            save_to_db(session, title, description)
```

## multiprocessing

8 процессов. Каждый создаёт собственный движок SQLAlchemy — пул соединений нельзя делить между процессами.

```python
def parse_and_save(url: str) -> None:
    local_engine = make_engine()
    try:
        resp = requests.get(url, ...)
        title, description = parse_wikipedia(resp.text)
        with Session(local_engine) as session:
            save_to_db(session, title, description)
    finally:
        local_engine.dispose()
```

## async

`aiohttp` для асинхронных HTTP-запросов, `AsyncSession` + `aiosqlite` для асинхронной записи в БД. Всё в одном event loop.

```python
async def parse_and_save(http: aiohttp.ClientSession, url: str) -> None:
    async with http.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
        html = await resp.text()
    title, description = parse_wikipedia(html)
    async with _db_lock:
        async with AsyncSessionLocal() as db_session:
            await save_to_db_async(db_session, title, description)

async def _run_all(urls):
    async with aiohttp.ClientSession() as http:
        await asyncio.gather(*(parse_and_save(http, url) for url in urls))
```

**`asyncio.Lock`** нужен потому что SQLite физически допускает только одного писателя одновременно.

## Результаты

| Подход | Время (с) |
|--------|-----------|
| async | 0.947 |
| threading | 1.092 |
| multiprocessing | 1.285 |

## Вывод

Парсинг — IO-bound задача (время уходит на ожидание ответа от Wikipedia):

- **async** быстрее всего: один event loop, `aiohttp` отправляет все запросы одновременно, минимум накладных расходов.
- **threading** немного медленнее: GIL снимается на IO, поэтому реальная параллельность есть, но есть накладные расходы на создание потоков и блокировки.
- **multiprocessing** медленнее всех: запуск 8 процессов и создание 8 движков SQLAlchemy — значительный старт для задачи длительностью ~0.1–0.2 с каждая. Оправдан только для CPU-bound задач или при очень длительном IO.
