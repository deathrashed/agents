#!/usr/bin/env python3
"""Build plain-text prompt reference CSVs from Typinator export CSVs.

These generated files are safe for picker-style lookup menus because they do not
contain live Typinator form syntax. Input fields are converted to readable
placeholders like ``[Topic]`` and display-only dialog chrome is removed.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
import re


ROOT = Path("/Users/rd/.config/typinator/Sets/Includes/Reference/CSV")
SOURCES = {
    "Prompts.csv": "Prompts Plain.csv",
    "Prompts-Enhanced.csv": "Prompts-Enhanced Plain.csv",
    "User Prompts.csv": "User Prompts Plain.csv",
}

DISPLAY_BLOCK_RE = re.compile(r"\{\{\?\*.*?\*\}\}|\{\{\?--\}\}|\{\{\?_.*?_\}\}", re.DOTALL)
DECL_RE = re.compile(r"\{\{([A-Za-z0-9_]+)=\?(.*?)\}\}", re.DOTALL)
COND_BLOCK_RE = re.compile(r"\{\{\?([A-Za-z0-9_]+)\[(.*?)\]\}\}", re.DOTALL)
COND_PAREN_RE = re.compile(r"\{\{\?([A-Za-z0-9_]+)\((.*?)\)\}\}", re.DOTALL)
BARE_INPUT_RE = re.compile(r"\{\{\?(?![_*~-])(.+?)\}\}", re.DOTALL)
VAR_RE = re.compile(r"\{\{([A-Za-z0-9_]+)\}\}")
CLIP_RE = re.compile(r"\{clip\}")
SPACEY_LINES_RE = re.compile(r"\n{3,}")
NON_ALNUM_RE = re.compile(r"[^A-Za-z0-9 ]+")


@dataclass
class CleanResult:
    text: str
    is_script: bool = False


def normalize_label(raw: str) -> str:
    label = raw.strip()
    for sep in ("<", "(", "//", "/#", "#", ":"):
        if sep in label:
            label = label.split(sep, 1)[0].strip()
    label = label.strip(" -*_")
    label = re.sub(r"\s+", " ", label)
    if not label or not re.search(r"[A-Za-z0-9]", label):
        return "Input"
    return label


def placeholder(label: str) -> str:
    return f"[{label}]"


def split_choice_branches(spec: str) -> list[str]:
    parts: list[str] = []
    current: list[str] = []
    depth = 0
    for ch in spec:
        if ch == "|" and depth == 0:
            parts.append("".join(current))
            current = []
            continue
        if ch in "([<":
            depth += 1
        elif ch in ")]>" and depth > 0:
            depth -= 1
        current.append(ch)
    parts.append("".join(current))
    return parts


def extract_branch_texts(spec: str) -> list[str]:
    texts: list[str] = []
    for branch in split_choice_branches(spec):
        if ":" not in branch:
            return []
        _, value = branch.split(":", 1)
        value = value.strip()
        if value:
            texts.append(value)
    return texts


def clean_prompt(text: str) -> CleanResult:
    stripped = text.strip()
    if stripped.startswith("{Scripts/") or stripped.startswith("{/Shell") or stripped.startswith("{/Python"):
        return CleanResult(text="", is_script=True)

    labels: dict[str, str] = {}
    working = DISPLAY_BLOCK_RE.sub("", text)

    def decl_repl(match: re.Match[str]) -> str:
        var_name = match.group(1)
        labels[var_name] = normalize_label(match.group(2))
        return ""

    working = DECL_RE.sub(decl_repl, working)

    for _ in range(8):
        previous = working

        def cond_block_repl(match: re.Match[str]) -> str:
            inner = match.group(2)
            return inner

        working = COND_BLOCK_RE.sub(cond_block_repl, working)

        def cond_paren_repl(match: re.Match[str]) -> str:
            var_name = match.group(1)
            branch_texts = extract_branch_texts(match.group(2))
            if len(branch_texts) == 1:
                return branch_texts[0]
            return placeholder(labels.get(var_name, normalize_label(var_name)))

        working = COND_PAREN_RE.sub(cond_paren_repl, working)

        def bare_input_repl(match: re.Match[str]) -> str:
            return placeholder(normalize_label(match.group(1)))

        working = BARE_INPUT_RE.sub(bare_input_repl, working)

        def var_repl(match: re.Match[str]) -> str:
            return placeholder(labels.get(match.group(1), normalize_label(match.group(1))))

        working = VAR_RE.sub(var_repl, working)
        working = CLIP_RE.sub("[Clipboard]", working)

        if working == previous:
            break

    working = working.replace('""', '"')
    working = working.replace("\u2028", "\n")
    working = re.sub(r"[ \t]+\n", "\n", working)
    working = re.sub(r"\n[ \t]+", "\n", working)
    working = SPACEY_LINES_RE.sub("\n\n", working)
    working = working.strip()
    return CleanResult(text=working, is_script=False)


def build_plain_sources() -> None:
    for source_name, output_name in SOURCES.items():
        source_path = ROOT / source_name
        output_path = ROOT / output_name
        rows_out: list[list[str]] = []

        with source_path.open(encoding="utf-8", newline="") as handle:
            for row in csv.reader(handle):
                if len(row) < 2 or not row[0].strip():
                    continue
                cleaned = clean_prompt(row[1])
                if cleaned.is_script or not cleaned.text:
                    continue
                rows_out.append([row[0], cleaned.text])

        with output_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerows(rows_out)

        print(f"Wrote {output_path} ({len(rows_out)} rows)")


if __name__ == "__main__":
    build_plain_sources()
