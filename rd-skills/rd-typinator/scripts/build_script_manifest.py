#!/usr/bin/env python3
"""Build a canonical Typinator script manifest.

Output CSV columns:
- alias_path
- canonical_path
- status (active|deprecated)
- category
- interactive_allowed (yes|no)

Rules:
- Real script files are emitted as active rows with empty alias_path.
- Symlinked script files are emitted as deprecated alias rows that point to canonical targets.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path
import re


SCRIPT_EXTS = {".applescript", ".scpt", ".sh", ".py", ".rb", ".swift", ".js"}
INTERACTIVE_PATTERNS = [
    re.compile(r"\bdisplay dialog\b", re.IGNORECASE),
    re.compile(r"\bdisplay alert\b", re.IGNORECASE),
    re.compile(r"\bchoose from list\b", re.IGNORECASE),
    re.compile(r"\bchoose file\b", re.IGNORECASE),
    re.compile(r"\bchoose folder\b", re.IGNORECASE),
]


def is_script_file(path: Path) -> bool:
    return path.is_file() and path.suffix.lower() in SCRIPT_EXTS


def interactive_allowed(path: Path) -> str:
    try:
        text = path.read_text(errors="ignore")
    except Exception:  # noqa: BLE001
        return "unknown"
    for pat in INTERACTIVE_PATTERNS:
        if pat.search(text):
            return "no"
    return "yes"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--includes-root",
        default="/Users/rd/.config/typinator/Sets/Includes",
        help="Typinator Includes root",
    )
    ap.add_argument(
        "--out",
        default=None,
        help="Output manifest CSV path (default: Includes/Documentation/Generated/script-manifest.csv)",
    )
    args = ap.parse_args()

    includes_root = Path(args.includes_root).expanduser().resolve()
    scripts_root = includes_root / "Scripts"
    if not scripts_root.exists():
        print(f"ERROR: scripts root not found: {scripts_root}")
        return 2

    out_path = (
        Path(args.out).expanduser().resolve()
        if args.out
        else includes_root / "Documentation" / "Reference" / "script-manifest.csv"
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for p in sorted(scripts_root.rglob("*")):
        if not is_script_file(p):
            continue
        rel = p.relative_to(includes_root).as_posix()
        parts = rel.split("/")
        category = parts[1] if len(parts) > 1 else "Scripts"

        if p.is_symlink():
            try:
                target = p.resolve()
            except Exception:  # noqa: BLE001
                target = p
            if not target.exists():
                continue
            canonical_rel = target.relative_to(includes_root).as_posix()
            rows.append(
                {
                    "alias_path": rel,
                    "canonical_path": canonical_rel,
                    "status": "deprecated",
                    "category": category,
                    "interactive_allowed": interactive_allowed(target),
                }
            )
        else:
            rows.append(
                {
                    "alias_path": "",
                    "canonical_path": rel,
                    "status": "active",
                    "category": category,
                    "interactive_allowed": interactive_allowed(p),
                }
            )

    with out_path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(
            fh,
            fieldnames=[
                "alias_path",
                "canonical_path",
                "status",
                "category",
                "interactive_allowed",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote manifest: {out_path} ({len(rows)} rows)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

