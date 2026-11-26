#!/usr/bin/env python3
"""Check README media: what GitHub strips, unoptimised assets, missing sources.

Errors are things that render as nothing or lose the reader; warnings are size
and hygiene judgements. Exit status is 1 on any error (or warning with --strict).
"""

import argparse
import os
import re
import subprocess
import sys

# GitHub strips these outright in .md files; the reader sees nothing.
STRIPPED = re.compile(r"<(video|iframe|embed|object)\b", re.IGNORECASE)
RAW_VIDEO = re.compile(
    r"""(?:<video\b[^>]*src=["']|!?\[[^\]]*\]\()\s*((?!https://github\.com/user-attachments)"""
    r"""[^"')\s]+\.(?:mp4|mov|webm|mkv))""",
    re.IGNORECASE,
)
IMG = re.compile(r"<img\b[^>]*>|!\[[^\]]*\]\([^)]+\)", re.IGNORECASE)
SRC = re.compile(r"""(?:src|srcset)=["']([^"']+)["']|\]\(([^)\s]+)""", re.IGNORECASE)
ALT_ATTR = re.compile(r"""\balt\s*=\s*""", re.IGNORECASE)

GIF_LIMIT = 5 * 1024 * 1024
IMAGE_LIMIT = 2 * 1024 * 1024
SVG_LIMIT = 20 * 1024
TOTAL_LIMIT = 12 * 1024 * 1024


def human(size):
    return f"{size / 1024 / 1024:.1f} MB" if size >= 1024 * 1024 else f"{size / 1024:.0f} KB"


def local_path(repo, url):
    if re.match(r"(?:https?:|data:|#|mailto:)", url, re.IGNORECASE):
        return None
    return os.path.normpath(os.path.join(repo, url.split("?")[0].split("#")[0]))


def check(path):
    errors, warnings = [], []
    repo = os.path.dirname(os.path.abspath(path))
    text = open(path, encoding="utf-8").read()

    # Tags GitHub removes entirely
    for match in STRIPPED.finditer(text):
        tag = match.group(1).lower()
        line = text[: match.start()].count("\n") + 1
        if tag in ("embed", "object"):
            errors.append(f"line {line}: <{tag}> is stripped by GitHub; use an <img> or a link")
        elif tag == "iframe":
            errors.append(f"line {line}: <iframe> is stripped by GitHub; use a thumbnail image linking to the video")
        else:
            errors.append(f"line {line}: <video> is stripped on GitHub unless it is a github.com/user-attachments URL; use animated WebP/GIF in <img> (references/media.md)")

    for match in RAW_VIDEO.finditer(text):
        line = text[: match.start()].count("\n") + 1
        errors.append(f"line {line}: video {match.group(1)[:60]} will not play on GitHub; see references/media.md")

    # Alt text on media images only. Decorative heading/badge icons and Iconify
    # glyphs are not content; validate-readme.py covers the general case.
    for match in IMG.finditer(text):
        tag = match.group(0)
        line = text[: match.start()].count("\n") + 1
        is_heading = re.match(r"^#{1,6}\s", text.splitlines()[line - 1] or "")
        decorative = re.search(r"iconify\.design|shieldcn\.dev|shields\.io|demolab\.com|readmecodegen|readme-typing-svg|img\.shields", tag)
        is_media = re.search(r"\.(?:gif|webp|png|jpe?g|svg|mp4|mov|webm)\b", tag, re.IGNORECASE)
        if is_heading or decorative or not is_media:
            continue
        if tag.lower().startswith("<img") and not ALT_ATTR.search(tag):
            errors.append(f"line {line}: media <img> without alt: {tag[:60]}")

    # Local media: existence and size
    total, seen, missing = 0, set(), []
    for a, b in SRC.findall(text):
        url = (a or b).strip()
        if not url or url.startswith("#"):
            continue
        target = local_path(repo, url)
        if not target or target in seen:
            continue
        seen.add(target)
        ext = os.path.splitext(target)[1].lower()
        if ext not in (".gif", ".webp", ".png", ".jpg", ".jpeg", ".svg", ".mp4", ".mov", ".webm"):
            continue
        if not os.path.isfile(target):
            missing.append(url)
            continue
        size = os.path.getsize(target)
        total += size
        rel = os.path.relpath(target, repo)
        if ext == ".gif" and size > GIF_LIMIT:
            warnings.append(f"{rel} is {human(size)}: convert to WebP or MP4, or trim it (references/media.md)")
        elif ext in (".png", ".jpg", ".jpeg", ".webp") and size > IMAGE_LIMIT:
            warnings.append(f"{rel} is {human(size)}: downscale or re-encode as WebP at quality 80")
        elif ext == ".svg" and size > SVG_LIMIT:
            warnings.append(f"{rel} is {human(size)}: minify the SVG or simplify the animation")
    for url in missing[:5]:
        errors.append(f"media file referenced but not on disk: {url}")

    if total > TOTAL_LIMIT:
        warnings.append(f"total local media is {human(total)}: the page loads slowly; trim to the few that earn it")

    # Animated SVG must honour reduced motion
    animated = 0
    for target in seen:
        if os.path.splitext(target)[1].lower() != ".svg" or not os.path.isfile(target):
            continue
        svg = open(target, encoding="utf-8", errors="replace").read()
        if re.search(r"@keyframes|<animate", svg):
            animated += 1
            if "prefers-reduced-motion" not in svg:
                warnings.append(f"{os.path.relpath(target, repo)} animates without a prefers-reduced-motion override")
    if animated > 2:
        warnings.append(f"{animated} animated SVGs: keep to one or two signature motions")

    # A demo earns its place only if the text also says something
    if re.search(r"\.(?:gif|webp|mp4)[\"'\)\s]", text) and not re.search(r"^```", text, re.MULTILINE):
        warnings.append("media but no code block: pair the demo with the command it demonstrates")

    return errors, warnings


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("readme")
    parser.add_argument("--strict", action="store_true", help="fail on warnings too")
    args = parser.parse_args()

    errors, warnings = check(args.readme)
    for e in errors:
        print(f"  ✗ {e}")
    for w in warnings:
        print(f"  ! {w}")
    if not errors and not warnings:
        print("✓ No media problems found")
    else:
        print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors or (args.strict and warnings) else 0)


if __name__ == "__main__":
    main()
