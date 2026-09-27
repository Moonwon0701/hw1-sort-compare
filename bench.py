import random
import statistics
import time

KINDS = ["random", "sorted", "reversed", "nearly_sorted", "few_unique"]


def make_input(kind, n, seed=20260927):
    rng = random.Random(seed)
    if kind == "random":
        return [rng.randrange(n * 10) for _ in range(n)]
    if kind == "sorted":
        return list(range(n))
    if kind == "reversed":
        return list(range(n, 0, -1))
    if kind == "nearly_sorted":
        data = list(range(n))
        for _ in range(max(1, n // 100)):
            i, j = rng.randrange(n), rng.randrange(n)
            data[i], data[j] = data[j], data[i]
        return data
    if kind == "few_unique":
        return [rng.randrange(8) for _ in range(n)]
    raise ValueError(kind)


def measure(sort, data, reps=3, **options):
    expected = sorted(data)
    times = []
    stats = {}
    for _ in range(reps):
        arr = data[:]
        start = time.perf_counter()
        stats = sort(arr, **options)
        times.append((time.perf_counter() - start) * 1000)
        if arr != expected:
            raise AssertionError(f"{sort.__name__} failed to sort")
    return {
        "millis": statistics.median(times),
        "compares": stats.get("compares", 0),
        "moves": stats.get("moves", 0),
        "height": stats.get("height", ""),
    }
