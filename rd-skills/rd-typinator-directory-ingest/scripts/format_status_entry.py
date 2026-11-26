#!/usr/bin/env python3
"""Generate a STATUS log entry for a processed ingest source."""

from __future__ import annotations

import argparse
from datetime import date


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Format a _docs/STATUS.md entry for a processed source."
    )
    parser.add_argument("--source", required=True, help="Source path label")
    parser.add_argument(
        "--dest",
        action="append",
        required=True,
        help="Destination canonical path label; repeat for multiple files",
    )
    parser.add_argument(
        "--date",
        default=date.today().isoformat(),
        help="Date for the entry in YYYY-MM-DD format",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    destination_text = ", ".join(args.dest)
    print(f"- [x] {args.source} → {destination_text} ({args.date})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
