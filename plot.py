import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager

RESULTS = Path(__file__).resolve().parent / "results"

COLORS = {
    "merge": "#2a78d6",
    "quick": "#eb6834",
    "tree": "#1baf7a",
    "quick_first": "#eda100",
}
LABELS = {
    "merge": "병합 정렬",
    "quick": "퀵 정렬 (중앙값 피벗)",
    "tree": "트리 정렬",
    "quick_first": "퀵 정렬 (맨 앞 피벗)",
}
KIND_LABELS = {
    "random": "무작위",
    "sorted": "정렬됨",
    "reversed": "역순",
    "nearly_sorted": "거의 정렬",
    "few_unique": "중복 많음",
}

INSTALLED_FONTS = {f.name for f in font_manager.fontManager.ttflist}
KOREAN_FONT = next((f for f in ("Malgun Gothic", "AppleGothic", "NanumGothic") if f in INSTALLED_FONTS), "sans-serif")
plt.rcParams["font.family"] = KOREAN_FONT
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.color"] = "#e4e3df"
plt.rcParams["axes.axisbelow"] = True


def load(name):
    with open(RESULTS / name, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["n"] = int(r["n"])
        r["millis"] = float(r["millis"])
        r["compares"] = int(r["compares"])
        r["moves"] = int(r["moves"])
    return rows


def pick(rows, **cond):
    return [r for r in rows if all(r[k] == v for k, v in cond.items())]


def save(fig, name):
    fig.tight_layout()
    fig.savefig(RESULTS / name, dpi=150)
    plt.close(fig)
    print(f"-> results/{name}")


def plot_shapes():
    rows = load("shapes.csv")
    kinds = list(KIND_LABELS)
    algos = ["merge", "quick", "tree", "quick_first"]
    width = 0.2
    fig, ax = plt.subplots(figsize=(10, 5))
    for i, algo in enumerate(algos):
        xs = [k + (i - 1.5) * width for k in range(len(kinds))]
        ys = [pick(rows, algo=algo, input=kind)[0]["millis"] for kind in kinds]
        bars = ax.bar(xs, ys, width * 0.9, color=COLORS[algo], label=LABELS[algo])
        ax.bar_label(bars, labels=[f"{y:.3g}" for y in ys], fontsize=7, padding=2)
    ax.set_yscale("log")
    ax.set_xticks(range(len(kinds)), [KIND_LABELS[k] for k in kinds])
    ax.set_ylabel("시간 (ms, 로그 축)")
    ax.set_title("입력 모양에 따른 정렬 시간 (n = 2,000)")
    ax.legend(frameon=False, ncols=2)
    save(fig, "shapes_time.png")


def plot_growth_time():
    rows = load("growth.csv")
    fig, ax = plt.subplots(figsize=(8, 5))
    for algo in ["merge", "quick", "tree"]:
        rs = pick(rows, algo=algo)
        ax.plot([r["n"] for r in rs], [r["millis"] for r in rs], marker="o",
                color=COLORS[algo], label=LABELS[algo], linewidth=2)
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("n (원소 개수, 로그 축)")
    ax.set_ylabel("시간 (ms, 로그 축)")
    ax.set_title("n이 커질 때 정렬 시간 (무작위 입력)")
    ax.legend(frameon=False)
    save(fig, "growth_time.png")


def plot_growth_counts():
    rows = load("growth.csv")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), sharex=True)
    for ax, field, title in ((axes[0], "compares", "비교 횟수"), (axes[1], "moves", "이동(쓰기) 횟수")):
        for algo in ["merge", "quick", "tree"]:
            rs = pick(rows, algo=algo)
            ax.plot([r["n"] for r in rs], [r[field] for r in rs], marker="o",
                    color=COLORS[algo], label=LABELS[algo], linewidth=2)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("n (원소 개수, 로그 축)")
        ax.set_ylabel(f"{title} (로그 축)")
        ax.set_title(f"{title} (무작위 입력)")
        ax.legend(frameon=False)
    save(fig, "growth_counts.png")


def plot_tree_vs_quick():
    rows = load("tree_vs_quick.csv")
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    for ax, kind in zip(axes, ["sorted", "random"]):
        for algo, style in (("tree", "-"), ("quick_first", "--")):
            rs = pick(rows, algo=algo, input=kind)
            ax.plot([r["n"] for r in rs], [r["compares"] for r in rs], marker="o", linestyle=style,
                    color=COLORS[algo], label=LABELS[algo], linewidth=2)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel("n (원소 개수, 로그 축)")
        ax.set_ylabel("비교 횟수 (로그 축)")
        ax.set_title(f"트리 정렬 vs 맨 앞 피벗 퀵 정렬 — {KIND_LABELS[kind]} 입력")
        ax.legend(frameon=False)
    save(fig, "tree_vs_quick.png")


if __name__ == "__main__":
    plot_shapes()
    plot_growth_time()
    plot_growth_counts()
    plot_tree_vs_quick()
