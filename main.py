import csv
from pathlib import Path

from bench import KINDS, make_input, measure
from sorts import SORTS
from sorts.quick_sort import quick_sort
from sorts.tree_sort import tree_sort

RESULTS = Path(__file__).resolve().parent / "results"
FIELDS = ["algo", "input", "n", "millis", "compares", "moves", "height"]

VARIANTS = [
    ("merge", SORTS["merge"], {}),
    ("quick", SORTS["quick"], {}),
    ("quick_first", quick_sort, {"pivot": "first"}),
    ("tree", SORTS["tree"], {}),
]


def run(algo, sort, options, kind, n, reps):
    data = make_input(kind, n)
    row = {"algo": algo, "input": kind, "n": n}
    row.update(measure(sort, data, reps, **options))
    print(f"  {algo:12} {kind:14} n={n:<7} {row['millis']:10.2f} ms  "
          f"compares={row['compares']:<10} moves={row['moves']:<10} height={row['height']}")
    return row


def save(name, rows):
    RESULTS.mkdir(exist_ok=True)
    path = RESULTS / name
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(rows)
    print(f"-> {path.relative_to(RESULTS.parent)}\n")


def experiment_shapes():
    print("[1] input shapes (n = 2000)")
    rows = []
    for kind in KINDS:
        for algo, sort, options in VARIANTS:
            rows.append(run(algo, sort, options, kind, 2000, reps=5))
    save("shapes.csv", rows)


def experiment_growth():
    print("[2] growth (random input)")
    rows = []
    for n in (1000, 3000, 10000, 30000, 100000):
        for algo, sort, options in VARIANTS:
            if algo == "quick_first":
                continue
            rows.append(run(algo, sort, options, "random", n, reps=3))
    save("growth.csv", rows)


def experiment_tree_vs_quick():
    print("[3] tree sort vs quick sort with first pivot")
    rows = []
    for kind in ("random", "sorted"):
        for n in (500, 1000, 2000, 4000):
            rows.append(run("tree", tree_sort, {}, kind, n, reps=1))
            rows.append(run("quick_first", quick_sort, {"pivot": "first"}, kind, n, reps=1))
    save("tree_vs_quick.csv", rows)


if __name__ == "__main__":
    experiment_shapes()
    experiment_growth()
    experiment_tree_vs_quick()
