#!/usr/bin/env python3
"""Build or update a Typinator master-menu row in a CSV set.

Usage:
  python3 build_master_menu.py --csv "/abs/path/set.csv" --abbr "@menu" --title "Prompts"
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


def safe_label(value: str) -> str:
    return (
        value.replace(":", "꞉")
        .replace("|", "¦")
        .replace(")", "⟯")
        .replace("(", "⟮")
    )


def build_menu_expansion(csv_path: Path, title: str, abbreviations: list[str]) -> str:
    options = "|".join(f"{safe_label(a)}:{a}" for a in abbreviations)
    return (
        f"{{{{?*{title} Master Menu*}}}}{{{{?--}}}}{{{{?_Select any abbreviation from this set to output its full expansion text._}}}}{{{{?--}}}}"
        f"{{{{sel=?Abbreviation({options})}}}}"
        "{/Shell\n"
        "python3 - <<'PY'\n"
        "import csv\n"
        f"path = {str(csv_path)!r}\n"
        'target = "{{sel}}"\n'
        "with open(path, encoding='utf-8', newline='') as f:\n"
        "    for row in csv.reader(f):\n"
        "        if row and row[0] == target:\n"
        "            print(row[1], end='')\n"
        "            break\n"
        "PY\n"
        "}"
    )


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--csv", required=True, help="Absolute path to Typinator CSV set")
    p.add_argument("--abbr", required=True, help="Menu abbreviation")
    p.add_argument("--title", required=True, help="Menu title")
    args = p.parse_args()

    csv_path = Path(args.csv).expanduser().resolve()
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    with csv_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.reader(f))

    rows = [r for r in rows if not (r and r[0] == args.abbr)]
    abbreviations = [r[0] for r in rows if r]
    menu = [args.abbr, build_menu_expansion(csv_path, args.title, abbreviations)]
    rows.append(menu)

    with csv_path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)

    print(f"Updated {csv_path} with menu {args.abbr} ({len(abbreviations)} options)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
