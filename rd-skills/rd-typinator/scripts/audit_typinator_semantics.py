#!/usr/bin/env python3
"""Run deeper semantic checks for Typinator exports and Includes resources."""

from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path
import sys

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

from _typinator_common import detect_menu_sizes, list_csv_files, normalized_expansion, parse_rows, referenced_script_paths, similarity, to_json  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--includes-root", default="/Users/rd/.config/typinator/Sets/Includes")
    ap.add_argument("--export-dir", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    includes_root = Path(args.includes_root).expanduser().resolve()
    export_dir = Path(args.export_dir).expanduser().resolve() if args.export_dir else includes_root / "Exported"
    csv_files = list_csv_files(export_dir)

    exact_duplicates: dict[str, list[dict[str, str]]] = defaultdict(list)
    oversized_menus: list[dict[str, object]] = []
    near_duplicates: list[dict[str, object]] = []
    referenced_scripts: set[str] = set()
    expansions: list[tuple[str, str, str]] = []

    for csv_file in csv_files:
        for row in parse_rows(csv_file):
            if len(row) < 2 or not row[0].strip():
                continue
            abbr = row[0].strip()
            exp = row[1]
            expansions.append((csv_file.name, abbr, exp))
            exact_duplicates[normalized_expansion(exp)].append({"file": csv_file.name, "abbreviation": abbr})
            referenced_scripts.update(referenced_script_paths(exp))
            for size in detect_menu_sizes(exp):
                if size >= 15:
                    oversized_menus.append({"file": csv_file.name, "abbreviation": abbr, "options": size})

    for index, (file_a, abbr_a, exp_a) in enumerate(expansions):
        norm_a = normalized_expansion(exp_a)
        if not norm_a or len(norm_a) < 30:
            continue
        for file_b, abbr_b, exp_b in expansions[index + 1 :]:
            norm_b = normalized_expansion(exp_b)
            if not norm_b or norm_a == norm_b:
                continue
            score = similarity(norm_a, norm_b)
            if score >= 0.92:
                near_duplicates.append(
                    {
                        "score": round(score, 3),
                        "left": f"{file_a}:{abbr_a}",
                        "right": f"{file_b}:{abbr_b}",
                    }
                )

    payload = {
        "export_dir": str(export_dir),
        "exact_duplicate_groups": [
            {"count": len(entries), "entries": entries[:10]}
            for key, entries in exact_duplicates.items()
            if len(entries) > 1
        ],
        "near_duplicates": sorted(near_duplicates, key=lambda item: (-item["score"], item["left"], item["right"]))[:100],
        "oversized_menus": sorted(oversized_menus, key=lambda item: (-item["options"], item["file"], item["abbreviation"]))[:100],
        "referenced_script_count": len(referenced_scripts),
    }

    if args.json:
        print(to_json(payload))
    else:
        print(f"Semantic audit checked {len(csv_files)} export file(s).")
        print(f"Exact duplicate groups: {len(payload['exact_duplicate_groups'])}")
        print(f"Near duplicate pairs: {len(payload['near_duplicates'])}")
        print(f"Oversized menus: {len(payload['oversized_menus'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
