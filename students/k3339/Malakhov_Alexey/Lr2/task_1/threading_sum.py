import threading
import time

TOTAL = 1_000_000
NUM_THREADS = 4


def calculate_sum(start: int, end: int, results: list, index: int) -> None:
    results[index] = sum(range(start, end + 1))


def run() -> int:
    chunk = TOTAL // NUM_THREADS
    threads: list[threading.Thread] = []
    results: list[int] = [0] * NUM_THREADS

    for i in range(NUM_THREADS):
        start = i * chunk + 1
        end = (i + 1) * chunk if i < NUM_THREADS - 1 else TOTAL
        t = threading.Thread(target=calculate_sum, args=(start, end, results, i))
        threads.append(t)

    for t in threads:
        t.start()
    for t in threads:
        t.join()

    return sum(results)


if __name__ == "__main__":
    start_time = time.perf_counter()
    total = run()
    elapsed = time.perf_counter() - start_time
    print(f"[threading]       result={total}, time={elapsed:.4f}s")
