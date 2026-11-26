#!/usr/bin/env python3
"""Upsert live Typinator rules safely through AppleScript, one rule at a time."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
import subprocess
import sys


def parse_args() -> argparse.Namespace:
    ap = argparse.ArgumentParser(
        description=(
            "Create or update live Typinator rules safely. "
            "Rules are applied one at a time to avoid brittle bulk AppleScript payloads."
        )
    )
    ap.add_argument("--set-name", required=True, help="Typinator rule set name to update")
    ap.add_argument(
        "--spec-json",
        help="Path to a JSON file containing a list of rule specs",
    )
    ap.add_argument(
        "--spec-csv",
        help="Path to a CSV file with columns: abbreviation, expansion, description",
    )
    ap.add_argument(
        "--text-root",
        help="Optional Includes/Text root to auto-generate rules from subfolders",
    )
    ap.add_argument(
        "--folders",
        nargs="+",
        help="Folder names under --text-root to include when auto-generating rules",
    )
    ap.add_argument(
        "--prefix",
        default="++",
        help="Default abbreviation prefix for auto-generated rules (default: ++)",
    )
    ap.add_argument(
        "--description-prefix",
        default="",
        help="Optional prefix added to generated descriptions",
    )
    ap.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the resolved specs without modifying Typinator",
    )
    ap.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable output",
    )
    return ap.parse_args()


def load_specs_from_json(path: Path) -> list[dict[str, str]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, list):
        raise ValueError("JSON spec must be a list of objects")
    return [normalize_spec(item) for item in payload]


def load_specs_from_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        rows = list(csv.DictReader(fh))
    return [normalize_spec(item) for item in rows]


def titleize(stem: str) -> str:
    specials = {"ai": "AI", "ides": "IDEs", "mp3tag": "Mp3tag", "macos": "macOS"}
    return " ".join(specials.get(word.lower(), word.capitalize()) for word in stem.replace("-", " ").split())


def build_specs_from_text_root(
    text_root: Path,
    folders: list[str],
    prefix: str,
    description_prefix: str,
) -> list[dict[str, str]]:
    folder_names = {
        "ai": "AI",
        "app": "App",
        "directory": "Directory",
        "dotfile": "Dotfile",
        "music": "Music",
        "obsidian": "Obsidian",
        "scripts": "Scripts",
        "system": "System",
        "util": "Utility",
    }
    overrides = {
        "directory/apfspace.txt": "++apfspace",
        "directory/audio.txt": "++audio",
        "system/config-quickref.txt": "++cfg quick",
        "directory/config.txt": "++config",
        "directory/eksternal.txt": "++eksternal",
        "directory/home.txt": "++home",
        "util/typinator-includes.txt": "++includes typinator",
        "directory/obsidian.txt": "++obsidian",
        "directory/scripts.txt": "++scripts",
        "directory/typinator.txt": "++typinator",
        "obsidian/music-vault.txt": "++vault music",
        "scripts/web.txt": "++web script",
        "ai/ai-profiles.txt": "++ai profiles",
        "ai/chatbot-personalization.txt": "++chatbot",
        "app/karabiner.txt": "++karabiner",
        "app/keyboard-maestro.txt": "++keyboard maestro",
        "app/leader-key.txt": "++leader key",
        "directory/applications.txt": "++applications",
        "directory/icons.txt": "++icons",
        "music/mp3tag-guide.txt": "++mp3tag guide",
        "music/mp3tag-mta.txt": "++mp3tag mta",
        "music/music-research.txt": "++music research",
        "music/music-tools.txt": "++music tools",
        "obsidian/apple-vault.txt": "++vault apple",
        "obsidian/dev-vault.txt": "++vault dev",
        "obsidian/main-vault.txt": "++vault main",
        "obsidian/scripts-vault.txt": "++vault scripts",
        "obsidian/workspace-vault.txt": "++vault workspace",
        "scripts/apps.txt": "++apps script",
        "scripts/dev.txt": "++dev script",
        "scripts/media.txt": "++media script",
        "scripts/system.txt": "++system script",
        "scripts/utilities.txt": "++utilities script",
        "system/macos-toolkit.txt": "++mac toolkit",
        "system/rileys-environment.txt": "++rileys environment",
        "system/system-profile.txt": "++system profile",
        "util/gupload-toolkit.txt": "++gupload",
        "util/mackup.txt": "++mackup",
        "util/scripts-hub-import.txt": "++script hub",
        "util/shell.txt": "++shell util",
    }
    specs: list[dict[str, str]] = []
    seen_abbrs: set[str] = set()

    for folder in folders:
        for path in sorted((text_root / folder).glob("*.txt")):
            rel = path.relative_to(text_root).as_posix()
            stem = path.stem
            abbreviation = overrides.get(rel, prefix + stem.replace("-", " "))
            if abbreviation in seen_abbrs:
                raise ValueError(f"duplicate abbreviation generated: {abbreviation}")
            seen_abbrs.add(abbreviation)
            descr = f"{description_prefix}{folder_names.get(folder, folder.capitalize())} - {titleize(stem)}".strip()
            specs.append(
                {
                    "abbreviation": abbreviation,
                    "expansion": "{Text/" + text_root.name + "/" + rel + "}",
                    "description": descr,
                    "expansion_type": "plain text",
                    "whole_word": False,
                    "case_handling": "case does not matter",
                }
            )
    return specs


def normalize_spec(item: dict[str, object]) -> dict[str, str]:
    abbreviation = str(item.get("abbreviation", "")).strip()
    expansion = str(item.get("expansion", ""))
    description = str(item.get("description", "")).strip()
    expansion_type = str(item.get("expansion_type", "plain text")).strip() or "plain text"
    whole_word = bool(item.get("whole_word", False))
    case_handling = str(item.get("case_handling", "case does not matter")).strip() or "case does not matter"
    if not abbreviation:
        raise ValueError("rule spec is missing abbreviation")
    return {
        "abbreviation": abbreviation,
        "expansion": expansion,
        "description": description,
        "expansion_type": expansion_type,
        "whole_word": "true" if whole_word else "false",
        "case_handling": case_handling,
    }


def esc(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def run_applescript(source: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["osascript", "-"], input=source, text=True, capture_output=True)


def upsert_rule(set_name: str, spec: dict[str, str]) -> None:
    abbreviation = esc(spec["abbreviation"])
    expansion = esc(spec["expansion"])
    description = esc(spec["description"])
    expansion_type = esc(spec["expansion_type"])
    case_handling = esc(spec["case_handling"])
    whole_word = spec["whole_word"]

    lines = [
        'tell application "Typinator"',
        f'  set targetSet to first rule set whose name is "{esc(set_name)}"',
        f'  set matchedRules to (every rule of targetSet whose abbreviation is "{abbreviation}")',
        "  if (count of matchedRules) > 0 then",
        "    set targetRule to item 1 of matchedRules",
        "  else",
        f'    set targetRule to make new rule at end of rules of targetSet with properties {{abbreviation:"{abbreviation}"}}',
        "  end if",
        f'  set expansion type of targetRule to {expansion_type}',
        f'  set plain expansion of targetRule to "{expansion}"',
    ]
    if spec["expansion_type"] != "plain text":
        lines.append(f'  set formatted expansion of targetRule to "{expansion}"')
    lines.extend(
        [
            f"  set whole word of targetRule to {whole_word}",
            f"  set case handling of targetRule to {case_handling}",
            f'  set description of targetRule to "{description}"',
            "end tell",
        ]
    )
    result = run_applescript("\n".join(lines) + "\n")
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown AppleScript error"
        raise RuntimeError(f"failed to upsert {spec['abbreviation']}: {message}")


def read_rule_count(set_name: str) -> int:
    result = run_applescript(
        "\n".join(
            [
                'tell application "Typinator"',
                f'  set targetSet to first rule set whose name is "{esc(set_name)}"',
                "  return count of rules of targetSet",
                "end tell",
                "",
            ]
        )
    )
    if result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip() or "unknown AppleScript error"
        raise RuntimeError(f"failed to read Typinator set count: {message}")
    return int((result.stdout or "0").strip())


def load_specs(args: argparse.Namespace) -> list[dict[str, str]]:
    chosen = [bool(args.spec_json), bool(args.spec_csv), bool(args.text_root)]
    if sum(chosen) != 1:
        raise ValueError("choose exactly one of --spec-json, --spec-csv, or --text-root")
    if args.spec_json:
        return load_specs_from_json(Path(args.spec_json).expanduser().resolve())
    if args.spec_csv:
        return load_specs_from_csv(Path(args.spec_csv).expanduser().resolve())
    if not args.folders:
        raise ValueError("--folders is required when using --text-root")
    return build_specs_from_text_root(
        Path(args.text_root).expanduser().resolve(),
        args.folders,
        args.prefix,
        args.description_prefix,
    )


def main() -> int:
    args = parse_args()
    try:
        specs = load_specs(args)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    payload = {
        "set_name": args.set_name,
        "rule_count": len(specs),
        "specs": specs,
    }
    if args.dry_run:
        if args.json:
            print(json.dumps(payload, indent=2))
        else:
            print(f"Dry run: {args.set_name} <- {len(specs)} rule(s)")
            for spec in specs:
                print(f"  - {spec['abbreviation']}: {spec['expansion']}")
        return 0

    try:
        for spec in specs:
            upsert_rule(args.set_name, spec)
        live_count = read_rule_count(args.set_name)
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    result_payload = {
        "ok": True,
        "set_name": args.set_name,
        "applied_rules": len(specs),
        "live_rule_count": live_count,
    }
    if args.json:
        print(json.dumps(result_payload, indent=2))
    else:
        print(f"Applied {len(specs)} rule(s) to Typinator set '{args.set_name}'.")
        print(f"Live rule count: {live_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
