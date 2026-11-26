#!/usr/bin/env python3
"""Build ANY shieldcn image URL: static, dynamic-JSON, HTTPS-endpoint, live provider, group, chart,
contributors, sponsors, flag, view counter, header. Emits an adaptive light/dark <picture> by default.

Static (label, message, colour; `_`/%20 = space, `__` = literal _, `--` = literal -):
  shieldcn_badge.py --label "Runs on" --message Linux --platform linux --variant outline
  shieldcn_badge.py --message Python --brand python --variant outline --value-color ffff
  shieldcn_badge.py --label build --message passing --color brightgreen --status-dot --animate pulse
Dynamic JSON / HTTPS endpoint:
  shieldcn_badge.py --dynamic-json https://api.github.com/repos/o/r --query '$.stargazers_count' --label stars
  shieldcn_badge.py --https cal-badge.runkit.sh/path
Live provider, group, chart, wall, flag (any endpoint path is accepted):
  shieldcn_badge.py --provider github/stars/OWNER/REPO --link https://github.com/OWNER/REPO
  shieldcn_badge.py --group npm/react github/stars/vercel/next.js github/license/vercel/next.js --variant branded
  shieldcn_badge.py --provider chart/github/issues/OWNER/REPO --param title=Issues --param bg=transparent
  shieldcn_badge.py --provider contributors/OWNER/REPO --param limit=12 --param names=false
  shieldcn_badge.py --provider flag/au --variant outline

Anything not covered by a named flag goes through --param KEY=VALUE (repeatable), so every documented
shieldcn option is reachable: labelColor, labelTextColor, labelOpacity, gradient, animate, height, fontSize,
radius, padX, iconSize, gap, labelGap, bg, border, ...

--mode both|light|dark|single  (both = <picture> pair, the default)   --ext svg|png|json|shields.json
--format html|md|url|json     (json prints {"light":..,"dark":..,"markdown":..,"html":..})
--logo-color-light / --logo-color-dark give a different icon colour per theme (a light-green icon vanishes on a light pill).
--logo accepts a SimpleIcons slug, ri:Name, lu:Name (Lucide), data: URI, an https image URL or false.
--brand works only for: python go rust docker github npm typescript react svelte bun cplusplus postgresql
sqlite redis vercel openpanel anthropic openai discord youtube homebrew vscode gitlab.
"""

import argparse
import json
import urllib.parse

BASE = "https://shieldcn.dev"
NAMED = {"brightgreen", "green", "yellow", "orange", "red", "blue", "purple", "violet", "grey", "lightgrey"}
PLATFORMS = {  # name -> (message, colour, logo slug, logo colour)
    "linux": ("Linux", "FCC624", "linux", "f1be1c"),
    "macos": ("macOS", "000000", "apple", "ffffff"),
    "windows": ("Windows", "0078D4", "windows", "ffffff"),
    "android": ("Android", "3DDC84", "android", "ffffff"),
    "ios": ("iOS", "000000", "apple", "ffffff"),
    "docker": ("Docker", "2496ED", "docker", "ffffff"),
    "tauri": ("Tauri", "FFC131", "tauri", "24C8DB"),
    "ratatui": ("ratatui", "000000", "rust", "ffffff"),
}


def seg(s: str) -> str:
    """Static-badge path segment: literal `-` -> `--`, literal `_` -> `__`, space -> `_`-safe %20."""
    s = s.replace("-", "--").replace("_", "__")
    return urllib.parse.quote(s, safe="").replace("%20", "%20")


def path(a) -> str:
    if a.group:
        return "group/" + "+".join(g.strip("/") for g in a.group)
    if a.dynamic_json:
        return "badge/dynamic/json"
    if a.https:
        return "https/" + a.https.replace("https://", "").strip("/")
    if a.provider:
        return a.provider.strip("/")
    if a.message:
        parts = [seg(a.label)] if a.label else []
        parts.append(seg(a.message))
        if a.color:
            parts.append(a.color.lstrip("#") if a.color.lstrip("#").lower() not in NAMED else a.color.lstrip("#").lower())
        return "badge/" + "-".join(parts)
    raise SystemExit("give --message (with --label), --provider, --group, --dynamic-json or --https")


