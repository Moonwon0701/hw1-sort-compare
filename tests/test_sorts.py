import math
import random
import unittest

from sorts import SORTS, STABLE
from sorts.merge_sort import merge_sort
from sorts.quick_sort import quick_sort
from sorts.tree_sort import tree_sort


class Rec:
    def __init__(self, key, order):
        self.key = key
        self.order = order

    def __lt__(self, other):
        return self.key < other.key

    def __le__(self, other):
        return self.key <= other.key


class TestAllSorts(unittest.TestCase):
    SMALL_CASES = [
        [],
        [42],
        [1, 2, 3, 4, 5],
        [5, 4, 3, 2, 1],
        [3, 1, 3, 1, 2],
        [7, 7, 7, 7],
        [-3, 10, 0, -7, 5],
        [2.5, -1.0, 3.25, 0.0],
        [6, 8, 5, 9, 10, 1, 7, 2, 4, 3],
    ]

    def test_small_cases(self):
        for name, sort in SORTS.items():
            for case in self.SMALL_CASES:
                with self.subTest(sort=name, case=case):
                    arr = case[:]
                    sort(arr)
                    self.assertEqual(arr, sorted(case))

    def test_random_sizes(self):
        rng = random.Random(20260927)
        for name, sort in SORTS.items():
            for n in range(0, 301):
                data = [rng.randrange(20) for _ in range(n)]
                with self.subTest(sort=name, n=n):
                    arr = data[:]
                    sort(arr)
                    self.assertEqual(arr, sorted(data))

    def test_in_place_and_stats(self):
        for name, sort in SORTS.items():
            with self.subTest(sort=name):
                arr = [5, 1, 4, 2, 3]
                same = arr
                stats = sort(arr)
                self.assertIs(arr, same)
                self.assertEqual(arr, [1, 2, 3, 4, 5])
                self.assertIsInstance(stats, dict)
                self.assertIn("compares", stats)
                self.assertIn("moves", stats)
                self.assertGreater(stats["compares"], 0)

    def test_stability(self):
        rng = random.Random(7)
        for name in STABLE:
            sort = SORTS[name]
            with self.subTest(sort=name):
                recs = [Rec(rng.randrange(5), i) for i in range(300)]
                sort(recs)
                for a, b in zip(recs, recs[1:]):
                    self.assertLessEqual(a.key, b.key)
                    if a.key == b.key:
                        self.assertLess(a.order, b.order)


class TestMergeSort(unittest.TestCase):
    def test_compares_at_most_n_log_n(self):
        rng = random.Random(1)
        n = 1000
        arr = [rng.random() for _ in range(n)]
        stats = merge_sort(arr)
        self.assertLessEqual(stats["compares"], n * math.log2(n))


class TestQuickSort(unittest.TestCase):
    def test_all_pivot_rules_sort(self):
        rng = random.Random(2)
        inputs = {
            "random": [rng.randrange(1000) for _ in range(2000)],
            "sorted": list(range(2000)),
            "reversed": list(range(2000, 0, -1)),
            "few_unique": [rng.randrange(8) for _ in range(2000)],
        }
        for pivot in ("first", "median3", "random"):
            for shape, data in inputs.items():
                with self.subTest(pivot=pivot, shape=shape):
                    arr = data[:]
                    quick_sort(arr, pivot=pivot)
                    self.assertEqual(arr, sorted(data))

    def test_first_pivot_is_quadratic_on_sorted(self):
        n = 2000
        stats = quick_sort(list(range(n)), pivot="first")
        self.assertGreater(stats["compares"], n * n / 4)

    def test_median3_is_not_quadratic(self):
        n = 2000
        for shape, data in (("sorted", list(range(n))), ("reversed", list(range(n, 0, -1)))):
            with self.subTest(shape=shape):
                stats = quick_sort(data, pivot="median3")
                self.assertLess(stats["compares"], 20 * n)


class TestTreeSort(unittest.TestCase):
    def test_sorted_input_makes_a_chain(self):
        n = 1000
        stats = tree_sort(list(range(n)))
        self.assertEqual(stats["height"], n)
        self.assertEqual(stats["compares"], n * (n - 1) // 2)

    def test_random_input_is_shallow(self):
        rng = random.Random(3)
        n = 10000
        stats = tree_sort([rng.random() for _ in range(n)])
        self.assertLess(stats["height"], 60)


if __name__ == "__main__":
    unittest.main()
