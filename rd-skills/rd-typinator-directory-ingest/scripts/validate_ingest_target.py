#!/usr/bin/env python3
"""Validate Directory ingest inputs before processing."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a Directory ingest source file."
    )
    parser.add_argument("--directory-root", required=True, help="Directory root path")
    parser.add_argument("--source", required=True, help="Source file path")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    directory_root = Path(args.directory_root).expanduser().resolve()
    source = Path(args.source).expanduser().resolve()
    extracted_root = directory_root / "_extracted"
    processed_root = extracted_root / "•processed"

    required_docs = [
        directory_root / "AGENTS.md",
        directory_root / "_docs" / "INGEST.md",
        directory_root / "_docs" / "TRANSFORM.md",
        directory_root / "_docs" / "STATUS.md",
    ]

    errors: list[str] = []

    if not directory_root.exists():
        errors.append(f"Directory root does not exist: {directory_root}")

    if not source.exists():
        errors.append(f"Source file does not exist: {source}")

    if source.exists() and not source.is_file():
        errors.append(f"Source is not a regular file: {source}")

    source_kind = "EXTERNAL"

    try:
        source.relative_to(extracted_root)
        source_kind = "STAGED"
    except ValueError:
        source_kind = "EXTERNAL"

    if source_kind == "STAGED":
        try:
            source.relative_to(processed_root)
            errors.append(f"Source is already archived in •processed/: {source}")
        except ValueError:
            pass

    for doc in required_docs:
        if not doc.exists():
            errors.append(f"Required governing doc is missing: {doc}")

    if errors:
        print("INVALID")
        for error in errors:
            print(f"- {error}")
        return 1

    print("VALID")
    print(f"- Source kind: {source_kind}")
    print(f"- Directory root: {directory_root}")
    print(f"- Source file: {source}")
    print(f"- Staging root: {extracted_root}")
    print(f"- Archive root: {processed_root}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
