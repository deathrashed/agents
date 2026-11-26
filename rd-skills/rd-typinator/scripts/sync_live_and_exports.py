#!/usr/bin/env python3
"""Compare live Typinator sets against export artifacts and report drift."""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from _typinator_common import dump_live_typinator_state, list_csv_files, parse_rows, to_json  # noqa: E402


def slug(value: str) -> str:
    normalized = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return normalized or "unnamed"


def load_exports(export_dir: Path) -> dict[str, dict[str, str]]:
    exports: dict[str, dict[str, str]] = {}
    for csv_file in list_csv_files(export_dir):
        set_name = csv_file.stem
        rows: dict[str, str] = {}
        for row in parse_rows(csv_file):
            if len(row) >= 2 and row[0].strip():
                rows[row[0].strip()] = row[1]
        exports[set_name] = rows
    return exports


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--includes-root", default="/Users/rd/.config/typinator/Sets/Includes")
    ap.add_argument("--export-dir", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    includes_root = Path(args.includes_root).expanduser().resolve()
    export_dir = Path(args.export_dir).expanduser().resolve() if args.export_dir else includes_root / "Exported"
    live_state = dump_live_typinator_state()
    if not export_dir.exists():
        payload = {"ok": False, "reason": f"export directory not found: {export_dir}", "export_dir": str(export_dir)}
        print(to_json(payload) if args.json else payload["reason"])
        return 2
    exports = load_exports(export_dir)

    if not live_state.get("available"):
        payload = {"ok": False, "reason": live_state.get("reason", "Live Typinator unavailable"), "export_dir": str(export_dir)}
        print(to_json(payload) if args.json else payload["reason"])
        return 2

    live_sets: dict[str, list[dict[str, str]]] = live_state["sets"]
    drift: list[dict[str, object]] = []
    for set_name, live_rules in sorted(live_sets.items()):
        export_rows = exports.get(set_name, exports.get(slug(set_name), {}))
        live_abbrs = {item["abbreviation"]: item for item in live_rules if item.get("abbreviation")}
        export_abbrs = set(export_rows)
        for abbr, item in sorted(live_abbrs.items()):
            if abbr not in export_abbrs:
                drift.append({"set": set_name, "abbreviation": abbr, "status": "missing_from_export"})
                continue
            if export_rows[abbr] != item["expansion"]:
                drift.append({"set": set_name, "abbreviation": abbr, "status": "expansion_differs"})
        for abbr in sorted(export_abbrs - set(live_abbrs)):
            drift.append({"set": set_name, "abbreviation": abbr, "status": "missing_from_live"})

    payload = {
        "ok": len(drift) == 0,
        "export_dir": str(export_dir),
        "live_set_count": len(live_sets),
        "export_set_count": len(exports),
        "drift": drift,
    }
    if args.json:
        print(to_json(payload))
    else:
        print(f"Compared {len(live_sets)} live set(s) to {len(exports)} export file(s).")
        if drift:
            print(f"Drift items: {len(drift)}")
            for item in drift[:100]:
                print(f"  - {item['set']} [{item['abbreviation']}]: {item['status']}")
        else:
            print("No live/export drift detected.")
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
