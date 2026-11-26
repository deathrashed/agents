#!/usr/bin/env python3
"""Check a draft Last.fm wiki for common formatting violations.

This is a deterministic syntax/style linter, NOT a factual verifier or a
Last.fm server-side parser. Python 3 standard library only.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

TOKEN = re.compile(r"\[(?P<close>/)?(?P<name>[A-Za-z]+)(?P<attrs>[^\]\r\n]*)\]")
LINK = re.compile(r"(?i)(?:https?://|www\.)[^\s\]<>()\"']+")
MARKDOWN_LINK = re.compile(r"\[[^\]\n]+\]\([^\)\n]+\)")
MARKDOWN_HEADING = re.compile(r"(?m)^\s*#{1,6}\s+\S")
MARKDOWN_LIST = re.compile(r"(?m)^\s*(?:[-*+]\s+|\d+\.\s+)")
VALID_NAMES = {"b", "i", "url", "ulist", "li", "user", "artist", "album", "track", "tag", "event"}
EMPTY_UNSAFE = {"artist", "album", "track", "tag", "user", "event", "url"}


def internal_lastfm(url: str) -> bool:
    """Allow only HTTP(S) URLs whose hostname is last.fm or a subdomain."""
    candidate = "https://" + url if url.lower().startswith("www.") else url
    parsed = urlparse(candidate)
    host = (parsed.hostname or "").lower().rstrip(".")
    return parsed.scheme in ("http", "https") and (
        host == "last.fm" or host.endswith(".last.fm")
    )


def validate(text: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    stack: list[tuple[str, int, int, str]] = []  # name, line, index, attrs

    if not text.strip():
        return ["Draft is empty."], warnings

    for match in TOKEN.finditer(text):
        name = match.group("name").lower()
        attrs = match.group("attrs")
        closing = bool(match.group("close"))
        line = text.count("\n", 0, match.start()) + 1

        if name not in VALID_NAMES:
            errors.append(f"Line {line}: unsupported BBCode tag [{name}].")
            continue

        if closing:
            if attrs.strip():
                errors.append(f"Line {line}: closing [/{name}] cannot have attributes.")
            if not stack:
                errors.append(f"Line {line}: unexpected closing tag [/{name}].")
                continue
            open_name, open_line, start, open_attrs = stack[-1]
            if name != open_name:
                errors.append(
                    f"Line {line}: expected [/{open_name}] for the tag opened "
                    f"on line {open_line}, found [/{name}]."
                )
                continue
            stack.pop()
            content = text[start:match.start()].strip()
            if name in EMPTY_UNSAFE and not content:
                errors.append(f"Line {line}: [{name}] content is empty.")
            if name == "url" and not open_attrs and content and not internal_lastfm(content):
                errors.append(f"Line {open_line}: raw [url] must link to last.fm only.")
            continue

        if name in ("album", "track"):
            attr_match = re.fullmatch(r"\s+artist\s*=\s*(.+?)\s*", attrs, re.I)
            if not attr_match or not attr_match.group(1).strip():
                errors.append(f"Line {line}: [{name}] must include artist=Artist Name.")
        elif name == "event":
            if not re.fullmatch(r"=\d+", attrs):
                errors.append(f"Line {line}: [event] requires a numeric event ID.")
        elif name == "url":
            if attrs:
                if not attrs.startswith("=") or not internal_lastfm(attrs[1:].strip()):
                    errors.append(f"Line {line}: [url=...] must target last.fm only.")
        elif attrs:
            errors.append(f"Line {line}: [{name}] does not take attributes.")

        if name == "ulist":
            warnings.append(f"Line {line}: lists are supported by Last.fm but discouraged by this skill's prose style.")
        if name == "li" and not any(item[0] == "ulist" for item in stack):
            errors.append(f"Line {line}: [li] must be inside [ulist].")
        stack.append((name, line, match.end(), attrs))

    for name, line, _start, _attrs in stack:
        errors.append(f"Line {line}: unclosed [{name}] tag.")

    for match in LINK.finditer(text):
        raw_url = match.group(0).rstrip(".,;!?")
        if not internal_lastfm(raw_url):
            line = text.count("\n", 0, match.start()) + 1
            errors.append(f"Line {line}: external link is forbidden in published wikis: {raw_url}")

    if MARKDOWN_LINK.search(text):
        errors.append("Markdown link syntax found; use Last.fm BBCode instead.")
    if MARKDOWN_HEADING.search(text):
        errors.append("Markdown heading found; use [b]Heading[/b] or plain prose.")
    if MARKDOWN_LIST.search(text):
        errors.append("Markdown list found; finished entries must use narrative paragraphs.")
    if "**" in text:
        errors.append("Markdown **bold** syntax found; use [b]...[/b].")
    if "```" in text:
        errors.append("Markdown code fence found; output final BBCode as plain text.")

    return list(dict.fromkeys(errors)), list(dict.fromkeys(warnings))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", nargs="?", help="UTF-8 wiki draft file; omit to read stdin")
    parser.add_argument("--strict", action="store_true", help="Also fail on warnings")
    args = parser.parse_args(argv)

    if args.file:
        try:
            draft = Path(args.file).read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            print(f"ERROR: cannot read draft: {exc}", file=sys.stderr)
            return 2
    else:
        draft = sys.stdin.read()

    errors, warnings = validate(draft)
    for error in errors:
        print(f"ERROR: {error}")
    for warning in warnings:
        print(f"WARNING: {warning}")
    if not errors and not warnings:
        print("PASS: no BBCode syntax or checked publication-style issues found.")
    elif not errors:
        print("PASS: no errors; review warnings manually.")
    return 1 if errors or (args.strict and warnings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
