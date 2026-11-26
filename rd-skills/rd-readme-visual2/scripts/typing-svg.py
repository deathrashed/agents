#!/usr/bin/env python3
"""Build a readme-typing-svg tagline as an adaptive <picture> block.

  typing-svg.py --color b030f0 "upload • reference • archive" "copy links in any format"

Defaults to repeat=false (no endless loop). The light-mode colour defaults to a
darker shade of --color so the text stays readable on white.
"""

import argparse
from urllib.parse import quote_plus

BASE = "https://readme-typing-svg.demolab.com/"


def darken(hex_color, factor=0.7):
    rgb = [int(hex_color[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{int(c * factor):02X}" for c in rgb)


def build(lines, color, args):
    params = [
        ("font", args.font), ("size", args.size), ("duration", args.duration), ("pause", args.pause),
        ("color", color.upper()), ("center", "true"), ("vCenter", "true"),
        ("repeat", "true" if args.repeat else "false"), ("width", args.width),
    ]
    if args.height:
        params.append(("height", args.height))
    if args.multiline:
        params.append(("multiline", "true"))
    query = "&".join(f"{k}={quote_plus(str(v))}" for k, v in params)
    return f"{BASE}?{query}&lines={';'.join(quote_plus(line) for line in lines)}"


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("lines", nargs="+", help="one argument per typed line")
    parser.add_argument("--color", required=True, help="accent hex for dark mode, no #")
    parser.add_argument("--light-color", help="hex for light mode (default: darker --color)")
    parser.add_argument("--font", default="JetBrains Mono")
    parser.add_argument("--size", type=int, default=18)
    parser.add_argument("--width", type=int, help="box width (default: fits the longest line)")
    parser.add_argument("--height", type=int)
    parser.add_argument("--duration", type=int, default=3000)
    parser.add_argument("--pause", type=int, default=1200)
    parser.add_argument("--repeat", action="store_true", help="loop forever (off by default)")
    parser.add_argument("--multiline", action="store_true")
    parser.add_argument("--link", default="", help="wrap in a link, e.g. #quick-start")
    args = parser.parse_args()

    color = args.color.lstrip("#")
    if not args.width:
        args.width = max(320, int(max(len(line) for line in args.lines) * args.size * 0.62) + 40)
    dark = build(args.lines, color, args)
    light = build(args.lines, (args.light_color or darken(color)).lstrip("#"), args)
    alt = "; ".join(args.lines).replace('"', "&quot;")

    picture = (f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{dark}">\n'
               f'  <img alt="{alt}" src="{light}">\n</picture>')
    if args.link:
        picture = f'<a href="{args.link}">{picture}</a>'
    print(f'<p align="center">{picture}</p>')


if __name__ == "__main__":
    main()
