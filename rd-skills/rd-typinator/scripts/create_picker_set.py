#!/usr/bin/env python3
"""Generate a grouped picker CSV set from newline-delimited options."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def safe_label(value: str) -> str:
    return value.replace(":", "꞉").replace("|", "¦")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True, help="Output CSV file")
    ap.add_argument("--abbr", required=True, help="Picker abbreviation")
    ap.add_argument("--title", required=True, help="Picker title")
    ap.add_argument("--options-file", required=True, help="Text file with one option per line")
    ap.add_argument("--insert-values", action="store_true", help="Use label:value form by splitting on first tab")
    args = ap.parse_args()

    options_path = Path(args.options_file).expanduser().resolve()
    lines = [line.strip() for line in options_path.read_text(encoding="utf-8").splitlines() if line.strip()]
    options: list[str] = []
    for line in lines:
        if args.insert_values and "\t" in line:
            label, value = line.split("\t", 1)
            options.append(f"{safe_label(label)}:{value}")
        else:
            options.append(safe_label(line))
    expansion = f"{{{{sel=?{args.title}({ '|'.join(options) })}}}}{{{{sel}}}}"

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["abbreviation", "expansion"])
        writer.writerow([args.abbr, expansion])
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
