#!/usr/bin/env python3
"""Run a whole-system health check across Typinator live sets, exports, scripts, and Includes."""

from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from _typinator_common import (  # noqa: E402
    Finding,
    dump_live_typinator_state,
    evaluate_csv_file,
    interactive_allowed,
    iter_script_files,
    list_csv_files,
    manifest_alias_map,
    normalized_expansion,
    parse_rows,
    referenced_script_paths,
    script_filename_conflicts,
    summarize_live_state,
    to_json,
    warn_exported_directory_case,
)


def orphan_runtime_assets(includes_root: Path, csv_files: list[Path]) -> tuple[list[str], list[str]]:
    referenced_scripts: set[str] = set()
    orphan_text_assets: list[str] = []
    for csv_file in csv_files:
        for row in parse_rows(csv_file):
            if len(row) < 2:
                continue
            referenced_scripts.update(referenced_script_paths(row[1]))
    script_orphans: list[str] = []
    for script_path in iter_script_files(includes_root / "Scripts"):
        rel = script_path.relative_to(includes_root).as_posix()
        if rel not in referenced_scripts:
            script_orphans.append(rel)
    text_root = includes_root / "Text"
    for text_path in sorted(text_root.rglob("*")):
        if not text_path.is_file():
            continue
        rel = text_path.relative_to(includes_root).as_posix()
        referenced = False
        needle = text_path.name
        for csv_file in csv_files:
            for row in parse_rows(csv_file):
                if any(needle in cell for cell in row):
                    referenced = True
                    break
            if referenced:
                break
        if not referenced:
            orphan_text_assets.append(rel)
    return script_orphans, orphan_text_assets


def duplicate_semantics(csv_files: list[Path]) -> list[dict[str, object]]:
    groups: dict[str, list[dict[str, str]]] = {}
    for csv_file in csv_files:
        for row in parse_rows(csv_file):
            if len(row) < 2 or not row[0].strip():
                continue
            key = normalized_expansion(row[1])
            if not key:
                continue
            groups.setdefault(key, []).append({"file": csv_file.name, "abbreviation": row[0].strip()})
    out = []
    for key, entries in groups.items():
        if len(entries) < 2:
            continue
        out.append({"hash": key[:64], "count": len(entries), "entries": entries[:10]})
    return sorted(out, key=lambda item: (-item["count"], item["hash"]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--includes-root", default="/Users/rd/.config/typinator/Sets/Includes")
    ap.add_argument("--export-dir", default=None)
    ap.add_argument("--manifest", default=None)
    ap.add_argument("--out", default=None, help="Optional markdown report path")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    includes_root = Path(args.includes_root).expanduser().resolve()
    export_dir = Path(args.export_dir).expanduser().resolve() if args.export_dir else includes_root / "Exported"
    manifest_path = Path(args.manifest).expanduser().resolve() if args.manifest else None

    alias_map = manifest_alias_map(manifest_path)
    export_dir_exists = export_dir.exists()
    csv_files = list_csv_files(export_dir)
    findings: list[Finding] = []
    findings.extend(Finding("warning", "exported_directory_case", msg, str(export_dir)) for msg in warn_exported_directory_case(includes_root))
    if not export_dir_exists:
        findings.append(Finding("warning", "missing_export_dir", f"export directory not found: {export_dir}", str(export_dir)))
    for csv_file in csv_files:
        findings.extend(evaluate_csv_file(csv_file, includes_root, alias_map=alias_map))
    for rel in script_filename_conflicts(includes_root / "Scripts"):
        findings.append(Finding("error", "script_filename_conflict", f"script filename contains marker-conflicting characters: {rel}", str(includes_root / 'Scripts')))

    live_state = dump_live_typinator_state()
    live_summary = summarize_live_state(live_state)
    script_orphans, text_orphans = orphan_runtime_assets(includes_root, csv_files)
    semantic_duplicates = duplicate_semantics(csv_files)
    interactive_scripts = [
        path.relative_to(includes_root).as_posix()
        for path in iter_script_files(includes_root / "Scripts")
        if interactive_allowed(path) == "no"
    ]

    payload = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "includes_root": str(includes_root),
        "export_dir": str(export_dir),
        "export_dir_exists": export_dir_exists,
        "live": live_summary,
        "csv_files": [p.name for p in csv_files],
        "summary": dict(Counter(f.severity for f in findings)),
        "findings": [f.to_dict() for f in findings],
        "orphan_scripts": script_orphans[:100],
        "orphan_text_assets": text_orphans[:100],
        "interactive_scripts": interactive_scripts[:100],
        "semantic_duplicates": semantic_duplicates[:50],
    }

    if args.out:
        out_path = Path(args.out).expanduser().resolve()
        lines = [
            "# Typinator Doctor Report",
            "",
            f"Generated: {payload['generated_at']}",
            f"- Includes root: `{includes_root}`",
            f"- Export dir: `{export_dir}`",
            f"- Live Typinator available: `{live_summary.get('available', False)}`",
            f"- Live set count: `{live_summary.get('set_count', 0)}`",
            f"- Live rule count: `{live_summary.get('rule_count', 0)}`",
            "",
            "## Findings",
        ]
        if payload["findings"]:
            for finding in payload["findings"]:
                row = f":{finding['row']}" if finding.get("row") else ""
                abbr = f" [{finding['abbreviation']}]" if finding.get("abbreviation") else ""
                lines.append(f"- `{finding['severity']}` `{finding['rule_id']}` `{finding['file']}{row}`{abbr}: {finding['message']}")
        else:
            lines.append("- No validator findings.")
        lines.extend(["", "## Orphans"])
        lines.append(f"- Orphan scripts: `{len(script_orphans)}`")
        lines.append(f"- Orphan text assets: `{len(text_orphans)}`")
        lines.extend(["", "## Semantic Duplicates"])
        if semantic_duplicates:
            for group in semantic_duplicates[:15]:
                sample = ", ".join(f"{entry['file']}:{entry['abbreviation']}" for entry in group["entries"][:4])
                lines.append(f"- `{group['count']}` matching expansions: {sample}")
        else:
            lines.append("- No likely duplicate expansions found.")
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    if args.json:
        print(to_json(payload))
    else:
        print(f"Typinator doctor checked {len(csv_files)} export file(s).")
        print(f"Live Typinator available: {live_summary.get('available', False)}")
        print(f"Findings: {payload['summary']}")
        print(f"Orphan scripts: {len(script_orphans)}")
        print(f"Orphan text assets: {len(text_orphans)}")
        print(f"Semantic duplicate groups: {len(semantic_duplicates)}")
        if args.out:
            print(f"Report: {Path(args.out).expanduser().resolve()}")

    return 0 if payload["summary"].get("error", 0) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
