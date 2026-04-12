#!/usr/bin/env python3
import argparse
import csv
from collections import defaultdict
from pathlib import Path

import matplotlib.pyplot as plt


def parse_bool(value: str) -> bool:
    return value.strip().lower() == "true"


def parse_float(value: str | float | int | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, (float, int)):
        return float(value)
    value = value.strip()
    if value.upper() == "N/A":
        return None
    return float(value)


def normalize_algo(value: str) -> str:
    value = value.strip()
    if value == "WEIGHTED-ASTAR":
        return "WEIGHTED_ASTAR"
    return value


def load_rows(csv_path: Path) -> list[dict[str, str]]:
    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["algo"] = normalize_algo(row["algo"])
    return rows


def filter_success(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    filtered = []
    for row in rows:
        if parse_bool(row["timeout"]):
            continue
        if parse_float(row["time(s)"]) is None:
            continue
        filtered.append(row)
    return filtered


def mean_by(
    rows: list[dict[str, str]], keys: tuple[str, ...], value_key: str
) -> dict[tuple[str, ...], float]:
    totals: dict[tuple[str, ...], float] = defaultdict(float)
    counts: dict[tuple[str, ...], int] = defaultdict(int)
    for row in rows:
        values = tuple(row[key] for key in keys)
        value = row[value_key]
        if value is None:
            continue
        totals[values] += value
        counts[values] += 1
    return {key: totals[key] / counts[key] for key in totals}


def group_sizes(rows: list[dict[str, str]]) -> list[str]:
    sizes = sorted({row["size"] for row in rows}, key=lambda value: int(value))
    return sizes


def algo_order(rows: list[dict[str, str]]) -> list[str]:
    preferred = ["BFS", "DFS", "IDS", "GREEDY", "ASTAR", "WEIGHTED_ASTAR"]
    present = {row["algo"] for row in rows}
    ordered = [algo for algo in preferred if algo in present]
    ordered.extend(sorted(present - set(ordered)))
    return ordered


def plot_runtime_by_algo(rows: list[dict[str, str]], out_dir: Path) -> None:
    rows = filter_success(rows)
    sizes = group_sizes(rows)
    algos = algo_order(rows)
    for row in rows:
        row["time(s)"] = parse_float(row["time(s)"])
    means = mean_by(rows, ("size", "algo"), "time(s)")

    fig, axes = plt.subplots(1, len(sizes), figsize=(4 * len(sizes), 4), sharey=True)
    if len(sizes) == 1:
        axes = [axes]

    for ax, size in zip(axes, sizes):
        values = [means.get((size, algo)) for algo in algos]
        labels = [algo for algo, value in zip(algos, values) if value is not None]
        plotted = [value for value in values if value is not None]
        ax.plot(labels, plotted, marker="o")
        ax.set_title(f"Size {size}")
        ax.set_yscale("log")
        ax.set_ylabel("Mean runtime (s)")
        ax.tick_params(axis="x", rotation=45)

    fig.suptitle("Mean runtime by algorithm (log scale)")
    fig.tight_layout()
    fig.savefig(out_dir / "runtime_by_algo.png", dpi=160)
    plt.close(fig)


def plot_informed_by_heuristic(rows: list[dict[str, str]], out_dir: Path) -> None:
    rows = filter_success(rows)
    informed_algos = {"GREEDY", "ASTAR", "WEIGHTED_ASTAR"}
    rows = [
        row
        for row in rows
        if row["algo"] in informed_algos and row["heuristic"].upper() != "N/A"
    ]
    sizes = group_sizes(rows)

    for row in rows:
        row["time(s)"] = parse_float(row["time(s)"])

    means = mean_by(rows, ("size", "algo", "heuristic"), "time(s)")

    fig, axes = plt.subplots(1, len(sizes), figsize=(4 * len(sizes), 4), sharey=True)
    if len(sizes) == 1:
        axes = [axes]

    for ax, size in zip(axes, sizes):
        entries = [
            (algo, heuristic, value)
            for (s, algo, heuristic), value in means.items()
            if s == size
        ]
        entries.sort(key=lambda item: (item[0], item[1]))
        labels = [f"{algo}:{heuristic}" for algo, heuristic, _ in entries]
        plotted = [value for _, _, value in entries]
        ax.plot(labels, plotted, marker="o")
        ax.set_title(f"Size {size}")
        ax.set_yscale("log")
        ax.set_ylabel("Mean runtime (s)")
        ax.tick_params(axis="x", rotation=45)

    fig.suptitle("Mean runtime for informed search (log scale)")
    fig.tight_layout()
    fig.savefig(out_dir / "informed_runtime_by_heuristic.png", dpi=160)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plot algorithm performance summaries."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "data" / "performance.csv",
        help="Path to performance CSV",
    )
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path(__file__).resolve().parent,
        help="Directory to save plots",
    )
    args = parser.parse_args()

    rows = load_rows(args.input)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    plot_runtime_by_algo(rows, args.out_dir)
    plot_informed_by_heuristic(rows, args.out_dir)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
