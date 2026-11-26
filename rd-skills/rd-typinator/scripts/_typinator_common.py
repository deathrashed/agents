#!/usr/bin/env python3
"""Shared helpers for Typinator skill maintenance scripts."""

from __future__ import annotations

from dataclasses import dataclass
import csv
import difflib
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
from typing import Iterable

TRANSLATIONS = {
    "\u2028": "\n",
    "\u2029": "\n",
    "\ufeff": "",
    "\u200b": "",
    "\u200c": "",
    "\u200d": "",
}

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

SYNTAX_PATTERNS = [
    (re.compile(r"\{Shell/"), "malformed_shell_marker", "malformed shell marker ({Shell/)"),
    (re.compile(r"\{form:[^}]+\}"), "foreign_form_placeholder", "non-native placeholder ({form:...})"),
    (re.compile(r"<Skip if null>"), "skip_if_null_artifact", "artifact (<Skip if null>)"),
]

INTERACTIVE_PATTERNS = [
    re.compile(r"\bdisplay dialog\b", re.IGNORECASE),
    re.compile(r"\bdisplay alert\b", re.IGNORECASE),
    re.compile(r"\bchoose from list\b", re.IGNORECASE),
    re.compile(r"\bchoose file\b", re.IGNORECASE),
    re.compile(r"\bchoose folder\b", re.IGNORECASE),
]

SCRIPT_EXTS = {".applescript", ".scpt", ".sh", ".py", ".rb", ".swift", ".js"}
FORM_PATTERN = re.compile(r"\{form:([^}]+)\}")
FORBIDDEN_SCRIPT_NAME_CHARS = {"|", "{", "}"}
MENU_PLACEHOLDER_RE = re.compile(r"\{\{\?[^{}()]+\((.*?)\)\}\}")
SCRIPT_REF_RE = re.compile(r"Scripts/[^\s`}|]+")


@dataclass
class Finding:
    severity: str
    rule_id: str
    message: str
    file: str
    row: int | None = None
    abbreviation: str | None = None
    fixable: bool = False
    suggestion: str | None = None

    def to_dict(self) -> dict[str, object]:
        return {
            "severity": self.severity,
            "rule_id": self.rule_id,
            "message": self.message,
            "file": self.file,
            "row": self.row,
            "abbreviation": self.abbreviation,
            "fixable": self.fixable,
            "suggestion": self.suggestion,
        }


@dataclass
class FileScan:
    total_rows: int
    data_rows: int
    issue_counts: dict[str, int]
    duplicate_groups: dict[str, list[int]]
    has_header: bool


def read_csv_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return [list(row) for row in csv.reader(fh)]


