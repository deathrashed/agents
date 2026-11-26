#!/usr/bin/env python3
"""Scaffold a reference-backed lookup rule using a script wrapper and source file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SCRIPT_TEMPLATE = """#!/usr/bin/env python3
#-- parameter: key

from pathlib import Path
import sys

SOURCE = Path({source!r})


def main() -> int:
    key = (sys.argv[1] if len(sys.argv) > 1 else "").strip().lower()
    if not SOURCE.exists():
        print("{{cancelExpansion=yes}}", end="")
        return 0
    for line in SOURCE.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if "\\t" not in line:
            continue
        lookup, value = line.split("\\t", 1)
        if lookup.strip().lower() == key:
            print(value, end="")
            return 0
    print("{{cancelExpansion=yes}}", end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--abbr", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--script-path", required=True)
    ap.add_argument("--source-file", required=True)
    args = ap.parse_args()

    includes_root = Path("/Users/rd/.config/typinator/Sets/Includes")
    csv_path = Path(args.csv).expanduser().resolve()
    script_rel = args.script_path.strip("/")
    source_rel = args.source_file.strip("/")
    script_abs = includes_root / script_rel
    source_abs = includes_root / source_rel

    script_abs.parent.mkdir(parents=True, exist_ok=True)
    source_abs.parent.mkdir(parents=True, exist_ok=True)
    if not source_abs.exists():
        source_abs.write_text("# key\\tvalue\nexample\tExample value\n", encoding="utf-8")
    if not script_abs.exists():
        script_abs.write_text(SCRIPT_TEMPLATE.format(source=str(source_abs)), encoding="utf-8")
        script_abs.chmod(0o755)

    placeholder = f"{{{{lookup=?{args.title}}}}}{{{script_rel} {{{{lookup}}}}}}"
    rows = []
    if csv_path.exists():
        with csv_path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
    if not rows:
        rows = [["abbreviation", "expansion"]]
    rows.append([args.abbr, placeholder])
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)
    print(f"Rule added to {csv_path}")
    print(f"Reference source scaffolded at {source_abs}")
    print(f"Lookup script scaffolded at {script_abs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
