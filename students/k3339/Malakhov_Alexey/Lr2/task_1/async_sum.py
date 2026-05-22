import asyncio
import time

TOTAL = 1_000_000
NUM_TASKS = 4


async def calculate_sum(start: int, end: int) -> int:
    # yield control to the event loop so tasks interleave
    await asyncio.sleep(0)
    return sum(range(start, end + 1))


async def run() -> int:
    chunk = TOTAL // NUM_TASKS
    tasks = []

    for i in range(NUM_TASKS):
        start = i * chunk + 1
        end = (i + 1) * chunk if i < NUM_TASKS - 1 else TOTAL
        tasks.append(asyncio.create_task(calculate_sum(start, end)))

    results = await asyncio.gather(*tasks)
    return sum(results)


if __name__ == "__main__":
    start_time = time.perf_counter()
    total = asyncio.run(run())
    elapsed = time.perf_counter() - start_time
    print(f"[async]           result={total}, time={elapsed:.4f}s")