def write_csv_rows(path: Path, rows: Iterable[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        csv.writer(fh).writerows(rows)


def parse_rows(path: Path) -> list[list[str]]:
    return read_csv_rows(path)


def roundtrip_equal(rows: list[list[str]]) -> bool:
    buf = io.StringIO()
    writer = csv.writer(buf)
    writer.writerows(rows)
    buf.seek(0)
    parsed = [list(row) for row in csv.reader(io.StringIO(buf.getvalue()))]
    return parsed == rows


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


def convert_form_placeholders(text: str) -> str:
    return apply_text_fixes(text, {"convert_form_placeholders", "remove_skip_if_null"})


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


def load_manifest_rows(path: Path | None) -> list[dict[str, str]]:
    if path is None or not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def manifest_alias_map(path: Path | None) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for row in load_manifest_rows(path):
        alias = (row.get("alias_path") or "").strip()
        canonical = (row.get("canonical_path") or "").strip()
        status = (row.get("status") or "").strip().lower()
        if alias and canonical and status in {"deprecated", "alias"}:
            mapping[alias] = canonical
    return mapping


def load_manifest_aliases(path: Path | None) -> set[str]:
    return set(manifest_alias_map(path))


def find_script_references(text: str, includes_root: Path) -> tuple[list[str], list[str]]:
    resolved: list[str] = []
    unresolved: list[str] = []
    i = 0
    while True:
        i = text.find("Scripts/", i)
        if i == -1:
            break
        tail = text[i:]
        found = None
        for end in range(len(tail), len("Scripts/") - 1, -1):
            candidate = tail[:end].rstrip(" \t\r\n`}|")
            if not candidate.startswith("Scripts/"):
                continue
            if (includes_root / candidate).exists():
                found = candidate
                break
        if found is None:
            snippet = tail[:120].splitlines()[0]
            unresolved.append(snippet)
            i += len("Scripts/")
            continue
        resolved.append(found)
        i += len(found)
    return resolved, unresolved


def referenced_script_paths(text: str) -> set[str]:
    return set(SCRIPT_REF_RE.findall(text))


def interactive_script_hits(path: Path) -> list[str]:
    try:
        src = path.read_text(errors="ignore")
    except Exception:
        return []
    hits = [pat.pattern for pat in INTERACTIVE_PATTERNS if pat.search(src)]
    return hits


def interactive_allowed(path: Path) -> str:
    hits = interactive_script_hits(path)
    return "no" if hits else "yes"


def iter_script_files(scripts_root: Path) -> Iterable[Path]:
    for p in sorted(scripts_root.rglob("*")):
        if p.is_file() and p.suffix.lower() in SCRIPT_EXTS:
            yield p


def newline_style(path: Path) -> str:
    raw = path.read_bytes()
    has_crlf = b"\r\n" in raw
    has_lf = b"\n" in raw
    if has_crlf and has_lf:
        mixed = b"\r\n" in raw and b"\n" in raw.replace(b"\r\n", b"")
        if mixed:
            return "mixed"
        return "crlf"
    if has_lf:
        return "lf"
    return "none"


def detect_menu_sizes(text: str) -> list[int]:
    sizes: list[int] = []
    for match in MENU_PLACEHOLDER_RE.finditer(text):
        options = match.group(1)
        if not options.strip():
            continue
        sizes.append(options.count("|") + 1)
    return sizes


def normalized_expansion(text: str) -> str:
    out = apply_text_fixes(text, set(FIX_KEYS))
    out = re.sub(r"\s+", " ", out).strip().lower()
    return out


def short_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]


def similarity(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, a, b).ratio()


def warn_exported_directory_case(includes_root: Path) -> list[str]:
    msgs: list[str] = []
    d1 = includes_root / "Exported"
    d2 = includes_root / "exported"
    if d1.exists() and d2.exists():
        msgs.append("Both Includes/Exported and Includes/exported exist. Consolidate to one runtime source.")
    return msgs


def script_filename_conflicts(scripts_root: Path) -> list[str]:
    hits: list[str] = []
    if not scripts_root.exists():
        return hits
    for script_file in iter_script_files(scripts_root):
        rel = script_file.relative_to(scripts_root).as_posix()
        if any(ch in rel for ch in FORBIDDEN_SCRIPT_NAME_CHARS):
            hits.append(rel)
    return hits


def scan_file(rows: list[list[str]]) -> FileScan:
    issue_counts = {k: 0 for k in FIX_KEYS}
    has_header = bool(
        rows
        and len(rows[0]) >= 2
        and rows[0][0].strip().lower() == "abbreviation"
        and rows[0][1].strip().lower() == "expansion"
    )
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


def evaluate_csv_file(
    csv_file: Path,
    includes_root: Path,
    *,
    alias_map: dict[str, str] | None = None,
    max_abbr_words: int | None = None,
) -> list[Finding]:
    findings: list[Finding] = []
    alias_map = alias_map or {}
    style = newline_style(csv_file)
    if style == "mixed":
        findings.append(
            Finding("warning", "mixed_newlines", "mixed newline style", csv_file.name, suggestion="Normalize to a single newline style.")
        )

    try:
        rows = parse_rows(csv_file)
    except Exception as exc:
        return [Finding("error", "csv_parse_error", f"CSV parse error: {exc}", csv_file.name)]

    if not roundtrip_equal(rows):
        findings.append(Finding("error", "csv_roundtrip_mismatch", "CSV round-trip structural mismatch", csv_file.name))

    abbr_to_rows: dict[str, list[int]] = {}
    for idx, row in enumerate(rows, start=1):
        if not row:
            continue
        abbr = row[0].strip() if row else ""
        if abbr:
            abbr_to_rows.setdefault(abbr, []).append(idx)
            if max_abbr_words is not None and len(abbr.split()) > max_abbr_words:
                findings.append(
                    Finding(
                        "error",
                        "abbreviation_policy",
                        f"abbreviation exceeds max words ({max_abbr_words})",
                        csv_file.name,
                        row=idx,
                        abbreviation=abbr,
                    )
                )

        exp = row[1] if len(row) >= 2 else ""
        for _, rule_id, label in SYNTAX_PATTERNS:
            if rule_id == "malformed_shell_marker" and "{Shell/" in exp:
                findings.append(
                    Finding(
                        "error",
                        rule_id,
                        label,
                        csv_file.name,
                        row=idx,
                        abbreviation=abbr,
                        fixable=True,
                        suggestion="Rewrite {Shell/ to {/Shell.",
                    )
                )
            if rule_id == "foreign_form_placeholder" and FORM_PATTERN.search(exp):
                findings.append(
                    Finding(
                        "error",
                        rule_id,
                        label,
                        csv_file.name,
                        row=idx,
                        abbreviation=abbr,
                        fixable=True,
                        suggestion="Rewrite {form:name} to {{?name}}.",
                    )
                )
            if rule_id == "skip_if_null_artifact" and "<Skip if null>" in exp:
                findings.append(
                    Finding(
                        "error",
                        rule_id,
                        label,
                        csv_file.name,
                        row=idx,
                        abbreviation=abbr,
                        fixable=True,
                        suggestion="Remove the artifact token.",
                    )
                )

        refs, unresolved = find_script_references(exp, includes_root)
        for snippet in unresolved:
            findings.append(
                Finding("error", "unresolved_script_reference", f"unresolved script reference near: {snippet!r}", csv_file.name, row=idx, abbreviation=abbr)
            )
        for ref in refs:
            p = includes_root / ref
            if p.is_symlink():
                findings.append(
                    Finding("error", "symlink_script_reference", f"script ref points to symlink alias: {ref}", csv_file.name, row=idx, abbreviation=abbr)
                )
            if ref in alias_map:
                findings.append(
                    Finding(
                        "error",
                        "deprecated_script_alias",
                        f"script ref points to deprecated alias: {ref}",
                        csv_file.name,
                        row=idx,
                        abbreviation=abbr,
                        fixable=True,
                        suggestion=f"Rewrite to canonical path {alias_map[ref]}",
                    )
                )
            interactive_hits = interactive_script_hits(p)
            if interactive_hits:
                findings.append(
                    Finding(
                        "warning",
                        "interactive_script_pattern",
                        f"interactive script pattern in {ref}: {', '.join(sorted(set(interactive_hits)))}",
                        csv_file.name,
                        row=idx,
                        abbreviation=abbr,
                    )
                )
        for size in detect_menu_sizes(exp):
            if size >= 20:
                findings.append(
                    Finding(
                        "warning",
                        "oversized_menu",
                        f"menu has {size} options; consider a grouped picker",
                        csv_file.name,
                        row=idx,
                        abbreviation=abbr,
                    )
                )

    duplicates = {k: v for k, v in abbr_to_rows.items() if len(v) > 1}
    for abbr, idxs in sorted(duplicates.items()):
        findings.append(
            Finding(
                "error",
                "duplicate_abbreviation",
                f"duplicate abbreviation appears on rows {', '.join(map(str, idxs))}",
                csv_file.name,
                row=idxs[0],
                abbreviation=abbr,
            )
        )

    return findings


def apply_manifest_rewrites(text: str, alias_map: dict[str, str]) -> tuple[str, list[tuple[str, str]]]:
    updated = text
    rewrites: list[tuple[str, str]] = []
    for alias, canonical in sorted(alias_map.items(), key=lambda item: len(item[0]), reverse=True):
        if alias in updated:
            updated = updated.replace(alias, canonical)
            rewrites.append((alias, canonical))
    return updated, rewrites


def list_csv_files(export_dir: Path) -> list[Path]:
    if not export_dir.exists():
        return []
    return sorted(export_dir.glob("*.csv"))


def osascript_available() -> bool:
    return subprocess.run(["/usr/bin/which", "osascript"], capture_output=True, text=True, check=False).returncode == 0


def dump_live_typinator_state() -> dict[str, object]:
    script = r'''
set text item delimiters to linefeed
tell application "Typinator"
	set outputLines to {}
	repeat with rs in rule sets
		set rsName to name of rs
		copy ("SET|" & rsName) to end of outputLines
		try
			repeat with r in rules of rs
				set ruleName to ""
				try
					set ruleName to name of r
				end try
				set abbrText to ""
				try
					set abbrText to abbreviation of r
				end try
				set expansionText to ""
				try
					set expansionText to expansion of r
				end try
				set commentText to ""
				try
					set commentText to comment of r
				end try
				set payload to abbrText & "||" & ruleName & "||" & expansionText & "||" & commentText
				copy ("RULE|" & rsName & "|" & payload) to end of outputLines
			end repeat
		end try
	end repeat
	return outputLines as text
end tell
'''
    if not osascript_available():
        return {"available": False, "reason": "osascript not available", "sets": []}
    result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)
    if result.returncode != 0:
        return {"available": False, "reason": result.stderr.strip() or "osascript failed", "sets": []}

    sets: dict[str, list[dict[str, str]]] = {}
    for line in result.stdout.splitlines():
        if line.startswith("SET|"):
            sets.setdefault(line.split("|", 1)[1], [])
            continue
        if not line.startswith("RULE|"):
            continue
        _, set_name, payload = line.split("|", 2)
        abbr, rule_name, expansion, comment = (payload.split("||", 3) + ["", "", "", ""])[:4]
        sets.setdefault(set_name, []).append(
            {
                "abbreviation": abbr,
                "rule_name": rule_name,
                "expansion": expansion,
                "comment": comment,
            }
        )
    return {"available": True, "sets": sets}


def summarize_live_state(live_state: dict[str, object]) -> dict[str, object]:
    if not live_state.get("available"):
        return {"available": False, "set_count": 0, "rule_count": 0}
    sets = live_state.get("sets", {})
    rule_count = sum(len(rules) for rules in sets.values())
    return {"available": True, "set_count": len(sets), "rule_count": rule_count}


def to_json(data: object) -> str:
    return json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True)
