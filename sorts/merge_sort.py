def merge_sort(arr):
    stats = {"compares": 0, "moves": 0}
    buf = [None] * len(arr)

    def merge(lo, mid, hi):
        buf[lo:hi] = arr[lo:hi]
        i, j = lo, mid
        for k in range(lo, hi):
            if i >= mid:
                arr[k] = buf[j]
                j += 1
            elif j >= hi:
                arr[k] = buf[i]
                i += 1
            else:
                stats["compares"] += 1
                if buf[i] <= buf[j]:
                    arr[k] = buf[i]
                    i += 1
                else:
                    arr[k] = buf[j]
                    j += 1
            stats["moves"] += 1

    def sort_range(lo, hi):
        if hi - lo < 2:
            return
        mid = (lo + hi) // 2
        sort_range(lo, mid)
        sort_range(mid, hi)
        merge(lo, mid, hi)

    sort_range(0, len(arr))
    return stats
