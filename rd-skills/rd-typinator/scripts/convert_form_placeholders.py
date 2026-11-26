#!/usr/bin/env python3
"""Convert non-Typinator {form:name} placeholders into Typinator input fields."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re

PATTERN = re.compile(r"\{form:([^}]+)\}")


def convert(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        label = m.group(1).strip()
        return "{{?" + label + "}}"

    text = PATTERN.sub(repl, text)
    text = text.replace('<Skip if null>', '')
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Path to CSV file")
    args = ap.parse_args()

    csv_path = Path(args.csv).expanduser().resolve()
    with csv_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    changed = 0
    for row in rows:
        if len(row) >= 2:
            new = convert(row[1])
            if new != row[1]:
                row[1] = new
                changed += 1

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

    print(f"Updated {csv_path}: {changed} rows changed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
