"""Запускает все три парсера и сравнивает время их выполнения."""
import multiprocessing
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import async_parser
import multiprocessing_parser
import threading_parser
from db import init_db


def main() -> None:
    init_db()
    print("=" * 60)
    print("Параллельный парсинг Wikipedia → SQLite (tasks.db)")
    print("=" * 60)

    results: list[tuple[str, float]] = []

    print("\n── threading ──────────────────────────────────────────────")
    elapsed = threading_parser.run()
    results.append(("threading", elapsed))
    print(f"Время: {elapsed:.3f}s")

    print("\n── multiprocessing ────────────────────────────────────────")
    elapsed = multiprocessing_parser.run()
    results.append(("multiprocessing", elapsed))
    print(f"Время: {elapsed:.3f}s")

    print("\n── async ──────────────────────────────────────────────────")
    elapsed = async_parser.run()
    results.append(("async", elapsed))
    print(f"Время: {elapsed:.3f}s")

    print("\n── Итоги ──────────────────────────────────────────────────")
    print(f"{'Подход':<20} {'Время (с)':>10}")
    print("-" * 32)
    for name, t in sorted(results, key=lambda x: x[1]):
        print(f"{name:<20} {t:>10.3f}s")

    fastest = min(results, key=lambda x: x[1])
    print(f"\nБыстрее всего: {fastest[0]} ({fastest[1]:.3f}s)")


if __name__ == "__main__":
    multiprocessing.freeze_support()
    main()