def query(a, mode):
    p = []
    if a.variant and not path(a).startswith(("chart/", "contributors/", "sponsors/")):
        p.append(("variant", a.variant))
    if a.size and a.size != "sm":
        p.append(("size", a.size))
    if mode:
        p.append(("mode", mode))
    for key, val in (("logo", a.logo), ("logoColor", a.logo_color), ("valueColor", a.value_color), ("labelColor", a.label_color),
                     ("brand", a.brand), ("theme", a.theme), ("font", a.font), ("gradient", a.gradient), ("animate", a.animate)):
        if val:
            p.append((key, val))
    if a.dynamic_json:
        p.append(("url", a.dynamic_json))
        p.append(("query", a.query or "$"))
        for key, val in (("prefix", a.prefix), ("suffix", a.suffix), ("label", a.label)):
            if val:
                p.append((key, val))
    if a.split:
        p.append(("split", "true"))
    if a.status_dot:
        p.append(("statusDot", "true"))
    for kv in a.param or []:
        k, _, v = kv.partition("=")
        p.append((k, v))
    return urllib.parse.urlencode(p, quote_via=urllib.parse.quote, safe=",")


def build(a, mode):
    if mode == "light" and getattr(a, "logo_color_light", None):
        a.logo_color = a.logo_color_light
    if mode == "dark" and getattr(a, "logo_color_dark", None):
        a.logo_color = a.logo_color_dark
    ext = "" if a.ext == "shields.json" else "." + a.ext
    tail = "/shields.json" if a.ext == "shields.json" else ""
    return f"{BASE}/{path(a)}{tail}{ext}?{query(a, mode)}".rstrip("?")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    for flag in ("logo-color-light", "logo-color-dark", "label", "message", "color", "provider", "dynamic-json", "query", "prefix", "suffix", "https", "brand", "logo", "logo-color",
                 "value-color", "label-color", "theme", "font", "gradient", "alt", "link"):
        ap.add_argument("--" + flag)
    ap.add_argument("--group", nargs="+")
    ap.add_argument("--platform", choices=sorted(PLATFORMS))
    ap.add_argument("--variant", default="secondary", help="secondary(default) outline ghost default branded destructive")
    ap.add_argument("--size", default="sm")
    ap.add_argument("--animate", choices=["pulse", "glow", "shimmer"])
    ap.add_argument("--split", action="store_true")
    ap.add_argument("--status-dot", action="store_true")
    ap.add_argument("--param", action="append", help="extra KEY=VALUE query parameter, repeatable")
    ap.add_argument("--ext", default="svg", choices=["svg", "png", "json", "shields.json"])
    ap.add_argument("--mode", default="both", choices=["both", "light", "dark", "single"])
    ap.add_argument("--format", default="html", choices=["html", "md", "url", "json"])
    a = ap.parse_args()
    a.dynamic_json = getattr(a, "dynamic_json")

    if a.platform:
        msg, color, logo, lcolor = PLATFORMS[a.platform]
        a.message, a.color = a.message or msg, a.color or color
        a.logo, a.logo_color = a.logo or logo, a.logo_color or lcolor
    alt = a.alt or " ".join(x for x in (a.label, a.message) if x) or a.provider or (a.group and " + ".join(a.group)) or "badge"

    if a.mode == "both":
        light, dark = build(a, "light"), build(a, "dark")
        e = lambda u: u.replace("&", "&amp;")  # valid HTML attribute text (GitHub accepts both)
        pic = f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{e(dark)}" />\n  <img alt="{alt}" src="{e(light)}" />\n</picture>'
        html = f'<a href="{a.link}">{pic}</a>' if a.link else pic
        md = f"[![{alt}]({light})]({a.link})" if a.link else f"![{alt}]({light})"
    else:
        mode = None if a.mode == "single" else a.mode
        light = dark = build(a, mode)
        img = f'<img alt="{alt}" src="{light.replace("&", "&amp;")}" />'
        html = f'<a href="{a.link}">{img}</a>' if a.link else img
        md = f"[![{alt}]({light})]({a.link})" if a.link else f"![{alt}]({light})"

    if a.format == "url":
        print(light if light == dark else f"light: {light}\ndark:  {dark}")
    elif a.format == "json":
        print(json.dumps({"light": light, "dark": dark, "markdown": md, "html": html}, indent=2))
    else:
        print(md if a.format == "md" else html)
