#!/usr/bin/env python3
"""Validate a README against the readme-visual checklist.

Errors are rule breaks that render badly or mislead readers; warnings are
judgement calls. Exit status is 1 when any error is found (or any warning with
--strict). --online also requests every image and link URL.
"""

import argparse
import concurrent.futures
import html
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request

LICENSE_LIBRARY = "/Users/rd/Scripts/Riley/gupload/uploads/files/licenses"
USER_AGENTS = (  # some hosts reject browser agents (iconify 403), others only answer them (crates.io)
    "readme-visual-validator/2.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/131.0 Safari/537.36",
)
ICONIFY_COLOR = re.compile(r"api\.iconify\.design/[^\s\"')]*?[?&]color=%23([0-9a-fA-F]{3,8})")
ICONIFY_SET = re.compile(r"api\.iconify\.design/([a-z0-9-]+)[:/]")
IMG_TAG = re.compile(r"<img\b[^>]*>", re.IGNORECASE)
TOP_TAG = re.compile(r"<(p|h1|h2|h3)\b[^>]*>", re.IGNORECASE)
HREF_ANCHOR = re.compile(r"""href=["']#([^"']+)["']""")
MD_ANCHOR = re.compile(r"\]\(#([^)\s]+)\)")
NAMED_ANCHOR = re.compile(r"""<a\s+(?:name|id)=["']([^"']+)["']""", re.IGNORECASE)
URLS = re.compile(r"""(?:src|href|srcset)=["'](https?://[^"'\s]+)["']|\]\((https?://[^)\s]+)\)""")
REL_LINKS = re.compile(r"""(?:src|href)=["'](?!https?:|#|mailto:|data:)([^"'\s]+)["']|\]\((?!https?:|#|mailto:)([^)\s]+)\)""")
BADGE_HOST = re.compile(r"shields\.io|shieldcn\.dev/(?:badge|github|npm|crates|pypi|group)|demolab\.com/badge")
QUICK_START = re.compile(r"quick\s*start|getting started|install", re.IGNORECASE)
FILLER = re.compile(r"\b(simply|just|basically|in order to|it is important to note|it's worth noting)\b", re.IGNORECASE)


def is_emoji(ch):
    # Symbol-other above the arrows block, excluding Mathematical Alphanumerics (Unicode bold text)
    return unicodedata.category(ch) == "So" and ord(ch) > 0x2100 and not 0x1D400 <= ord(ch) <= 0x1D7FF


def outside_code(lines):
    """Return [(line_number, line)] outside fenced code, and fence lines lacking a language."""
    in_fence, fence, bare, out = False, "", [], []
    for number, line in enumerate(lines, 1):
        stripped = line.strip()
        marker = stripped[:3]
        if marker in ("```", "~~~") and (not in_fence or marker == fence):
            if not in_fence and stripped in ("```", "~~~"):
                bare.append(number)
            in_fence, fence = not in_fence, marker
            continue
        if not in_fence:
            out.append((number, line))
    return out, bare


def heading_text(line):
    text = re.sub(r"^#+\s*", "", line)
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def slugify(text):
    """Match GitHub's anchor generation.

    Decode entities first (&amp; -> &), then drop everything that is not a word
    character, hyphen or space, then turn each space into a hyphen. Runs of
    spaces are NOT collapsed, so "Run & Test" becomes "#run--test". Failing to
    decode entities produced "#run-amp-test" and false "broken anchor" reports.
    """
    text = html.unescape(text)
    text = text.lower()
    text = re.sub(r"[^\w\- ]", "", text)
    return text.replace(" ", "-")


def first_line(path):
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            if line.strip():
                return line.strip().upper()
    return ""


