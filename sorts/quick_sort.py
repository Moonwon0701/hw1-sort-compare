import random


def quick_sort(arr, pivot="median3", seed=0):
    stats = {"compares": 0, "moves": 0}
    rng = random.Random(seed)

    def less(a, b):
        stats["compares"] += 1
        return a < b

    def swap(i, j):
        arr[i], arr[j] = arr[j], arr[i]
        stats["moves"] += 2

    def median_of_three(lo, mid, hi):
        if less(arr[mid], arr[lo]):
            swap(lo, mid)
        if less(arr[hi], arr[mid]):
            swap(mid, hi)
            if less(arr[mid], arr[lo]):
                swap(lo, mid)
        return mid

    def choose_pivot(lo, hi):
        if pivot == "first":
            return lo
        if pivot == "random":
            return rng.randint(lo, hi)
        return median_of_three(lo, (lo + hi) // 2, hi)

    def partition(lo, hi):
        p = choose_pivot(lo, hi)
        if p != lo:
            swap(lo, p)
        pv = arr[lo]
        i, j = lo, hi + 1
        while True:
            i += 1
            while i <= hi and less(arr[i], pv):
                i += 1
            j -= 1
            while less(pv, arr[j]):
                j -= 1
            if i >= j:
                break
            swap(i, j)
        if j != lo:
            swap(lo, j)
        return j

    def sort_range(lo, hi):
        while lo < hi:
            p = partition(lo, hi)
            if p - lo < hi - p:
                sort_range(lo, p - 1)
                lo = p + 1
            else:
                sort_range(p + 1, hi)
                hi = p - 1

    sort_range(0, len(arr) - 1)
    return stats
