#!/usr/bin/env python3
"""Generate an animated hub-and-spoke map (assets/flow.svg) from a small JSON config.

Use it when many things read or consume one thing (agents reading shared rules, services behind a gateway,
clients of an API). Boxes of files feed a hub; the hub pulses and sends a packet down a spoke to each target,
which pops, lights up and names itself; an optional second lane sends packets to chosen targets and drops a
badge with a drawn tick. Same dark terminal-window frame as header.py. Flat on purpose: no glows or texture.
Everything animates with SMIL + CSS and loops; reduced motion shows the finished frame.

  flow.py config.json            # config keys below; see references/flow-example.json

{
  "out": "assets/flow.svg",
  "window_title": "my-project  -  map",
  "accent": "#ffda00", "accent2": "#e6edf3", "good": "#11d116",
  "source": {"title": "my-project", "chips": ["AGENTS.md", "main.md"]},
  "hub": {"label": "~/.agents", "sub": "hub"},
  "targets": ["Gemini", "Cursor", "Claude"],
  "lane2": {"title": "marketplace/", "chips": ["rd marketplace"], "caption": "claude + codex",
            "to": ["Codex", "Claude"], "badge": "obsidian@rd"},
  "legend": ["symlinks and pointers", "plugin marketplace"]
}
Only "accent", "hub" and "targets" are required. Python 3.9+.
"""
import json
import math
import os
import sys

MONO = 'ui-monospace,SFMono-Regular,Menlo,Consolas,&quot;Liberation Mono&quot;,monospace'
BG = "#1e1e1e"


def hx(c):
    c = c.lstrip("#")
    return int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)


def mix(a, b, t):
    """a * t + b * (1 - t) as a hex colour."""
    ra, ga, ba = hx(a)
    rb, gb, bb = hx(b)
    return "#%02x%02x%02x" % (int(ra * t + rb * (1 - t)), int(ga * t + gb * (1 - t)), int(ba * t + bb * (1 - t)))