def detect_license(repo):
    """Return (library id, snippet title) for the repo's LICENSE, matched against the gupload library."""
    for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
        path = os.path.join(repo, name)
        if os.path.isfile(path):
            break
    else:
        return None, None
    if not os.path.isdir(LICENSE_LIBRARY):
        return "unknown", None
    head = first_line(path)
    for lid in sorted(os.listdir(LICENSE_LIBRARY)):
        lib = os.path.join(LICENSE_LIBRARY, lid, "LICENSE")
        snippet = os.path.join(LICENSE_LIBRARY, lid, "snippet.md")
        if os.path.isfile(lib) and os.path.isfile(snippet) and first_line(lib) == head:
            title = re.search(r"\[\*\*(.+?)\*\*\]", open(snippet, encoding="utf-8").read())
            return lid, title.group(1) if title else None
    return "unknown", None


def check(path, online=False):
    errors, warnings = [], []
    repo = os.path.dirname(os.path.abspath(path))
    raw = open(path, encoding="utf-8").read()
    lines = raw.splitlines()
    body, bare_fences = outside_code(lines)
    text = "\n".join(line for _, line in body)
    headings = [(n, line) for n, line in body if re.match(r"^#{1,6}\s", line)]
    h2 = [(n, line) for n, line in headings if line.startswith("## ")]

    # Top block: present, and every child centred on its own
    start = next((i for i, l in enumerate(lines[:20]) if '<div align="center">' in l), None)
    if start is None:
        errors.append('no centred top block: <div align="center"> in the first 20 lines')
    else:
        end = next((i for i in range(start + 1, len(lines)) if "</div>" in lines[i]), start)
        in_centred = False  # inside a <p align=...> that spans several lines
        for i in range(start + 1, end):
            line = lines[i]
            for match in TOP_TAG.finditer(line):
                if "align=" not in match.group(0):
                    errors.append(f"line {i + 1}: top-block <{match.group(1)}> without its own align=\"center\" (GitHub does not inherit it)")
            if line.lstrip().startswith("<img") and "align=" not in line and not in_centred:
                warnings.append(f"line {i + 1}: top-block <img> outside a centred <p> and without align")
            if re.search(r"<p\b[^>]*align=", line):
                in_centred = True
            if "</p>" in line:
                in_centred = False

    # Paragraph nesting
    if re.search(r'<p align="center">\s*<p\b', text):
        errors.append('nested <p align="center"> (one is left open)')
    opens, closes = len(re.findall(r"<p\b", text)), len(re.findall(r"</p>", text))
    if opens != closes:
        errors.append(f"unbalanced <p>: {opens} opened, {closes} closed")

    # Light/dark picture pairs and clickable badges
    for pic in re.findall(r"<picture>.*?</picture>", text, re.S):
        if "prefers-color-scheme: dark" not in pic or "<img" not in pic:
            errors.append("<picture> without a dark <source> and a fallback <img>")
    for match in re.finditer(r"<(picture|img)\b", text):
        pos = match.start()
        if match.group(1) == "img" and text.rfind("<picture>", 0, pos) > text.rfind("</picture>", 0, pos):
            continue  # checked through its <picture>
        close = "</picture>" if match.group(1) == "picture" else ">"
        chunk = text[pos:text.find(close, pos) + len(close)]
        if BADGE_HOST.search(chunk) and not re.search(r"<a\b[^>]*>\s*$", text[max(0, pos - 250):pos]):
            errors.append("badge not wrapped in <a href>: " + re.sub(r"\s+", " ", chunk)[:80])
            break

    # Headings: icon, no emoji, one Iconify set
    sets = set()
    for n, line in h2:
        if not re.search(r"<img\s|!\[", line):
            errors.append(f"line {n}: heading without an icon: {heading_text(line)!r}")
        sets.update(ICONIFY_SET.findall(line))
    for n, line in headings:
        if any(is_emoji(ch) for ch in heading_text(line)):
            errors.append(f"line {n}: emoji in heading: {heading_text(line)!r}")
    if len(sets) > 1:
        warnings.append(f"headings mix Iconify sets: {', '.join(sorted(sets))} (pick one)")

    # Palette
    colors = {c.lower() for c in ICONIFY_COLOR.findall(text)}
    if len(colors) > 2:
        shown = ", ".join("#" + c for c in sorted(colors))
        warnings.append(f"{len(colors)} Iconify colours in use ({shown}); keep to 1-2 accents")

    # Alt text
    for n, line in body:
        for tag in IMG_TAG.findall(line):
            if not re.search(r"\balt=", tag, re.IGNORECASE):
                errors.append(f"line {n}: <img> without alt: {tag[:70]}")
        if re.search(r"!\[\s*\]\(", line):
            warnings.append(f"line {n}: Markdown image with empty alt text")

    # Anchors
    slugs, seen = set(NAMED_ANCHOR.findall(text)), {}
    for _, line in headings:
        slug = slugify(heading_text(line))
        count = seen.get(slug, 0)
        slugs.add(slug if count == 0 else f"{slug}-{count}")
        seen[slug] = count + 1
    for anchor in sorted(set(HREF_ANCHOR.findall(text) + MD_ANCHOR.findall(text))):
        if urllib.parse.unquote(anchor) not in slugs:
            errors.append(f"broken anchor link: #{anchor}")

    # Heading hygiene: anchors a reader cannot predict, and sentence-style headings
    for n, line in h2:
        heading_raw = re.sub(r"<[^>]+>", "", re.sub(r"^#+\s*", "", line)).strip()
        if re.search(r"&(?:amp|lt|gt|quot|#\d+);|[&:?!,'\u2019]", heading_raw):
            slug = slugify(heading_raw)
            warnings.append(f"line {n}: {heading_raw!r} anchors to #{slug}; punctuation makes links unpredictable (use 'and', plain words)")
        if len(heading_raw.split()) > 6 or re.search(r"[a-z]:\s", heading_raw):
            warnings.append(f"line {n}: long heading {heading_raw!r}; keep ##/### to 1-3 words in Title Case")

    # Relative links (../../x is a GitHub UI route such as releases or issues)
    for a, b in REL_LINKS.findall(text):
        target = urllib.parse.unquote((a or b).split("#")[0].split("?")[0])
        if target and not target.startswith("../../") and not os.path.exists(os.path.join(repo, target)):
            errors.append(f"relative link to a missing file: {target}")

    # Markdown straight after <div align="center"> or </summary> renders literally on GitHub
    for i, line in enumerate(lines[:-1]):
        if line.strip() == '<div align="center">' and re.match(r"\s*(\[\*\*|\*\*|#|- |\|)", lines[i + 1]):
            errors.append(f"line {i + 2}: Markdown directly after <div align=\"center\"> needs a blank line before it")
        if line.rstrip().endswith("</summary>") and lines[i + 1].strip():
            errors.append(f"line {i + 2}: add a blank line after </summary> or the Markdown inside won't render")

    # Required structure
    quick = next((n for n, line in h2 if QUICK_START.search(line)), None)
    if quick is None:
        errors.append("no Quick Start / Install / Getting Started section")
    elif quick > 60:
        warnings.append(f"Quick Start first appears at line {quick}; aim for the first ~40 lines")
    if not re.search(r"^\|.*\|\s*$\n^\|\s*:?-{3,}", raw, re.MULTILINE):
        errors.append("no Markdown table (commands, options, config, or features)")
    if not re.search(r"```text\n(?:.*\n)*?.*[├└]──", raw):
        errors.append("no ASCII structure tree in a ```text block")
    if "<details" not in text:
        errors.append("no <details> dropdown for advanced material")
    if not re.search(r"^> \[!(TIP|NOTE|IMPORTANT|WARNING|CAUTION)\]", text, re.MULTILINE):
        errors.append("no GitHub alert hint (> [!TIP], > [!NOTE], ...)")
    for n in bare_fences:
        warnings.append(f"line {n}: code block without a language tag")

    # License section matches the repo's LICENSE and the library snippet
    section = re.search(r"^##\s.*licen[cs]e.*?(?=^## |\Z)", text, re.M | re.S | re.I)
    lid, title = detect_license(repo)
    if not section:
        errors.append("no License section")
    else:
        block = section.group(0)
        if 'width="180"' not in block or '<div align="center">' not in block:
            errors.append("License block is not the centred snippet with a 180px badge (references/licenses.md)")
        if title and title not in block:
            errors.append(f"License section doesn't match LICENSE ({lid}); use: scripts/license-snippet.py {lid}")
        if lid == "unknown":
            warnings.append("LICENSE isn't in the gupload library; add it there or ask which license is intended")
    if lid is None:
        warnings.append("no LICENSE file in the repo")

    # Prose: filler words and dashes (headings, tables, HTML, and code excluded)
    prose = [(n, l) for n, l in body if l.strip() and not l.lstrip().startswith(("#", "|", "<", ">", "!["))]
    dashes = [n for n, l in prose if re.search(r"\s[—–]\s|[a-z][—–][a-z]", l)]
    if dashes:
        warnings.append(f"em/en dashes in prose on lines {', '.join(map(str, dashes[:8]))}: use a full stop, comma, or colon")
    filler = [f"{n} ({m.group(0)})" for n, l in prose for m in [FILLER.search(l)] if m]
    if filler:
        warnings.append(f"filler words on lines {', '.join(filler[:8])}")

    if any("repeat=false" not in url for url in re.findall(r"readme-typing-svg[^\s\"']+", text)):
        warnings.append("typing SVG loops forever; add repeat=false unless the user wants a loop")

    # Audit checks (references/audit.md): badge discipline, honest status, verifiable claims
    count = len([m for m in re.findall(r"<img\b[^>]*(?:shields\.io|shieldcn\.dev|demolab\.com)|!\[[^\]]*\]\([^)]*(?:shields\.io|shieldcn\.dev|demolab\.com)", text) if "shieldcn.dev/header" not in m])
    if count > 5:
        warnings.append(f"{count} badges: keep 3-5 assessment signals that answer a reader's question; cut intent badges (references/audit.md)")
    for phrase in sorted({m.lower() for m in re.findall(r"production[- ]ready|battle[- ]tested|enterprise[- ]grade|blazing fast|world[- ]class", text, re.I)}):
        warnings.append(f"unverifiable claim {phrase!r}: cite a benchmark, CI matrix, or changelog entry, or cut it (references/audit.md)")
    if not re.search(r"\b(experimental|alpha|beta|pre-?release|stable|seeking (?:a )?maintainers?|actively maintained|maintenance mode)\b", text, re.I):
        warnings.append("no status line: say experimental / beta / stable / seeking maintainers (references/audit.md A4)")

    if online:
        errors.extend(check_urls(text))
    return errors, warnings


