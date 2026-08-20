#!/usr/bin/env python3
"""
Regenerate the evidence table in README.md from methods.yaml.

    python render_table.py             # print the table to stdout
    python render_table.py --write     # rewrite the block between the markers
    python render_table.py --ladder    # strength ladder only, strongest first
    python render_table.py --min 3     # only methods at or above a strength

Address verification is an evidence problem. Sorting the methods by how strong
the proof is, rather than by how easy they are to run, is the whole point of
this dataset: the easiest methods sit at the bottom of the ladder.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

START = "<!-- TABLE:START -->"
END = "<!-- TABLE:END -->"

COLUMNS = [
    ("name", "Method"),
    ("_stars", "Strength"),
    ("proves", "What a pass proves"),
    ("fails", "How it fails"),
    ("basis", "Typical lawful basis"),
]

MAX_STRENGTH = 5


def stars(strength: int) -> str:
    filled = max(0, min(int(strength), MAX_STRENGTH))
    return f"{filled}/{MAX_STRENGTH}"


def cell(method: dict, key: str) -> str:
    if key == "_stars":
        return stars(method.get("strength", 0))
    return str(method.get(key, ""))


def build_table(methods: list[dict]) -> str:
    ordered = sorted(
        methods, key=lambda m: (-int(m.get("strength", 0)), m.get("name", ""))
    )
    header = "| " + " | ".join(label for _, label in COLUMNS) + " |"
    divider = "| " + " | ".join("---" for _ in COLUMNS) + " |"
    rows = [
        "| " + " | ".join(cell(m, key) for key, _ in COLUMNS) + " |" for m in ordered
    ]
    return "\n".join([header, divider, *rows])


def print_ladder(methods: list[dict]) -> None:
    ordered = sorted(methods, key=lambda m: -int(m.get("strength", 0)))
    print(f"{'strength':<10} {'method':<34} latency")
    print("-" * 72)
    for m in ordered:
        print(
            f"{stars(m.get('strength', 0)):<10} {m.get('name', ''):<34} "
            f"{m.get('latency', '')}"
        )
    print(
        "\nNo single row is sufficient on its own. Stack one instant check for "
        "coverage\nwith one documentary check for defensibility."
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--ladder", action="store_true")
    ap.add_argument("--min", type=int, default=0, help="filter by minimum strength")
    ap.add_argument("--data", type=Path, default=Path("methods.yaml"))
    ap.add_argument("--readme", type=Path, default=Path("README.md"))
    args = ap.parse_args()

    methods = yaml.safe_load(args.data.read_text(encoding="utf-8"))["methods"]
    methods = [m for m in methods if int(m.get("strength", 0)) >= args.min]
    if not methods:
        raise SystemExit("No methods at or above that strength.")

    if args.ladder:
        print_ladder(methods)
        return 0

    table = build_table(methods)
    if not args.write:
        print(table)
        return 0

    text = args.readme.read_text(encoding="utf-8")
    if START not in text or END not in text:
        raise SystemExit("README is missing the TABLE markers.")
    before, after = text.split(START)[0], text.split(END)[1]
    args.readme.write_text(f"{before}{START}\n{table}\n{END}{after}", encoding="utf-8")
    print(f"Updated table in {args.readme} ({len(methods)} methods).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
