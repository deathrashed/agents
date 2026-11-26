#!/usr/bin/env python3
"""Generate a dark terminal-window README banner (assets/header.svg).

One flat dark window (traffic-light bar, centred title) holding the project's wordmark, an optional logo
beside it, a subtitle (white words, accent dots) and a typed command with its real listing underneath.
Calm on purpose: no glows, grid, scanlines or glitch. The images are embedded as data: URIs because an
SVG shown through <img> cannot load files. Reduced motion shows the finished frame.

  header.py --wordmark assets/wordmark.webp --accent '#ffda00' --subtitle 'rules|skills|plugins' \\
            --command 'ls ~/.agents' --listing 'AGENTS.md  main.md  rules/' --window-title 'rd-agents  -  zsh'

  header.py --title my-tool --accent '#00c2a8' --subtitle 'fast|small|local'     # no images: text title

Needs ImageMagick (`magick`) only when images are given. Python 3.9+.
"""
import argparse
import base64
import os
import subprocess
import sys
import tempfile

MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,&quot;Liberation Mono&quot;,monospace'


def magick(*args):
    r = subprocess.run(["magick"] + list(args), stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    if r.returncode != 0:
        sys.exit("header: ImageMagick failed (%s): %s" % (" ".join(args[:2]), r.stderr.strip()[:300]))


def dims(path):
    out = subprocess.run(["magick", "identify", "-format", "%w %h", path], capture_output=True, text=True, check=True).stdout.split()
    return int(out[0]), int(out[1])


def b64(path):
    return base64.b64encode(open(path, "rb").read()).decode()


def prep_image(src, work, name, tall, accent, shadow):
    """Trim padding, quantise to PNG8 (about 10-25 KB, clean on dark), and optionally build a clean
    accent-coloured silhouette (holes filled, smooth edges) to use as an offset shadow."""
    main = os.path.join(work, name + ".png")
    magick(src, "-trim", "+repage", "-resize", "x%d" % tall, "-strip", "-colors", "256", "PNG8:" + main)
    sil = None
    if shadow:
        m1 = os.path.join(work, name + "_m1.png")
        m2 = os.path.join(work, name + "_m2.png")
        m3 = os.path.join(work, name + "_m3.png")
        sil = os.path.join(work, name + "_shadow.png")
        magick(src, "-trim", "+repage", "-resize", "x%d" % tall, "-bordercolor", "none", "-border", "6", "-alpha", "extract", "-threshold", "45%", m1)
        magick(m1, "-fill", "gray50", "-draw", "color 0,0 floodfill", m2)
        magick(m2, "-fill", "white", "+opaque", "gray50", "-fill", "black", "-opaque", "gray50", "-shave", "6x6", "+repage", m3)
        w, h = dims(m3)
        magick("-size", "%dx%d" % (w, h), "xc:" + accent, m3, "-alpha", "off", "-compose", "copy-opacity", "-composite", "-strip", sil)
    return main, sil


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", default="assets/header.svg")
    ap.add_argument("--wordmark", help="transparent PNG/WebP of the project name (trimmed automatically)")
    ap.add_argument("--logo", help="optional transparent icon shown left of the wordmark")
    ap.add_argument("--title", default="project", help="text title when there is no wordmark")
    ap.add_argument("--accent", required=True, help="accent colour, e.g. #ffda00 (see palette.py)")
    ap.add_argument("--subtitle", default="", help="words separated by |, shown white with accent dots")
    ap.add_argument("--command", default="ls", help="command that types in the window")
    ap.add_argument("--listing", default="", help="its real output (one line); empty = none")
    ap.add_argument("--window-title", default="zsh")
    ap.add_argument("--bg", default="#1e1e1e")
    ap.add_argument("--bar", default="#181818")
    ap.add_argument("--word-height", type=int, default=220, help="drawn height of the wordmark in px")
    ap.add_argument("--shadow-offset", type=int, default=8)
    ap.add_argument("--no-shadow", action="store_true", help="no accent silhouette behind the wordmark")
    ap.add_argument("--cycle", type=float, default=7.0)
    a = ap.parse_args()

    W = 900
    CYCLE = a.cycle
    ACC = a.accent
    ih = a.word_height
    work = tempfile.mkdtemp()
    imgs = []     # (x, y, w, h, path)
    word_w = 0
    logo_w = 0
    gap = 18
    word = logo = word_shadow = logo_shadow = None
    if a.wordmark:
        word, word_shadow = prep_image(a.wordmark, work, "word", 400, ACC, not a.no_shadow)
        ww0, wh0 = dims(word)
        word_w = round(ww0 / float(wh0) * ih)
    if a.logo:
        logo, logo_shadow = prep_image(a.logo, work, "logo", 400, ACC, False)
        lw0, lh0 = dims(logo)
        logo_w = round(lw0 / float(lh0) * ih)
    have_img = bool(word or logo)
    total_w = logo_w + (gap if (logo and word) else 0) + word_w
    if have_img and total_w > 760:       # logo + wordmark too wide for the window: scale both down together
        k = 760.0 / total_w
        ih = int(ih * k)
        logo_w = int(logo_w * k)
        word_w = int(word_w * k)
        total_w = logo_w + (gap if (logo and word) else 0) + word_w
    iy = 48
    body_h = ih if have_img else 96
    bottom = iy + body_h + (a.shadow_offset if word_shadow else 0)
    sub_y = bottom + 30
    n_cmd = len(a.command)
    TX = 40
    TY = sub_y + 54
    H = TY + (24 if a.listing else 0) + 28
    CHAR_W = 9.62
    START, STEP = 0.6, 0.1
    t_end = START + n_cmd * STEP
    times = [0.0, START / CYCLE]
    widths = [0.0, 0.0]
    for i in range(1, n_cmd + 1):
        times.append((START + i * STEP) / CYCLE)
        widths.append(round(i * CHAR_W, 1))
    reset = (CYCLE - 0.7)
    times += [reset / CYCLE, (reset + 0.05) / CYCLE]
    widths += [round(n_cmd * CHAR_W, 1), 0.0]
    key_times = ";".join("%.4f" % t for t in times) + ";1"
    vals_w = ";".join(str(w) for w in widths) + ";0"
    vals_x = ";".join(str(round(TX + 18 + w, 1)) for w in widths) + ";%d" % (TX + 18)

    parts = []
    add = parts.append
    add('<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 %d %d" width="%d" height="%d" role="img" aria-label="%s">' % (
        W, H, W, H, ("%s: %s. A terminal window types %s and lists %s." % (a.title, a.subtitle.replace("|", ", "), a.command, a.listing)).replace('"', "'")))
    add("<title>%s</title>" % a.title)
    add('<defs><clipPath id="card"><rect width="%d" height="%d" rx="14"/></clipPath>' % (W, H))
    add('<clipPath id="typed"><rect x="%d" y="%d" width="%s" height="26"><animate attributeName="width" dur="%ss" repeatCount="indefinite" calcMode="discrete" keyTimes="%s" values="%s"/></rect></clipPath></defs>' % (
        TX + 18, TY - 20, n_cmd * CHAR_W, CYCLE, key_times, vals_w))
    add("<style>.t{font-family:%s}.cur{fill:#eff0f1;animation:blink 1s steps(1) infinite}@keyframes blink{50%%{opacity:0}}"
        ".stat{display:none}@media (prefers-reduced-motion:reduce){.anim{display:none}.stat{display:inline}.cur{animation:none}}</style>" % MONO)
    add('<g clip-path="url(#card)"><rect width="%d" height="%d" fill="%s"/>' % (W, H, a.bg))
    add('<rect width="%d" height="38" fill="%s"/><path d="M0 38H%d" stroke="rgba(255,255,255,0.07)"/>' % (W, a.bar, W))
    add('<circle cx="24" cy="19" r="6" fill="#ff5f57"/><circle cx="44" cy="19" r="6" fill="#febc2e"/><circle cx="64" cy="19" r="6" fill="#28c840"/>')
    add('<text class="t" x="%s" y="24" font-size="12.5" text-anchor="middle" fill="#7f8c8d">%s</text>' % (W / 2, a.window_title))

    # --- body: images or a text title
    if have_img:
        x = round((W - total_w) / 2.0)
        if logo:
            add('<image x="%d" y="%d" width="%d" height="%d" href="data:image/png;base64,%s"/>' % (x, iy, logo_w, ih, b64(logo)))
            x += logo_w + gap
        if word:
            if word_shadow:
                add('<image x="%d" y="%d" width="%d" height="%d" href="data:image/png;base64,%s"/>' % (x + a.shadow_offset, iy + a.shadow_offset, word_w, ih, b64(word_shadow)))
            add('<image x="%d" y="%d" width="%d" height="%d" href="data:image/png;base64,%s"/>' % (x, iy, word_w, ih, b64(word)))
    else:
        ty = iy + 74
        add('<text class="t" x="%s" y="%d" font-size="76" font-weight="800" text-anchor="middle" fill="%s">%s</text>' % (W / 2, ty + 6, ACC, a.title))
        add('<text class="t" x="%s" y="%d" font-size="76" font-weight="800" text-anchor="middle" fill="#f4f4f7">%s</text>' % (W / 2, ty, a.title))
    if a.subtitle:
        words = [w.strip() for w in a.subtitle.split("|") if w.strip()]
        sub = (' <tspan fill="%s">&#8226;</tspan> ' % ACC).join(words)
        add('<text class="t" x="%s" y="%d" font-size="15" text-anchor="middle" fill="#ffffff" xml:space="preserve">%s</text>' % (W / 2, sub_y, sub))

    # --- typed command and its listing
    add('<text class="t" x="%d" y="%d" font-size="16" font-weight="700" fill="%s">&#8250;</text>' % (TX, TY, ACC))
    add('<g class="anim"><g clip-path="url(#typed)"><text class="t" x="%d" y="%d" font-size="16" fill="#eff0f1">%s</text></g>' % (TX + 18, TY, a.command))
    add('<rect class="cur" x="%s" y="%d" width="8" height="17"><animate attributeName="x" dur="%ss" repeatCount="indefinite" calcMode="discrete" keyTimes="%s" values="%s"/></rect>' % (
        TX + 18 + n_cmd * CHAR_W, TY - 14, CYCLE, key_times, vals_x))
    if a.listing:
        add('<text class="t" x="%d" y="%d" font-size="14" fill="#7f8c8d">%s<animate attributeName="opacity" dur="%ss" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;%.4f;%.4f;0.9;0.93;1"/></text>' % (
            TX + 18, TY + 24, a.listing, CYCLE, t_end / CYCLE + 0.03, t_end / CYCLE + 0.08))
    add('</g><g class="stat"><text class="t" x="%d" y="%d" font-size="16" fill="#eff0f1">%s</text>' % (TX + 18, TY, a.command))
    if a.listing:
        add('<text class="t" x="%d" y="%d" font-size="14" fill="#7f8c8d">%s</text>' % (TX + 18, TY + 24, a.listing))
    add("</g></g></svg>")
    svg = "\n".join(parts) + "\n"
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(svg)
    print("wrote %s (%d KB, %dx%d)" % (a.out, len(svg) // 1024, W, H))


if __name__ == "__main__":
    sys.exit(main())