def fetch(url):
    status = None
    for agent in USER_AGENTS:
        request = urllib.request.Request(url, headers={"User-Agent": agent, "Accept": "text/html,image/svg+xml,*/*"})
        try:
            with urllib.request.urlopen(request, timeout=20) as response:
                response.read(512)
                return url, response.status
        except urllib.error.HTTPError as error:
            status = error.code
        except Exception as error:  # report network failures instead of raising
            status = type(error).__name__
    return url, status


def check_urls(text):
    urls = sorted({(a or b).replace("&amp;", "&") for a, b in URLS.findall(text)})
    urls = [u for u in urls if not (u.startswith("https://github.com/") and "/releases" in u)]
    problems = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        for url, status in pool.map(fetch, urls):
            if not (isinstance(status, int) and status < 400):
                problems.append(f"URL failed ({status}): {url[:120]}")
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("readme")
    parser.add_argument("--online", action="store_true", help="request every image and link URL")
    parser.add_argument("--strict", action="store_true", help="fail on warnings too")
    args = parser.parse_args()

    errors, warnings = check(args.readme, args.online)
    for e in errors:
        print(f"  ✗ {e}")
    for w in warnings:
        print(f"  ! {w}")
    if not errors and not warnings:
        print("✓ No problems found" + ("" if args.online else " (offline; add --online to test every URL)"))
    else:
        print(f"{len(errors)} error(s), {len(warnings)} warning(s)")
    sys.exit(1 if errors or (args.strict and warnings) else 0)


if __name__ == "__main__":
    main()
