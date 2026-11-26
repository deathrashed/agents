#!/usr/bin/env python3
"""Suggest a README colour palette from a project's logo or icon.

  palette.py assets/icon.webp            # human readable
  palette.py assets/icon.webp --json     # machine readable

Picks the most saturated dominant colour as the accent, the next distinct one as the second accent, and
prints a lightened variant of the accent for small text on a dark surface (with its contrast ratio). Needs
ImageMagick (`magick`). Neutral colours (white, black, grey) are ignored. When the logo has no saturated
colour at all the result says so: ask the owner for an accent instead of guessing.
"""
import argparse
import colorsys
import json
import re
import subprocess
import sys


def hexof(r, g, b):
    return "#%02x%02x%02x" % (r, g, b)


def lum(r, g, b):
    def ch(c):
        c = c / 255.0
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * ch(r) + 0.7152 * ch(g) + 0.0722 * ch(b)


def contrast(a, b):
    la, lb = lum(*a), lum(*b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def histogram(path, colors):
    r = subprocess.run(
        ["magick", path, "-background", "none", "-alpha", "remove", "-alpha", "off", "-resize", "240x240",
         "-colors", str(colors), "-depth", "8", "-format", "%c", "histogram:info:-"],
        capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("palette: ImageMagick could not read %s: %s" % (path, r.stderr.strip()[:300]))
    out = r.stdout
    rows = []
    for line in out.splitlines():
        m = re.match(r"\s*(\d+):.*?#([0-9A-Fa-f]{6})", line)
        if m:
            n = int(m.group(1))
            h = m.group(2)
            rows.append((n, int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    return rows


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("image")
    ap.add_argument("--surface", default="#1e1e1e", help="dark surface the text sits on (default #1e1e1e)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    rows = histogram(a.image, 10)
    total = sum(n for n, *_ in rows) or 1
    cands = []
    for n, r, g, b in rows:
        h, s, v = colorsys.rgb_to_hsv(r / 255.0, g / 255.0, b / 255.0)
        if s < 0.35 or v < 0.35:      # greys, near black, washed-out tints
            continue
        cands.append({"hex": hexof(r, g, b), "share": round(100.0 * n / total, 1), "sat": round(s, 2), "val": round(v, 2),
                      "score": s * v * (n / total) ** 0.5, "rgb": (r, g, b), "hue": h})
    cands.sort(key=lambda c: -c["score"])
    result = {"image": a.image, "accent": None, "accent2": None, "text_accent": None, "note": ""}
    sr = int(a.surface[1:3], 16), int(a.surface[3:5], 16), int(a.surface[5:7], 16)
    if not cands:
        result["note"] = "No saturated colour in the logo: ask the owner which accent to use."
    else:
        acc = cands[0]
        result["accent"] = acc["hex"]
        for c in cands[1:]:
            if abs(c["hue"] - acc["hue"]) > 0.08 and abs(c["hue"] - acc["hue"]) < 0.92:
                result["accent2"] = c["hex"]
                break
        # lighten the accent until it has 4.5:1 contrast on the dark surface (small text)
        r, g, b = acc["rgb"]
        t = 0.0
        while contrast((r, g, b), sr) < 4.5 and t < 1.0:
            t += 0.05
            r2 = int(acc["rgb"][0] + (255 - acc["rgb"][0]) * t)
            g2 = int(acc["rgb"][1] + (255 - acc["rgb"][1]) * t)
            b2 = int(acc["rgb"][2] + (255 - acc["rgb"][2]) * t)
            r, g, b = r2, g2, b2
        result["text_accent"] = hexof(r, g, b)
        result["contrast_on_surface"] = round(contrast((r, g, b), sr), 1)
        result["candidates"] = [{k: c[k] for k in ("hex", "share", "sat")} for c in cands[:5]]
        result["note"] = "accent = badges, icons, links; text_accent = small text on the dark surface"
    if a.json:
        print(json.dumps(result, indent=2))
    else:
        print("accent      :", result["accent"])
        print("accent2     :", result["accent2"])
        print("text_accent :", result["text_accent"], "(contrast %s on %s)" % (result.get("contrast_on_surface"), a.surface))
        print(result["note"])


if __name__ == "__main__":
    sys.exit(main())
