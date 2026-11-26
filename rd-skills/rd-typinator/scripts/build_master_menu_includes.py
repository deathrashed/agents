#!/usr/bin/env python3
"""Build master menu targeting runtime CSV lookup tables by default.

Default base:
  /Users/rd/.config/typinator/Sets/Includes/Reference/CSV

Usage:
  python3 build_master_menu_includes.py --file Prompts.csv --abbr "@prompt menu" --title Prompts
"""

from __future__ import annotations

import argparse
from pathlib import Path
import subprocess

DEFAULT_BASE = Path("/Users/rd/.config/typinator/Sets/Includes/Reference/CSV")
THIS_DIR = Path(__file__).resolve().parent
BUILD_SCRIPT = THIS_DIR / "build_master_menu.py"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True, help="CSV filename under base dir (e.g. Prompts.csv)")
    ap.add_argument("--abbr", required=True, help="Menu abbreviation")
    ap.add_argument("--title", required=True, help="Menu title")
    ap.add_argument("--base", default=str(DEFAULT_BASE), help="Base directory containing CSV sets")
    args = ap.parse_args()

    csv_path = (Path(args.base).expanduser().resolve() / args.file).resolve()
    if not csv_path.exists():
        raise FileNotFoundError(csv_path)

    cmd = [
        "python3",
        str(BUILD_SCRIPT),
        "--csv",
        str(csv_path),
        "--abbr",
        args.abbr,
        "--title",
        args.title,
    ]
    completed = subprocess.run(cmd, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())
