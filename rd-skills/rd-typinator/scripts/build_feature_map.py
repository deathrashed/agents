#!/usr/bin/env python3
"""Rebuild the Typinator feature map from a curated source manifest."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_MANIFEST = Path("/Users/rd/.config/typinator/.skill/references/typinator-feature-map-sources.json")
DEFAULT_OUT = Path("/Users/rd/.config/typinator/.skill/references/typinator-feature-map.md")
DEFAULT_DOC_ROOT = Path("/Users/rd/.config/typinator/Sets/Includes/Documentation")

SUPPRESSED_DOC_NAMES = {
    "README.md",
    ".DS_Store",
}

SUPPRESSED_PATH_PARTS = {
    "Generated",
}

SUPPRESSED_EXACT_PATHS = {
    Path("/Users/rd/.config/typinator/Sets/Includes/Documentation/Project/Archive/Exploit GitHub as infinite storage.md").resolve(),
}


def iter_local_docs(doc_root: Path) -> list[Path]:
    docs: list[Path] = []
    for path in sorted(doc_root.rglob("*")):
        if not path.is_file():
            continue
        if path.name in SUPPRESSED_DOC_NAMES:
            continue
        if path.suffix.lower() not in {".md", ".txt", ".pdf", ".csv"}:
            continue
        resolved = path.resolve()
        if resolved in SUPPRESSED_EXACT_PATHS:
            continue
        if any(part in SUPPRESSED_PATH_PARTS for part in resolved.parts):
            continue
        docs.append(resolved)
    return docs


def load_manifest(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def format_source(source: dict[str, str]) -> str:
    kind = source["kind"]
    path = source["path"]
    return f"- {kind.capitalize()}: `{path}`"


def classified_local_paths(manifest: dict[str, object]) -> set[Path]:
    paths: set[Path] = set()
    for area in manifest["feature_areas"]:
        for source in area["sources"]:
            if source["kind"].startswith("online"):
                continue
            paths.add(Path(source["path"]).expanduser().resolve())
    return paths


def discover_unmapped_docs(manifest: dict[str, object], doc_root: Path) -> list[Path]:
    known = classified_local_paths(manifest)
    docs = iter_local_docs(doc_root)
    return [path for path in docs if path not in known]


def build_markdown(manifest: dict[str, object], doc_root: Path) -> str:
    lines = [
        "# Typinator Feature Map",
        "",
        "Use this file as the navigation index for Typinator knowledge.",
        "",
        "Goal:",
        "- find the best source quickly",
        "- distinguish official behavior from local summaries",
        "- reduce repeated doc-hunting before editing or explaining Typinator features",
        "",
        "Conventions:",
        "- Prefer official Ergonis help-center articles for product behavior that may change.",
        "- Prefer local Ergonis-authored Guides and official Reference docs for deeper retained context.",
        "- Treat local derivative notes as convenience summaries, not the final authority.",
        "- Review the unmapped-docs section regularly so new local documentation is classified instead of drifting out of the map.",
    ]
    for area in manifest["feature_areas"]:
        lines.extend(["", f"## {area['title']}", "", "Best starting points:"])
        for source in area["sources"]:
            lines.append(format_source(source))
        lines.extend(["", "Use for:"])
        for item in area["use_for"]:
            lines.append(f"- {item}")

    unmapped = discover_unmapped_docs(manifest, doc_root)
    lines.extend(["", "## Unmapped Local Docs", ""])
    if unmapped:
        lines.append("These local documentation files exist under the Typinator documentation tree but are not yet assigned to a feature area in the curated manifest.")
        lines.append("")
        for path in unmapped:
            lines.append(f"- `{path}`")
    else:
        lines.append("All discovered local docs are currently mapped.")

    lines.extend(
        [
            "",
            "## Skill-Specific Operational Rule",
            "",
            "Before answering a non-trivial Typinator question or editing a complex Typinator artifact:",
            "- identify the feature area above",
            "- read at least one best local source",
            "- if behavior could have changed, check the linked official help-center article",
            "- prefer official Ergonis behavior over convenience notes when they conflict",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Curated source manifest JSON")
    ap.add_argument("--out", default=str(DEFAULT_OUT), help="Output markdown path")
    ap.add_argument("--doc-root", default=str(DEFAULT_DOC_ROOT), help="Local Typinator documentation root to scan for unmapped docs")
    ap.add_argument("--list-unmapped", action="store_true", help="Print unmapped local documentation files and exit")
    args = ap.parse_args()

    manifest_path = Path(args.manifest).expanduser().resolve()
    out_path = Path(args.out).expanduser().resolve()
    doc_root = Path(args.doc_root).expanduser().resolve()
    manifest = load_manifest(manifest_path)
    unmapped = discover_unmapped_docs(manifest, doc_root)

    if args.list_unmapped:
        for path in unmapped:
            print(path)
        return 0

    markdown = build_markdown(manifest, doc_root)
    out_path.write_text(markdown, encoding="utf-8")
    print(out_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
