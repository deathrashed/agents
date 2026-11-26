#!/usr/bin/env python3
"""Validate and optionally autofix Typinator exported CSV sets."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from _typinator_common import (  # noqa: E402
    FIX_KEYS,
    Finding,
    apply_manifest_rewrites,
    apply_text_fixes,
    evaluate_csv_file,
    list_csv_files,
    load_manifest_aliases,
    manifest_alias_map,
    parse_rows,
    script_filename_conflicts,
    summarize_live_state,
    to_json,
    warn_exported_directory_case,
    write_csv_rows,
)


def rewrite_rows(rows: list[list[str]], alias_map: dict[str, str]) -> tuple[list[list[str]], int]:
    changed = 0
    updated_rows: list[list[str]] = []
    for row in rows:
        if len(row) < 2:
            updated_rows.append(row)
            continue
        new_row = list(row)
        original = new_row[1]
        fixed = apply_text_fixes(original, set(FIX_KEYS))
        fixed, rewrites = apply_manifest_rewrites(fixed, alias_map)
        if fixed != original or rewrites:
            new_row[1] = fixed
            changed += 1
        updated_rows.append(new_row)
    return updated_rows, changed


def format_findings(findings: list[Finding]) -> str:
    lines: list[str] = []
    by_file: dict[str, list[Finding]] = {}
    for finding in findings:
        by_file.setdefault(finding.file, []).append(finding)
    for file_name in sorted(by_file):
        lines.append(f"{file_name}:")
        for item in sorted(by_file[file_name], key=lambda f: (f.row or 0, f.severity, f.rule_id)):
            location = f":{item.row}" if item.row else ""
            abbr = f" [{item.abbreviation}]" if item.abbreviation else ""
            fix = f" | suggestion: {item.suggestion}" if item.suggestion else ""
            lines.append(f"  - {item.severity.upper()} {item.rule_id}{location}{abbr}: {item.message}{fix}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--includes-root", default="/Users/rd/.config/typinator/Sets/Includes", help="Typinator Includes root")
    ap.add_argument("--export-dir", default=None, help="Export directory (defaults to Includes/Exported)")
    ap.add_argument("--manifest", default=None, help="Optional alias manifest CSV")
    ap.add_argument("--max-abbr-words", type=int, default=None, help="Optional max words allowed in abbreviations")
    ap.add_argument("--fix", action="store_true", help="Apply safe autofixes in-place")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable JSON")
    args = ap.parse_args()

    includes_root = Path(args.includes_root).expanduser().resolve()
    export_dir = Path(args.export_dir).expanduser().resolve() if args.export_dir else includes_root / "Exported"
    manifest_path = Path(args.manifest).expanduser().resolve() if args.manifest else None

    alias_map = manifest_alias_map(manifest_path)
    alias_hits = load_manifest_aliases(manifest_path)

    findings: list[Finding] = []
    for message in warn_exported_directory_case(includes_root):
        findings.append(Finding("warning", "exported_directory_case", message, str(export_dir)))

    csv_files = list_csv_files(export_dir)
    if not export_dir.exists():
        payload = {"ok": False, "error": f"export directory not found: {export_dir}"}
        print(to_json(payload) if args.json else payload["error"])
        return 2

    changed_files: dict[str, int] = {}
    if args.fix:
        for csv_file in csv_files:
            rows = parse_rows(csv_file)
            rewritten_rows, changed = rewrite_rows(rows, alias_map)
            if changed:
                write_csv_rows(csv_file, rewritten_rows)
                changed_files[csv_file.name] = changed

    for csv_file in csv_files:
        findings.extend(
            evaluate_csv_file(
                csv_file,
                includes_root,
                alias_map=alias_map,
                max_abbr_words=args.max_abbr_words,
            )
        )

    for rel in script_filename_conflicts(includes_root / "Scripts"):
        findings.append(
            Finding("error", "script_filename_conflict", f"script filename contains marker-conflicting characters: {rel}", str(includes_root / "Scripts"))
        )

    counts = Counter(f.severity for f in findings)
    payload = {
        "ok": counts["error"] == 0,
        "export_dir": str(export_dir),
        "csv_files": [p.name for p in csv_files],
        "manifest_aliases_loaded": len(alias_hits),
        "fix_applied": args.fix,
        "changed_files": changed_files,
        "summary": dict(counts),
        "findings": [finding.to_dict() for finding in findings],
    }

    if args.json:
        print(to_json(payload))
    else:
        print(f"Validated {len(csv_files)} CSV files in {export_dir}")
        if changed_files:
            print("Applied safe autofixes:")
            for name, count in sorted(changed_files.items()):
                print(f"  - {name}: {count} row(s) updated")
        if findings:
            print(format_findings(findings))
        else:
            print("All checks passed.")

    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
