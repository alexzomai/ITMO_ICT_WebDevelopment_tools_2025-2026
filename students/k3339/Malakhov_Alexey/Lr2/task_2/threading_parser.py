"""Параллельный парсинг веб-страниц с использованием threading."""
import os
import sys
import threading
import time

import requests
from sqlmodel import Session

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db import engine
from utils import parse_wikipedia, save_to_db

URLS = [
    "https://en.wikipedia.org/wiki/Python_(programming_language)",
    "https://en.wikipedia.org/wiki/PostgreSQL",
    "https://en.wikipedia.org/wiki/Docker_(software)",
    "https://en.wikipedia.org/wiki/JavaScript",
    "https://en.wikipedia.org/wiki/Representational_state_transfer",
    "https://en.wikipedia.org/wiki/JSON",
    "https://en.wikipedia.org/wiki/HTML",
    "https://en.wikipedia.org/wiki/CSS",
]

_db_lock = threading.Lock()


def parse_and_save(url: str) -> None:
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
    resp.raise_for_status()

    title, description = parse_wikipedia(resp.text)

    with _db_lock:
        with Session(engine) as session:
            inserted = save_to_db(session, title, description)

    status = "saved" if inserted else "skipped (duplicate)"
    print(f"[threading] {status}: {title}")


def run(urls: list[str] = URLS) -> float:
    threads = [threading.Thread(target=parse_and_save, args=(url,)) for url in urls]

    start = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - start

    return elapsed


if __name__ == "__main__":
    elapsed = run()
    print(f"\n[threading] total time: {elapsed:.3f}s")
