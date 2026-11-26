#!/usr/bin/env python3
"""Interactively fix Typinator CSV exports.

Features:
- Scan one CSV file or a directory of CSV exports
- Show per-file issue summary
- Prompt which fixes to apply
- Optionally deduplicate abbreviations (keep first/last/all)
- Write fixed copies to output directory (safe default) or in-place with backup
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import re
from typing import Iterable

TRANSLATIONS = {
    "\u2028": "\n",
    "\u2029": "\n",
    "\ufeff": "",
    "\u200b": "",
    "\u200c": "",
    "\u200d": "",
}

FORM_PATTERN = re.compile(r"\{form:([^}]+)\}")

FIX_KEYS = [
    "normalize_unicode",
    "normalize_newlines",
    "collapse_blank_lines",
    "fix_shell_marker",
    "remove_skip_if_null",
    "convert_form_placeholders",
]

FIX_LABELS = {
    "normalize_unicode": "normalize zero-width/BOM and Unicode line separators",
    "normalize_newlines": "normalize CRLF/CR to LF",
    "collapse_blank_lines": "collapse 3+ blank lines to 2",
    "fix_shell_marker": "fix malformed shell marker ({Shell/ -> {/Shell)",
    "remove_skip_if_null": "remove '<Skip if null>' artifacts",
    "convert_form_placeholders": "convert {form:name} to {{?name}}",
}


@dataclass
class FileScan:
    total_rows: int
    data_rows: int
    issue_counts: dict[str, int]
    duplicate_groups: dict[str, list[int]]
    has_header: bool


def yes_no(prompt: str, default: bool = True) -> bool:
    suffix = "[Y/n]" if default else "[y/N]"
    while True:
        raw = input(f"{prompt} {suffix} ").strip().lower()
        if not raw:
            return default
        if raw in {"y", "yes"}:
            return True
        if raw in {"n", "no"}:
            return False
        print("Please answer y or n.")


def choose(prompt: str, options: list[str], default_index: int = 0) -> str:
    for i, option in enumerate(options, start=1):
        mark = " (default)" if i - 1 == default_index else ""
        print(f"  {i}. {option}{mark}")
    while True:
        raw = input(f"{prompt} [1-{len(options)}]: ").strip()
        if not raw:
            return options[default_index]
        if raw.isdigit():
            idx = int(raw)
            if 1 <= idx <= len(options):
                return options[idx - 1]
        print("Enter a valid option number.")


def detect_text_issues(text: str) -> set[str]:
    issues: set[str] = set()

    if any(ch in text for ch in TRANSLATIONS):
        issues.add("normalize_unicode")
    if "\r" in text:
        issues.add("normalize_newlines")
    if re.search(r"\n\s*\n\s*\n+", text):
        issues.add("collapse_blank_lines")
    if "{Shell/" in text:
        issues.add("fix_shell_marker")
    if "<Skip if null>" in text:
        issues.add("remove_skip_if_null")
    if FORM_PATTERN.search(text):
        issues.add("convert_form_placeholders")

    return issues


def apply_text_fixes(text: str, selected_fixes: set[str]) -> str:
    out = text

    if "normalize_unicode" in selected_fixes:
        for src, dst in TRANSLATIONS.items():
            out = out.replace(src, dst)
    if "normalize_newlines" in selected_fixes:
        out = out.replace("\r\n", "\n").replace("\r", "\n")
    if "collapse_blank_lines" in selected_fixes:
        out = re.sub(r"\n\s*\n\s*\n+", "\n\n", out)
    if "fix_shell_marker" in selected_fixes:
        out = out.replace("{Shell/", "{/Shell")
    if "remove_skip_if_null" in selected_fixes:
        out = out.replace("<Skip if null>", "")
    if "convert_form_placeholders" in selected_fixes:
        out = FORM_PATTERN.sub(lambda m: "{{?" + m.group(1).strip() + "}}", out)

    return out


def read_csv_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as f:
        return [list(row) for row in csv.reader(f)]


def write_csv_rows(path: Path, rows: Iterable[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        csv.writer(f).writerows(rows)


def scan_file(rows: list[list[str]]) -> FileScan:
    issue_counts = {k: 0 for k in FIX_KEYS}

    has_header = bool(rows and len(rows[0]) >= 2 and rows[0][0].strip().lower() == "abbreviation" and rows[0][1].strip().lower() == "expansion")
    start_index = 1 if has_header else 0

    abbr_map: dict[str, list[int]] = {}
    data_rows = 0

    for i in range(start_index, len(rows)):
        row = rows[i]
        if not row:
            continue
        data_rows += 1
        abbr = row[0].strip() if len(row) >= 1 else ""
        exp = row[1] if len(row) >= 2 else ""

        if abbr:
            abbr_map.setdefault(abbr, []).append(i)

        for issue in detect_text_issues(exp):
            issue_counts[issue] += 1

    duplicate_groups = {abbr: idxs for abbr, idxs in abbr_map.items() if len(idxs) > 1}

    return FileScan(
        total_rows=len(rows),
        data_rows=data_rows,
        issue_counts=issue_counts,
        duplicate_groups=duplicate_groups,
        has_header=has_header,
    )


def dedupe_rows(rows: list[list[str]], has_header: bool, mode: str) -> tuple[list[list[str]], int]:
    if mode == "keep_all":
        return rows, 0

    start_index = 1 if has_header else 0
    kept: list[list[str]] = rows[:start_index]
    removed = 0

    if mode == "keep_first":
        seen: set[str] = set()
        for row in rows[start_index:]:
            abbr = row[0].strip() if row else ""
            if not abbr:
                kept.append(row)
                continue
            if abbr in seen:
                removed += 1
                continue
            seen.add(abbr)
            kept.append(row)
        return kept, removed

    if mode == "keep_last":
        last_index: dict[str, int] = {}
        indexed = list(enumerate(rows[start_index:], start=start_index))
        for i, row in indexed:
            abbr = row[0].strip() if row else ""
            if abbr:
                last_index[abbr] = i

        for i, row in indexed:
            abbr = row[0].strip() if row else ""
            if not abbr:
                kept.append(row)
                continue
            if last_index.get(abbr) != i:
                removed += 1
                continue
            kept.append(row)
        return kept, removed

    raise ValueError(f"Unknown dedupe mode: {mode}")


def output_path_for(src_file: Path, src_root: Path, out_dir: Path | None, in_place: bool) -> Path:
    if in_place:
        return src_file
    if out_dir is None:
        raise ValueError("out_dir must be set when not using in-place mode")
    rel = src_file.relative_to(src_root)
    return out_dir / rel


def make_backup(path: Path) -> Path:
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup = path.with_suffix(path.suffix + f".bak-{stamp}")
    backup.write_bytes(path.read_bytes())
    return backup


def process_file(src_file: Path, src_root: Path, out_dir: Path | None, in_place: bool, backup: bool) -> None:
    print("\n" + "=" * 88)
    print(f"File: {src_file}")

    rows = read_csv_rows(src_file)
    scan = scan_file(rows)

    print(f"Rows: total={scan.total_rows}, data={scan.data_rows}, header={'yes' if scan.has_header else 'no'}")
    print("Issues:")
    found_any = False
    for key in FIX_KEYS:
        count = scan.issue_counts[key]
        if count > 0:
            found_any = True
            print(f"  - {FIX_LABELS[key]}: {count}")
    if not found_any:
        print("  - none detected")

    dup_count = len(scan.duplicate_groups)
    dup_rows = sum(len(v) - 1 for v in scan.duplicate_groups.values())
    print(f"Duplicate abbreviations: groups={dup_count}, removable_rows={dup_rows}")

    if not yes_no("Process this file?", default=True):
        print("Skipped.")
        return

    selected_fixes: set[str] = set()
    for key in FIX_KEYS:
        if scan.issue_counts[key] > 0 and yes_no(f"Apply fix: {FIX_LABELS[key]}?", default=True):
            selected_fixes.add(key)

    dedupe_mode = "keep_all"
    if dup_count > 0:
        dedupe_mode = choose(
            "Duplicate abbreviation strategy",
            ["keep_all", "keep_first", "keep_last"],
            default_index=1,
        )

    changed_text_rows = 0
    start_index = 1 if scan.has_header else 0

    out_rows = [list(r) for r in rows]
    for i in range(start_index, len(out_rows)):
        row = out_rows[i]
        if len(row) >= 2:
            original = row[1]
            updated = apply_text_fixes(original, selected_fixes)
            if updated != original:
                row[1] = updated
                changed_text_rows += 1

    deduped_rows, removed_rows = dedupe_rows(out_rows, scan.has_header, dedupe_mode)

    out_file = output_path_for(src_file, src_root, out_dir, in_place)

    if in_place and backup:
        backup_path = make_backup(src_file)
        print(f"Backup: {backup_path}")

    write_csv_rows(out_file, deduped_rows)
    print(f"Wrote: {out_file}")
    print(f"Changed rows (text fixes): {changed_text_rows}")
    print(f"Removed duplicate rows: {removed_rows}")


def collect_csv_files(src: Path) -> tuple[Path, list[Path]]:
    if src.is_file():
        return src.parent, [src]
    files = sorted(src.glob("*.csv"))
    return src, files


def main() -> int:
    parser = argparse.ArgumentParser(description="Interactively fix Typinator CSV exports")
    parser.add_argument("--src", required=True, help="CSV file or directory containing CSV files")
    parser.add_argument(
        "--out",
        help="Output directory for fixed files (default: <src>/Cleaned-Interactive when --src is directory)",
    )
    parser.add_argument("--in-place", action="store_true", help="Overwrite source files")
    parser.add_argument("--no-backup", action="store_true", help="Disable .bak backups for --in-place")
    args = parser.parse_args()

    src = Path(args.src).expanduser().resolve()
    if not src.exists():
        raise FileNotFoundError(src)

    src_root, files = collect_csv_files(src)
    if not files:
        print("No CSV files found.")
        return 0

    out_dir: Path | None = None
    if not args.in_place:
        if args.out:
            out_dir = Path(args.out).expanduser().resolve()
        elif src.is_dir():
            out_dir = src / "Cleaned-Interactive"
        else:
            out_dir = src.parent / "Cleaned-Interactive"
        out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Found {len(files)} CSV file(s).")
    if args.in_place:
        print("Mode: in-place overwrite")
    else:
        print(f"Mode: write fixed copies to {out_dir}")

    for file in files:
        process_file(
            src_file=file,
            src_root=src_root,
            out_dir=out_dir,
            in_place=args.in_place,
            backup=not args.no_backup,
        )

    print("\nDone.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
