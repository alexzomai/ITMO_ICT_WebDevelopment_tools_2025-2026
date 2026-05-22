"""Параллельный парсинг веб-страниц с использованием asyncio + aiohttp и async SQLAlchemy (aiosqlite)."""
import asyncio
import os
import sys
import time

import aiohttp

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import AsyncSessionLocal
from utils import parse_wikipedia, save_to_db_async

URLS = [
    "https://en.wikipedia.org/wiki/Redis",
    "https://en.wikipedia.org/wiki/Kubernetes",
    "https://en.wikipedia.org/wiki/Linux",
    "https://en.wikipedia.org/wiki/Flask_(web_framework)",
    "https://en.wikipedia.org/wiki/Apache_Kafka",
    "https://en.wikipedia.org/wiki/SQLite",
    "https://en.wikipedia.org/wiki/Node.js",
    "https://en.wikipedia.org/wiki/React_(JavaScript_library)",
]

# Сериализуем запись в БД: HTTP-запросы параллельны, но SQLite допускает только одного писателя.
_db_lock = asyncio.Lock()


async def parse_and_save(http: aiohttp.ClientSession, url: str) -> None:
    async with http.get(url, headers={"User-Agent": "Mozilla/5.0"}) as resp:
        resp.raise_for_status()
        html = await resp.text()

    title, description = parse_wikipedia(html)

    async with _db_lock:
        async with AsyncSessionLocal() as db_session:
            inserted = await save_to_db_async(db_session, title, description)

    status = "saved" if inserted else "skipped (duplicate)"
    print(f"[async] {status}: {title}")


async def _run_all(urls: list[str]) -> None:
    async with aiohttp.ClientSession() as http:
        await asyncio.gather(*(parse_and_save(http, url) for url in urls))


def run(urls: list[str] = URLS) -> float:
    start = time.perf_counter()
    asyncio.run(_run_all(urls))
    return time.perf_counter() - start


if __name__ == "__main__":
    elapsed = run()
    print(f"\n[async] total time: {elapsed:.3f}s")
