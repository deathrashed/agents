#!/usr/bin/env python3
"""Archive a processed staged file into _extracted/•processed/."""

from __future__ import annotations

import argparse
from pathlib import Path
import shutil
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Archive a processed Directory ingest input."
    )
    parser.add_argument("--directory-root", required=True, help="Directory root path")
    parser.add_argument("--source", required=True, help="Source file path")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show the archive destination without moving the file",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    directory_root = Path(args.directory_root).expanduser().resolve()
    source = Path(args.source).expanduser().resolve()
    extracted_root = directory_root / "_extracted"
    processed_root = extracted_root / "•processed"

    if not source.exists():
        print(f"Source file does not exist: {source}", file=sys.stderr)
        return 1

    try:
        relative = source.relative_to(extracted_root)
    except ValueError:
        print(f"Source is not inside _extracted/: {source}", file=sys.stderr)
        return 1

    destination = processed_root / relative

    if args.dry_run:
        print(destination)
        return 0

    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(source), str(destination))
    print(destination)
    return 0


if __name__ == "__main__":
    sys.exit(main())
