#!/usr/bin/env python3
"""Normalize Typinator CSV exports into a cleaned output directory."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re

TRANSLATIONS = {
    "\u2028": "\n",
    "\u2029": "\n",
    "\ufeff": "",
    "\u200b": "",
    "\u200c": "",
    "\u200d": "",
}


def clean_text(text: str) -> str:
    for src, dst in TRANSLATIONS.items():
        text = text.replace(src, dst)
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"\n\s*\n\s*\n+", "\n\n", text)
    text = text.replace("{Shell/", "{/Shell")
    text = text.replace('<Skip if null>', '')
    return text


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="Source directory with CSV exports")
    ap.add_argument("--out", required=True, help="Output directory for cleaned CSV files")
    args = ap.parse_args()

    src = Path(args.src).expanduser().resolve()
    out = Path(args.out).expanduser().resolve()
    out.mkdir(parents=True, exist_ok=True)

    for csv_file in sorted(src.glob("*.csv")):
        with csv_file.open(encoding="utf-8", newline="") as f:
            rows = list(csv.reader(f))

        cleaned_rows = []
        for row in rows:
            if len(row) >= 2:
                row = list(row)
                row[1] = clean_text(row[1])
            cleaned_rows.append(row)

        out_file = out / csv_file.name
        with out_file.open("w", encoding="utf-8", newline="") as f:
            csv.writer(f).writerows(cleaned_rows)

        print(f"Cleaned: {out_file}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
