#!/usr/bin/env python3
"""Scaffold a script-backed Typinator rule and companion script file."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path


SCRIPT_TEMPLATES = {
    "python": "#!/usr/bin/env python3\n#-- parameter: input\n\nimport sys\n\n\ndef main() -> int:\n    value = sys.argv[1] if len(sys.argv) > 1 else \"\"\n    print(value, end=\"\")\n    return 0\n\n\nif __name__ == \"__main__\":\n    raise SystemExit(main())\n",
    "shell": "#!/usr/bin/env bash\n#-- parameter: input\nset -euo pipefail\nprintf '%s' \"${1-}\"\n",
}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True, help="Target CSV set")
    ap.add_argument("--abbr", required=True, help="New abbreviation")
    ap.add_argument("--script-path", required=True, help="Path under Includes root, e.g. Scripts/Tools/my_rule.py")
    ap.add_argument("--language", choices=sorted(SCRIPT_TEMPLATES), default="python")
    ap.add_argument("--parameter", default="input", help="Single Typinator parameter name")
    args = ap.parse_args()

    csv_path = Path(args.csv).expanduser().resolve()
    script_rel = args.script_path.strip("/")
    script_abs = csv_path.parents[3] / script_rel if "Includes" in str(csv_path) else Path("/Users/rd/.config/typinator/Sets/Includes") / script_rel
    script_abs.parent.mkdir(parents=True, exist_ok=True)
    if not script_abs.exists():
        script_abs.write_text(SCRIPT_TEMPLATES[args.language], encoding="utf-8")
        script_abs.chmod(0o755)

    placeholder = f"{{{script_rel} {{{{?{args.parameter}}}}}}}"
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
    print(f"Script scaffolded at {script_abs}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
