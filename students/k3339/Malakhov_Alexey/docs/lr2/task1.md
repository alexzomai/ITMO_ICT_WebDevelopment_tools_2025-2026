# Задание 1 — Сумма чисел от 1 до 1 000 000

Задача: вычислить сумму чисел от 1 до 1 000 000, разбив диапазон на 4 части и запустив вычисления параллельно.

## threading

Четыре потока, каждый считает свою часть диапазона через `sum(range(...))`. Результаты пишутся в общий список `results` по индексу — без блокировок, т.к. каждый поток пишет в свою ячейку.

```python
def calculate_sum(start: int, end: int, results: list, index: int) -> None:
    results[index] = sum(range(start, end + 1))

def run() -> int:
    threads = [threading.Thread(target=calculate_sum, args=(start, end, results, i))
               for i in range(NUM_THREADS)]
    for t in threads: t.start()
    for t in threads: t.join()
    return sum(results)
```

**Особенность:** GIL не снимается на чистых вычислениях в Python, поэтому потоки выполняются поочерёдно, а не параллельно.

## multiprocessing

Каждый процесс получает диапазон, считает сумму и кладёт результат в `Queue`.

```python
def calculate_sum(start: int, end: int, queue: multiprocessing.Queue) -> None:
    queue.put(sum(range(start, end + 1)))
```

**Особенность:** Процессы обходят GIL и работают по-настоящему параллельно, но запуск каждого процесса и передача данных через IPC создают накладные расходы.

## async

Четыре корутины запускаются через `asyncio.gather`. Каждая уступает управление через `await asyncio.sleep(0)` и затем считает свою часть.

```python
async def calculate_sum(start: int, end: int) -> int:
    await asyncio.sleep(0)
    return sum(range(start, end + 1))
```

**Особенность:** Однопоточный event loop — реального параллелизма нет. Корутины переключаются кооперативно, поэтому накладных расходов минимум.

## Результаты

| Подход | Результат | Время (с) | Корректно |
|--------|-----------|-----------|-----------|
| threading | 500 000 500 000 | 0.0082 | да |
| multiprocessing | 500 000 500 000 | 0.0653 | да |
| async | 500 000 500 000 | 0.0078 | да |

## Вывод

Для CPU-bound задач все три подхода дают одинаковый результат, но разную производительность:

- **async** и **threading** показывают схожее время — оба однопоточны на уровне CPython из-за GIL.
- **multiprocessing** медленнее из-за накладных расходов на `spawn` процессов — при такой короткой задаче старт процессов дороже самих вычислений.
- На задачах с бо́льшим объёмом вычислений multiprocessing выиграет, так как использует все ядра процессора.
