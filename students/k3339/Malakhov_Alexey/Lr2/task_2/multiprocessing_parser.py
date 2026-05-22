"""Параллельный парсинг веб-страниц с использованием multiprocessing."""
import multiprocessing
import os
import sys
import time

import requests
from sqlmodel import Session

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import make_engine
from utils import parse_wikipedia, save_to_db

URLS = [
    "https://en.wikipedia.org/wiki/Git",
    "https://en.wikipedia.org/wiki/Django_(web_framework)",
    "https://en.wikipedia.org/wiki/Nginx",
    "https://en.wikipedia.org/wiki/TypeScript",
    "https://en.wikipedia.org/wiki/MongoDB",
    "https://en.wikipedia.org/wiki/Elasticsearch",
    "https://en.wikipedia.org/wiki/RabbitMQ",
    "https://en.wikipedia.org/wiki/GraphQL",
]


def parse_and_save(url: str) -> None:
    # Каждый процесс создаёт свой движок — пул соединений SQLAlchemy нельзя передавать между процессами.
    local_engine = make_engine()

    try:
        resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        resp.raise_for_status()

        title, description = parse_wikipedia(resp.text)

        with Session(local_engine) as session:
            inserted = save_to_db(session, title, description)

        status = "saved" if inserted else "skipped (duplicate)"
        print(f"[multiprocessing] {status}: {title}")
    finally:
        local_engine.dispose()


def run(urls: list[str] = URLS) -> float:
    processes = [multiprocessing.Process(target=parse_and_save, args=(url,)) for url in urls]

    start = time.perf_counter()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    elapsed = time.perf_counter() - start

    return elapsed


if __name__ == "__main__":
    multiprocessing.freeze_support()
    elapsed = run()
    print(f"\n[multiprocessing] total time: {elapsed:.3f}s")
