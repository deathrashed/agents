#!/usr/bin/env python3
"""Print centred, clickable README badge rows, one <p align="center"> per row.

Each badge is LABEL|LOGO|LINK[|ALT]; the word +++ starts a new row.

  generate-badge-row.py --theme purple "Python 3|python|https://www.python.org/|Python 3 runtime" \\
      "Bash|gnubash|https://www.gnu.org/software/bash/" +++ "GPL 3|lu:Scale|#license|GPL-3.0 license"

  generate-badge-row.py --json badges.json   # [[{"label", "logo", "href", "alt"}, ...], ...] or a flat list

Default output is adaptive shieldcn: a <picture> with dark and light sources.
--shields emits the classic shields.io for-the-badge style with the labelColor
recipe (references/shieldcn-recipes.md). For any other shieldcn image (groups,
providers, charts, split badges) use scripts/shieldcn_badge.py.
"""

import argparse
import json
import sys
from urllib.parse import quote


def shieldcn_url(badge, args, mode):
    logo_color = args.light_logo_color if mode == "light" and args.light_logo_color else args.logo_color
    params = [("variant", args.variant), ("size", args.size), ("theme", args.theme),
              ("logo", badge.get("logo")), ("logoColor", logo_color), ("mode", mode)]
    query = "&amp;".join(f"{k}={quote(v, safe='')}" for k, v in params if v)
    return f"https://shieldcn.dev/badge/{quote(badge['label'], safe='')}.svg?{query}"


def render(badge, args):
    href, alt = badge["href"], badge.get("alt") or badge["label"]
    if args.shields:
        label = quote(badge["label"].lower().replace("-", "--"), safe="")
        src = f"https://img.shields.io/badge/{label}-{args.bg}?style=for-the-badge"
        if badge.get("logo"):
            src += f"&amp;logo={quote(badge['logo'], safe='')}&amp;logoColor={args.logo_color or 'ffffff'}"
        src += f"&amp;labelColor={args.label_bg}"
        return f'  <a href="{href}"><img src="{src}" alt="{alt}"></a>'
    return (f'  <a href="{href}"><picture>'
            f'<source media="(prefers-color-scheme: dark)" srcset="{shieldcn_url(badge, args, "dark")}">'
            f'<img src="{shieldcn_url(badge, args, "light")}" alt="{alt}"></picture></a>')


def parse(spec):
    parts = spec.split("|")
    if len(parts) not in (3, 4):
        sys.exit(f"badge must be LABEL|LOGO|LINK[|ALT], got: {spec}")
    return dict(zip(("label", "logo", "href", "alt"), parts))


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("items", nargs="*", help="LABEL|LOGO|LINK[|ALT] badges; +++ starts a new row")
    parser.add_argument("--json", help="JSON file: a list of rows, or one flat list of badges")
    parser.add_argument("--variant", default="outline", help="shieldcn variant: outline (common choice), secondary, default, branded")
    parser.add_argument("--size", default="", help="shieldcn size: xs, sm, default, lg")
    parser.add_argument("--theme", default="", help="shieldcn theme: purple, blue, green, emerald, rose, ...")
    parser.add_argument("--logo-color", default="ffffff", help="logo colour hex without # (dark mode)")
    parser.add_argument("--light-logo-color", default="", help="light-mode logo colour (defaults to --logo-color)")
    parser.add_argument("--shields", action="store_true", help="classic shields.io style instead of shieldcn")
    parser.add_argument("--bg", default="202327", help="shields.io background hex")
    parser.add_argument("--label-bg", default="40474e", help="shields.io logo segment hex")
    args = parser.parse_args()

    rows, current = [], []
    for item in args.items:
        if item == "+++":
            rows.append(current)
            current = []
        else:
            current.append(parse(item))
    rows.append(current)
    if args.json:
        with open(args.json, encoding="utf-8") as handle:
            data = json.load(handle)
        rows += data if data and isinstance(data[0], list) else [data]
    rows = [row for row in rows if row]
    if not rows:
        parser.error("give at least one badge or --json")

    for row in rows:
        print('<p align="center">')
        print("\n".join(render(badge, args) for badge in row))
        print("</p>")


if __name__ == "__main__":
    main()
