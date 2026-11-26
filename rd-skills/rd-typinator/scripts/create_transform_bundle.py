#!/usr/bin/env python3
"""Create a small transform bundle: script, CSV row, and helper note."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SCRIPT_TEMPLATE = """#!/usr/bin/env python3
#-- parameter: text

import sys


def main() -> int:
    text = sys.argv[1] if len(sys.argv) > 1 else ""
    print({transform}, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--abbr", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--script-path", required=True)
    ap.add_argument("--mode", choices=["upper", "lower", "title", "strip"], default="upper")
    args = ap.parse_args()

    transforms = {
        "upper": "text.upper()",
        "lower": "text.lower()",
        "title": "text.title()",
        "strip": "text.strip()",
    }

    includes_root = Path("/Users/rd/.config/typinator/Sets/Includes")
    csv_path = Path(args.csv).expanduser().resolve()
    script_rel = args.script_path.strip("/")
    script_abs = includes_root / script_rel
    script_abs.parent.mkdir(parents=True, exist_ok=True)
    if not script_abs.exists():
        script_abs.write_text(SCRIPT_TEMPLATE.format(transform=transforms[args.mode]), encoding="utf-8")
        script_abs.chmod(0o755)

    placeholder = f"{{{{input=?{args.name}}}}}{{{script_rel} {{{{input}}}}}}"
    rows = []
    if csv_path.exists():
        with csv_path.open(encoding="utf-8", newline="") as fh:
            rows = list(csv.reader(fh))
    if not rows:
        rows = [["abbreviation", "expansion"]]
    rows.append([args.abbr, placeholder])
    with csv_path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)
    print(f"Transform bundle added to {csv_path}")
    print(f"Script scaffolded at {script_abs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
