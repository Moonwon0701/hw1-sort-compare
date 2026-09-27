def tree_sort(arr):
    stats = {"compares": 0, "moves": 0, "height": 0}
    n = len(arr)
    if n == 0:
        return stats

    vals = arr[:]
    left = [-1] * n
    right = [-1] * n
    height = 1

    for i in range(1, n):
        cur = 0
        depth = 1
        while True:
            stats["compares"] += 1
            if vals[i] < vals[cur]:
                if left[cur] == -1:
                    left[cur] = i
                    break
                cur = left[cur]
            else:
                if right[cur] == -1:
                    right[cur] = i
                    break
                cur = right[cur]
            depth += 1
        height = max(height, depth + 1)

    stack = []
    node = 0
    k = 0
    while stack or node != -1:
        while node != -1:
            stack.append(node)
            node = left[node]
        node = stack.pop()
        arr[k] = vals[node]
        stats["moves"] += 1
        k += 1
        node = right[node]

    stats["height"] = height
    return stats
