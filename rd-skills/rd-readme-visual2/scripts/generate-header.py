#!/usr/bin/env python3
"""Adaptive shieldcn header banner (light/dark <picture> pair) with every documented option.

  generate-header.py --title LYRIXEARCH --subtitle "find, review & embed lyrics for your audio library"
  generate-header.py --title Acme --subtitle "Build faster" --preset graph --logo rust --logo-color brand --font geist-mono
  generate-header.py --title Acme --size social --gradient 6366f1,8b5cf6,135 --title-color fff --align left --no-border
  generate-header.py --title Acme --logo https://example.com/logo.png --preset glow --theme blue --watermark

Presets: dots (default) surface gradient grid graph glow transparent.   Sizes: banner 750x260, wide 1280x400,
social 1280x640, square 640x640, or --width 240-2400 / --height 100-1600.   Logo: SimpleIcons slug, ri:Name,
lu:Name (Lucide), data: URI, https image, or false; --logo-color hex or `brand`.
Photo backgrounds: --param image=<url> --param overlay=<hex> --param tint=<hex>.  Anything else: --param K=V.
"""

import argparse
import urllib.parse


def url(a, mode):
    p = [("title", a.title)]
    if a.subtitle:
        p.append(("subtitle", a.subtitle))
    p.append(("mode", mode))
    p.append(("align", a.align))
    for key, val in (("logo", a.logo), ("logoColor", a.logo_color), ("theme", a.theme), ("font", a.font), ("accent", a.accent), ("size", a.size),
                     ("width", a.width), ("height", a.height), ("bg", a.bg), ("gradient", a.gradient), ("glow", a.glow),
                     ("titleColor", a.title_color), ("subtitleColor", a.subtitle_color), ("radius", a.radius), ("pattern", a.pattern)):
        if val:
            p.append((key, str(val)))
    if a.no_border:
        p.append(("border", "false"))
    if a.watermark:
        p.append(("watermark", "true"))
    for kv in a.param or []:
        k, _, v = kv.partition("=")
        p.append((k, v))
    return f"https://shieldcn.dev/header/{a.preset}.{a.ext}?" + urllib.parse.urlencode(p, quote_via=urllib.parse.quote_plus, safe=":/,")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--title", required=True)
    ap.add_argument("--subtitle", default="")
    ap.add_argument("--preset", default="dots", choices=["dots", "surface", "gradient", "grid", "graph", "glow", "transparent"])
    ap.add_argument("--align", default="left", choices=["left", "center"])
    for f in ("logo", "logo-color", "theme", "font", "accent", "size", "width", "height", "bg", "gradient", "glow", "title-color", "subtitle-color",
              "radius", "pattern", "link"):
        ap.add_argument("--" + f)
    ap.add_argument("--no-border", action="store_true")
    ap.add_argument("--watermark", action="store_true")
    ap.add_argument("--param", action="append")
    ap.add_argument("--ext", default="svg", choices=["svg", "png", "json"])
    ap.add_argument("--format", default="html", choices=["html", "md", "url"])
    a = ap.parse_args()
    light, dark = url(a, "light"), url(a, "dark")
    if a.format == "url":
        print(f"light: {light}\ndark:  {dark}")
    elif a.format == "md":
        print(f"![{a.title}]({light})")
    else:
        pic = f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{dark}" />\n  <img alt="{a.title}" src="{light}" />\n</picture>'
        pic = f'<a href="{a.link}">{pic}</a>' if a.link else pic
        print(f'<p align="center">\n{pic}\n</p>')
