"""csv_to_markdown.py — Convert a CSV to a Markdown table.

Usage:
    python csv_to_markdown.py input.csv [--delimiter ,] [--out table.md]
"""

import argparse
import csv
import sys
from pathlib import Path


def to_markdown(rows: list[list[str]]) -> str:
    if not rows:
        return ""
    header, *body = rows
    widths = [max(len(str(cell)) for cell in col) for col in zip(*rows)]

    def row(cells: list[str]) -> str:
        return "| " + " | ".join(c.ljust(w) for c, w in zip(cells, widths)) + " |"

    sep = "| " + " | ".join("-" * w for w in widths) + " |"
    return "\n".join([row(header), sep, *(row(r) for r in body)])


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv", help="Path to the input CSV")
    parser.add_argument("--delimiter", default=",", help="CSV delimiter (default: ,)")
    parser.add_argument("--out", help="Optional output file; defaults to stdout")
    args = parser.parse_args()

    with open(args.csv, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f, delimiter=args.delimiter))

    md = to_markdown(rows)

    if args.out:
        Path(args.out).write_text(md, encoding="utf-8")
        print(f"Wrote {len(rows)} rows to {args.out}", file=sys.stderr)
    else:
        print(md)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
