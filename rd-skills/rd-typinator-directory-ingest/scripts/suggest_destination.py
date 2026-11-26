#!/usr/bin/env python3
"""Suggest likely canonical destination files for a source path or label."""

from __future__ import annotations

import argparse


RULES = [
    ("icons", "directory/icons.txt"),
    ("apfspace", "directory/apfspace.txt"),
    ("obsidian", "directory/obsidian.txt"),
    ("scripts", "directory/scripts.txt"),
    ("karabiner", "app/karabiner.txt"),
    ("keyboard maestro", "app/keyboard-maestro.txt"),
    ("keyboard-maestro", "app/keyboard-maestro.txt"),
    ("typinator", "app/typinator.txt"),
    ("shell", "util/shell.txt"),
    ("zsh", "util/shell.txt"),
    ("system-profile", "system/system-profile.txt"),
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Suggest a likely canonical destination from a source label."
    )
    parser.add_argument("--source", required=True, help="Source path or label")
    return parser.parse_args()


def main() -> int:
    source = parse_args().source.strip().lower()
    matches: list[str] = []

    for needle, destination in RULES:
        if needle in source and destination not in matches:
            matches.append(destination)

    if not matches:
        print("NO_MATCH")
        print(
            "Inspect existing canonical files manually and choose the domain owner."
        )
        return 0

    print("LIKELY_DESTINATIONS")
    for match in matches:
        print(f"- {match}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
