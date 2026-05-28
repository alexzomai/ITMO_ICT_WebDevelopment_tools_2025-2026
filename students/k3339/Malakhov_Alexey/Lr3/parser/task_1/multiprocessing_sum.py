import multiprocessing
import time

TOTAL = 1_000_000
NUM_PROCESSES = 4


def calculate_sum(start: int, end: int, queue: multiprocessing.Queue) -> None:
    queue.put(sum(range(start, end + 1)))


def run() -> int:
    chunk = TOTAL // NUM_PROCESSES
    queue: multiprocessing.Queue = multiprocessing.Queue()
    processes: list[multiprocessing.Process] = []

    for i in range(NUM_PROCESSES):
        start = i * chunk + 1
        end = (i + 1) * chunk if i < NUM_PROCESSES - 1 else TOTAL
        p = multiprocessing.Process(target=calculate_sum, args=(start, end, queue))
        processes.append(p)

    for p in processes:
        p.start()
    for p in processes:
        p.join()

    return sum(queue.get() for _ in range(NUM_PROCESSES))


if __name__ == "__main__":
    start_time = time.perf_counter()
    total = run()
    elapsed = time.perf_counter() - start_time
    print(f"[multiprocessing] result={total}, time={elapsed:.4f}s")
