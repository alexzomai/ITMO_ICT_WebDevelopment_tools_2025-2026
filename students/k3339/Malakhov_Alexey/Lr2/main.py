import asyncio
import multiprocessing
import threading
import time

TOTAL = 1_000_000
NUM_WORKERS = 4

# ── threading ─────────────────────────────────────────────────────────────────

def _thread_worker(start: int, end: int, results: list, index: int) -> None:
    results[index] = sum(range(start, end + 1))


def calculate_sum_threading() -> tuple[int, float]:
    chunk = TOTAL // NUM_WORKERS
    results: list[int] = [0] * NUM_WORKERS
    threads: list[threading.Thread] = []

    for i in range(NUM_WORKERS):
        start = i * chunk + 1
        end = (i + 1) * chunk if i < NUM_WORKERS - 1 else TOTAL
        threads.append(threading.Thread(target=_thread_worker, args=(start, end, results, i)))

    t0 = time.perf_counter()
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.perf_counter() - t0

    return sum(results), elapsed


# ── multiprocessing ───────────────────────────────────────────────────────────

def _process_worker(start: int, end: int, queue: multiprocessing.Queue) -> None:
    queue.put(sum(range(start, end + 1)))


def calculate_sum_multiprocessing() -> tuple[int, float]:
    chunk = TOTAL // NUM_WORKERS
    queue: multiprocessing.Queue = multiprocessing.Queue()
    processes: list[multiprocessing.Process] = []

    for i in range(NUM_WORKERS):
        start = i * chunk + 1
        end = (i + 1) * chunk if i < NUM_WORKERS - 1 else TOTAL
        processes.append(multiprocessing.Process(target=_process_worker, args=(start, end, queue)))

    t0 = time.perf_counter()
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    elapsed = time.perf_counter() - t0

    return sum(queue.get() for _ in range(NUM_WORKERS)), elapsed


# ── async ─────────────────────────────────────────────────────────────────────

async def _async_worker(start: int, end: int) -> int:
    await asyncio.sleep(0)  # yield to event loop so tasks interleave
    return sum(range(start, end + 1))


async def _async_run() -> int:
    chunk = TOTAL // NUM_WORKERS
    tasks = []
    for i in range(NUM_WORKERS):
        start = i * chunk + 1
        end = (i + 1) * chunk if i < NUM_WORKERS - 1 else TOTAL
        tasks.append(asyncio.create_task(_async_worker(start, end)))
    return sum(await asyncio.gather(*tasks))


def calculate_sum_async() -> tuple[int, float]:
    t0 = time.perf_counter()
    result = asyncio.run(_async_run())
    elapsed = time.perf_counter() - t0
    return result, elapsed


# ── main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    expected = TOTAL * (TOTAL + 1) // 2  # 500_000_500_000

    print(f"Сумма чисел от 1 до {TOTAL:,} (ожидается: {expected:,})\n")
    print(f"{'Подход':<20} {'Результат':>15} {'Время (с)':>12} {'Верно?':>8}")
    print("-" * 60)

    for label, func in [
        ("threading",       calculate_sum_threading),
        ("multiprocessing", calculate_sum_multiprocessing),
        ("async",           calculate_sum_async),
    ]:
        result, elapsed = func()
        ok = "да" if result == expected else "НЕТ"
        print(f"{label:<20} {result:>15,} {elapsed:>11.4f}s {ok:>8}")


if __name__ == "__main__":
    multiprocessing.freeze_support()  # needed on Windows/macOS with spawn
    main()
