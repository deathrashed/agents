#!/usr/bin/env python3
"""Find official logos and icons on Wikimedia Commons, print their URLs, Markdown/HTML snippets, or download them.

Commons hosts the real brand marks (Discogs_icon.svg, ITunes_logo.svg, ...) with their licence, so it is the most
accurate source for README icons. Standard library only.

  commons-icon.py search "Discogs icon"              # SVGs that match, best first, with size and licence
  commons-icon.py search "iTunes logo" --md          # ready-to-paste <img> snippets
  commons-icon.py search "Bandcamp" --all-types      # PNGs and JPEGs too
  commons-icon.py url "File:Discogs icon.svg"        # one file's direct URL
  commons-icon.py url "Discogs icon.svg" --png 64    # a 64 px PNG rendering of it
  commons-icon.py get "File:ITunes logo.svg" --out assets/icons
  commons-icon.py get "Discogs icon" --pick 1 --out assets/icons --png 128

For README use, `--md` gives a 120 px PNG rendering: GitHub shows README images through its camo proxy, and camo
cannot load Commons SVG originals (HTTP 502), while it loads Commons PNG renderings. `--svg` keeps the original.

The first search result is not always the mark you want: read the list, then use `url` or `get` with the exact
file title. Logos on Commons are free (public domain or Creative Commons); brand marks stay subject to their
owners' trademark terms. Some are CC BY-SA: credit the author when you ship the file itself.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
# Wikimedia asks every client to identify itself with a way to reach its owner.
AGENT = "readme-visual-commons-icon/1.0 (https://github.com/deathrashed)"


def _get(params: dict) -> dict:
    url = f"{API}?{urllib.parse.urlencode({**params, 'format': 'json', 'formatversion': 2})}"
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=30) as reply:
        return json.load(reply)


def _clean(url: str) -> str:
    """The plain upload.wikimedia.org address (Commons adds tracking parameters)."""
    return url.split("?", 1)[0].replace("://thumb.wikimedia.org/", "://upload.wikimedia.org/") if url else url


def _text(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value or "").strip()


def _row(page: dict) -> dict:
    info = (page.get("imageinfo") or [{}])[0]
    meta = info.get("extmetadata") or {}
    return {
        "title": page.get("title", ""),
        "url": _clean(info.get("url", "")),
        "png": _clean(info.get("thumburl", "")) if info.get("thumburl") else "",
        "mime": info.get("mime", ""),
        "width": info.get("width"),
        "height": info.get("height"),
        "license": _text((meta.get("LicenseShortName") or {}).get("value", "")),
        "author": _text((meta.get("Artist") or {}).get("value", ""))[:80],
        "page": f"https://commons.wikimedia.org/wiki/{urllib.parse.quote(page.get('title', '').replace(' ', '_'))}",
    }


INFO = {"prop": "imageinfo", "iiprop": "url|size|mime|extmetadata", "iiextmetadatafilter": "LicenseShortName|Artist"}


def search(query: str, *, limit: int = 8, svg_only: bool = True, png: int = 0) -> list[dict]:
    text = f"{query} filemime:image/svg+xml" if svg_only else query
    params: dict[str, object] = {"action": "query", "generator": "search", "gsrsearch": text, "gsrnamespace": 6, "gsrlimit": limit, **INFO}
    if png:
        params["iiurlwidth"] = png
    pages = (_get(params).get("query") or {}).get("pages") or []
    return [_row(p) for p in sorted(pages, key=lambda p: p.get("index", 0))]


def lookup(title: str, *, png: int = 0) -> dict:
    title = title if title.lower().startswith("file:") else f"File:{title}"
    params: dict[str, object] = {"action": "query", "titles": title, **INFO}
    if png:
        params["iiurlwidth"] = png
    pages = (_get(params).get("query") or {}).get("pages") or []
    if not pages or pages[0].get("missing"):
        raise SystemExit(f"Not on Commons: {title}")
    return _row(pages[0])


def snippet(row: dict, *, height: int = 16, png: bool = False) -> str:
    name = re.sub(r"^File:|\.(svg|png|jpe?g)$", "", row["title"], flags=re.I).replace("_", " ")
    src = row["png"] if png and row["png"] else row["url"]
    return f'<img src="{src}" height="{height}" alt="{name}">'


def download(row: dict, out: Path, *, png: bool = False) -> Path:
    url = row["png"] if png and row["png"] else row["url"]
    out.mkdir(parents=True, exist_ok=True)
    target = out / urllib.parse.unquote(url.rsplit("/", 1)[-1])
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=60) as reply:
        target.write_bytes(reply.read())
    return target


def _print(rows: list[dict], *, md: bool, png: bool, as_json: bool, height: int) -> None:
    if as_json:
        print(json.dumps(rows, indent=2, ensure_ascii=False))
        return
    for n, row in enumerate(rows, 1):
        size = f"{row['width']}×{row['height']}" if row["width"] else ""
        print(f"{n:>2}. {row['title']}  [{size} · {row['license'] or 'licence unknown'}]")
        print(f"    {row['png'] if png and row['png'] else row['url']}")
        if md:
            print(f"    {snippet(row, height=height, png=png)}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("search", "url", "get"):
        command = sub.add_parser(name)
        command.add_argument("query", help="search words, or an exact file title for url/get")
        command.add_argument("--png", type=int, default=0, metavar="WIDTH", help="a PNG rendering this wide instead of the original")
        command.add_argument("--md", action="store_true", help="also print an <img> snippet (a 120 px PNG, which GitHub can show)")
        command.add_argument("--svg", action="store_true", help="with --md: the SVG original (GitHub's image proxy cannot load it)")
        command.add_argument("--height", type=int, default=16, help="snippet height (default 16)")
        command.add_argument("--json", action="store_true", help="JSON output")
        if name != "url":
            command.add_argument("--limit", type=int, default=8)
            command.add_argument("--all-types", action="store_true", help="PNG and JPEG too, not only SVG")
        if name == "get":
            command.add_argument("--out", type=Path, default=Path("."), help="folder to save into")
            command.add_argument("--pick", type=int, default=0, help="with search words: which result to save (1 = first)")
    args = parser.parse_args()
    if args.md and not args.png and not args.svg:
        args.png = 120  # GitHub's camo proxy loads Commons PNG renderings, not the SVG originals
    png = bool(args.png)
    if args.command == "search":
        rows = search(args.query, limit=args.limit, svg_only=not args.all_types, png=args.png)
        if not rows:
            sys.exit("Nothing found; try other words or --all-types")
        _print(rows, md=args.md, png=png, as_json=args.json, height=args.height)
    elif args.command == "url":
        _print([lookup(args.query, png=args.png)], md=args.md, png=png, as_json=args.json, height=args.height)
    else:
        if args.query.lower().startswith("file:") or re.search(r"\.(svg|png|jpe?g)$", args.query, re.I):
            row = lookup(args.query, png=args.png)
        else:
            rows = search(args.query, limit=args.limit, svg_only=not args.all_types, png=args.png)
            if not rows:
                sys.exit("Nothing found")
            if not args.pick:
                _print(rows, md=False, png=png, as_json=False, height=args.height)
                sys.exit("Several matches: run again with --pick N, or give the exact file title")
            row = rows[args.pick - 1]
        path = download(row, args.out, png=png)
        print(f"{path}  [{row['license'] or 'licence unknown'}]")
        if args.md:
            print(snippet({**row, "url": str(path)}, height=args.height))


if __name__ == "__main__":
    main()