def build(cfg):
    W = 940
    CYCLE = 9.0
    ACC = cfg["accent"]
    ACC2 = cfg.get("accent2", "#e6edf3")
    GOOD = cfg.get("good", "#11d116")
    PKT = mix(ACC, "#ffffff", 0.65)
    PKT2 = "#ffffff"
    LIT = mix(ACC, BG, 0.22)
    NODE_LIT = mix(ACC, BG, 0.42)
    POP_STROKE = mix(ACC, "#ffffff", 0.45)
    LIT2 = mix(ACC2, BG, 0.18)
    targets = cfg["targets"]
    n = len(targets)
    src = cfg.get("source")
    lane2 = cfg.get("lane2")
    hub = cfg["hub"]

    step = min(48.0, max(34.0, 330.0 / max(1, n - 1)))
    TOP = 78.0
    BOT = TOP + (n - 1) * step
    chips = (src or {}).get("chips", [])
    src_h = 56 + 28 * len(chips)
    lane_top = 66 + src_h + 44
    lane_chips = (lane2 or {}).get("chips", [])
    lane_h = 74 + 30 * len(lane_chips)
    H = int(max(BOT + 34, (lane_top + lane_h + 24) if lane2 else 0, 360))
    HX = 380
    HR = max(46, int(max(len(hub["label"]) * 8.4, len(hub.get("sub", "hub")) * 6.6) / 2) + 12)   # hub grows to fit its labels
    HY = (TOP + BOT) / 2.0
    RX = 232
    out = []
    add = out.append

    def packet(path, begin, dur, color):
        kt = dur / CYCLE
        add(f'<circle class="pkt" r="4.8" cx="0" cy="0" opacity="0" fill="{color}" filter="url(#glow)">'
            f'<animateMotion path="{path}" dur="{CYCLE}s" begin="{begin:.2f}s" repeatCount="indefinite" calcMode="linear" keyPoints="0;1;1" keyTimes="0;{kt:.4f};1"/>'
            f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;0.01;{kt - 0.006:.4f};{kt:.4f};1" dur="{CYCLE}s" begin="{begin:.2f}s" repeatCount="indefinite"/></circle>')

    def chip(x, y, w, text, delay, cls="chip lit", size=12, h=22):
        add(f'<rect class="{cls}" x="{x}" y="{y}" width="{w}" height="{h}" rx="5" style="animation-delay:{delay:.2f}s"/>')
        add(f'<text class="c" x="{x + 10}" y="{y + h / 2 + 4.2:.1f}" font-size="{size}">{text}</text>')

    names = ", ".join(targets)
    add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
        f'aria-label="{cfg.get("alt", "Map: " + ", ".join(chips) + " feed the " + hub["label"] + " hub, which reaches " + names + ".")}">'.replace("\n", " "))
    add(f'<title>{cfg.get("title", cfg.get("window_title", "map"))}</title>')
    add(f'''<defs><clipPath id="card"><rect width="{W}" height="{H}" rx="14"/></clipPath>
<filter id="glow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2.6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>''')
    add(f'''<style>
.c{{fill:#e6edf3;font-family:{MONO}}}
.t{{fill:#e6edf3;font:600 14px {MONO}}}
.s{{fill:#7f8c8d;font:400 12px {MONO}}}
.nm{{fill:#e6edf3;font:500 12.5px {MONO}}}
.box{{fill:#252526;stroke:rgba(255,255,255,0.14);stroke-width:1.2}}
.chip{{fill:#2d2d2d;stroke:#454545;stroke-width:1}}
.lit{{animation:lit {CYCLE}s cubic-bezier(.22,1,.36,1) infinite}}
@keyframes lit{{0%{{fill:#2d2d2d;stroke:#454545}}4%{{fill:{LIT};stroke:{ACC}}}86%{{fill:{LIT};stroke:{ACC}}}95%,100%{{fill:#2d2d2d;stroke:#454545}}}}
.litb{{animation:litb {CYCLE}s cubic-bezier(.22,1,.36,1) infinite}}
@keyframes litb{{0%{{fill:#2d2d2d;stroke:#454545}}4%{{fill:{LIT2};stroke:{ACC2}}}86%{{fill:{LIT2};stroke:{ACC2}}}95%,100%{{fill:#2d2d2d;stroke:#454545}}}}
.node{{fill:#2d2d2d;stroke:#454545;stroke-width:1.4;animation:node {CYCLE}s cubic-bezier(.22,1,.36,1) infinite}}
@keyframes node{{0%{{fill:#2d2d2d;stroke:#454545;r:12}}3%{{fill:{ACC};stroke:{POP_STROKE};r:16}}8%{{fill:{NODE_LIT};stroke:{ACC};r:12}}86%{{fill:{NODE_LIT};stroke:{ACC};r:12}}95%,100%{{fill:#2d2d2d;stroke:#454545;r:12}}}}
.lab{{opacity:.35;animation:lab {CYCLE}s linear infinite}}
@keyframes lab{{0%{{opacity:.35}}4%,86%{{opacity:1}}95%,100%{{opacity:.35}}}}
.spoke{{fill:none;stroke:{ACC};stroke-width:1.3;stroke-dasharray:3 7;opacity:.5;animation:dash 1.4s linear infinite}}
.plug{{fill:none;stroke:{ACC2};stroke-width:1.6;stroke-dasharray:3 7;opacity:.6;animation:dash 1.4s linear infinite}}
@keyframes dash{{to{{stroke-dashoffset:-20}}}}
.ring{{fill:none;stroke:{ACC};stroke-width:2;transform-box:fill-box;transform-origin:center;opacity:0;animation:ring {CYCLE}s cubic-bezier(.22,1,.36,1) infinite;animation-delay:1.5s}}
@keyframes ring{{0%{{transform:scale(1);opacity:.9}}18%,100%{{transform:scale(1.9);opacity:0}}}}
.tick{{fill:none;stroke:{GOOD};stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round;stroke-dasharray:24;stroke-dashoffset:24;animation:draw {CYCLE}s cubic-bezier(.22,1,.36,1) infinite}}
@keyframes draw{{0%{{stroke-dashoffset:24}}4%,86%{{stroke-dashoffset:0}}95%,100%{{stroke-dashoffset:24}}}}
.badge{{opacity:0;animation:badge {CYCLE}s cubic-bezier(.22,1,.36,1) infinite}}
@keyframes badge{{0%{{opacity:0;transform:translateX(-6px)}}5%,86%{{opacity:1;transform:none}}95%,100%{{opacity:0}}}}
.cur{{fill:{ACC};animation:blink 1.1s steps(1) infinite}}
@keyframes blink{{50%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{
.pkt,.cur,.ring{{display:none}}
.spoke,.plug{{animation:none}}
.lit{{animation:none;fill:{LIT};stroke:{ACC}}}
.litb{{animation:none;fill:{LIT2};stroke:{ACC2}}}
.node{{animation:none;fill:{NODE_LIT};stroke:{ACC}}}
.lab,.badge{{animation:none;opacity:1}}
.tick{{animation:none;stroke-dashoffset:0}}
}}
</style>''')
    add('<g clip-path="url(#card)">')
    add(f'<rect width="{W}" height="{H}" fill="{BG}"/><rect width="{W}" height="38" fill="#181818"/><path d="M0 38H{W}" stroke="rgba(255,255,255,0.08)"/>')
    add('<circle cx="24" cy="19" r="6" fill="#ff5f57"/><circle cx="44" cy="19" r="6" fill="#febc2e"/><circle cx="64" cy="19" r="6" fill="#28c840"/>')
    add(f'<text class="s" x="{W / 2}" y="24" font-size="12.5" text-anchor="middle">{cfg.get("window_title", "map")}</text>')

    # ---- source box with chips, curves and packets into the hub
    fy = []
    if src:
        add(f'<rect class="box" x="24" y="66" width="174" height="{src_h}" rx="10"/>')
        add(f'<text class="t" x="40" y="94">{src["title"]}</text>')
        add(f'<rect class="cur" x="{40 + 8.6 * len(src["title"]) + 6:.0f}" y="81" width="8" height="15"/>')
        for i, nm in enumerate(chips):
            yy = 110 + 28 * i
            fy.append(yy)
            chip(40, yy, 142, nm, 0.2 + i * 0.2)
        for i, yy in enumerate(fy):
            d = f"M184 {yy + 11} C 270 {yy + 11} 290 {HY:.1f} {HX - HR} {HY:.1f}"
            add(f'<path class="spoke" d="{d}"/>')
            packet(d, 0.5 + i * 0.22, 1.1, PKT)

    # ---- spokes and targets (even vertical spacing, bulging right like an arc)
    nodes = []
    for i, nm in enumerate(targets):
        ny = TOP + i * (BOT - TOP) / max(1, n - 1)
        t = (ny - (TOP + BOT) / 2.0) / (((BOT - TOP) / 2.0) or 1)
        nx = HX + 46 + (RX - 46) * math.sqrt(max(0.0, 1 - t * t))
        nodes.append((nm, nx, ny))
        cx_, cy_ = HX + (nx - HX) * 0.55, HY + (ny - HY) * 0.18
        d = f"M{HX} {HY:.1f} Q {cx_:.1f} {cy_:.1f} {nx:.1f} {ny:.1f}"
        add(f'<path class="spoke" d="{d}"/>')
        packet(d, 2.0 + i * 0.24, 0.9, PKT)
    for i, (nm, nx, ny) in enumerate(nodes):
        arrive = 2.0 + i * 0.24 + 0.7
        add(f'<circle class="node" cx="{nx:.1f}" cy="{ny:.1f}" r="12" style="animation-delay:{arrive:.2f}s"/>')
        add(f'<text class="nm lab" x="{nx + 22:.1f}" y="{ny + 4.4:.1f}" style="animation-delay:{arrive:.2f}s">{nm}</text>')

    # ---- hub on top of the spokes
    add(f'<circle class="ring" cx="{HX}" cy="{HY:.1f}" r="{HR}"/>')
    add(f'<circle cx="{HX}" cy="{HY:.1f}" r="{HR}" fill="#1a1a1a" stroke="{ACC}" stroke-width="2"/>')
    add(f'<text class="t" x="{HX}" y="{HY - 2:.1f}" text-anchor="middle" font-size="14">{hub["label"]}</text>')
    add(f'<text class="s" x="{HX}" y="{HY + 16:.1f}" text-anchor="middle" font-size="11">{hub.get("sub", "hub")}</text>')

    # ---- optional second lane: box -> chosen targets, badge with a tick on arrival
    if lane2:
        add(f'<rect class="box" x="24" y="{lane_top}" width="174" height="{lane_h}" rx="10"/>')
        add(f'<text class="t" x="40" y="{lane_top + 28}">{lane2["title"]}</text>')
        for i, nm in enumerate(lane_chips):
            chip(40, lane_top + 42 + 30 * i, 142, nm, 4.2 + i * 0.2, size=11.5)
        if lane2.get("caption"):
            add(f'<text class="s" x="40" y="{lane_top + 42 + 30 * len(lane_chips) + 22}">{lane2["caption"]}</text>')
        sx, sy = 184, lane_top + 42 + 30 * max(0, len(lane_chips) - 1) + 11
        for k, tname in enumerate(lane2.get("to", [])):
            node = next((nd for nd in nodes if nd[0] == tname), None)
            if not node:
                continue
            nm, nx, ny = node
            d = f"M{sx} {sy} C {sx + 120} {sy + 38} {nx - 90:.1f} {ny + 36:.1f} {nx - 14:.1f} {ny + 4:.1f}"
            add(f'<path class="plug" d="{d}"/>')
            base = 4.7 + 0.3 * k
            packet(d, base, 1.3, PKT2)
            if lane2.get("badge"):
                bx, by = nx + 22 + 7.4 * len(nm) + 10, ny
                bw = 8 * len(lane2["badge"]) + 28
                delay = base + 1.2
                add(f'<g class="badge" style="animation-delay:{delay:.2f}s"><rect x="{bx:.1f}" y="{by - 11:.1f}" width="{bw}" height="22" rx="6" fill="{LIT2}" stroke="{ACC2}"/>'
                    f'<text class="c" x="{bx + 8:.1f}" y="{by + 4:.1f}" font-size="11.5">{lane2["badge"]}</text>'
                    f'<path class="tick" d="M{bx + bw - 18:.1f} {by:.1f} l3.6 3.8 l7.2 -8" style="animation-delay:{delay:.2f}s"/></g>')

    # ---- legend, top right
    legend = cfg.get("legend", [])
    for i, text in enumerate(legend[:2]):
        col = ACC if i == 0 else ACC2
        add(f'<circle cx="716" cy="{86 + 22 * i}" r="5" fill="{col}"/><text class="s" x="730" y="{90 + 22 * i}">{text}</text>')
    add('</g></svg>')
    return "\n".join(out) + "\n", W, H


def main():
    if len(sys.argv) != 2 or sys.argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0 if len(sys.argv) == 2 else 2
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    svg, W, H = build(cfg)
    out = os.path.expanduser(cfg.get("out", "assets/flow.svg"))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    open(out, "w", encoding="utf-8").write(svg)
    print("wrote %s (%d KB, %dx%d)" % (out, len(svg) // 1024, W, H))
    return 0


if __name__ == "__main__":
    sys.exit(main())
