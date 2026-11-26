#!/usr/bin/env python3
"""Fill templates/demo.tape.tmpl: a vhs tape styled like the owner's terminal.

  make-tape.py --command 'scripts/agents-check | sed -n "1,14p"' --wait token_tools \\
               --name rd-agents --folder-rgb 29,154,243 --chevron-rgb 149,87,176 \\
               --export FORCE_COLOR=1 --out assets/demo.tape --output assets/.raw/demo.mp4

Colours come from the owner's Ghostty config (~/.config/ghostty/config: background, foreground, palette
lines, theme name). Breeze is built in; any other theme needs `palette = N=#hex` lines in the config or
--palette-json. Pick --folder-rgb / --chevron-rgb from the owner's prompt (starship.toml) or the project's accent.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TMPL = os.path.join(os.path.dirname(HERE), "templates", "demo.tape.tmpl")

BREEZE = ["#31363b", "#ed1515", "#11d116", "#f67400", "#1d99f3", "#9b59b6", "#1abc9c", "#eff0f1",
          "#7f8c8d", "#c0392b", "#1cdc9a", "#fdbc4b", "#3daee9", "#8e44ad", "#16a085", "#fcfcfc"]
DEFAULT = ["#000000", "#cd3131", "#0dbc79", "#e5e510", "#2472c8", "#bc3fbc", "#11a8cd", "#e5e5e5",
           "#666666", "#f14c4c", "#23d18b", "#f5f543", "#3b8eea", "#d670d6", "#29b8db", "#ffffff"]
NAMES = ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white",
         "brightBlack", "brightRed", "brightGreen", "brightYellow", "brightBlue", "brightMagenta", "brightCyan", "brightWhite"]


def ghostty_theme(path):
    pal = None
    bg, fg, theme = "#1e1e1e", "#eff0f1", None
    explicit = {}
    if os.path.exists(path):
        for line in open(path, encoding="utf-8", errors="ignore"):
            line = line.strip()
            if line.startswith("#") or "=" not in line:
                continue
            k, v = [x.strip() for x in line.split("=", 1)]
            if k == "background":
                bg = v
            elif k == "foreground":
                fg = v
            elif k == "theme":
                theme = v
            elif k == "palette":
                m = re.match(r"(\d+)=(#[0-9a-fA-F]{6})", v)
                if m:
                    explicit[int(m.group(1))] = m.group(2)
    if theme and theme.lower().startswith("breeze"):
        pal = list(BREEZE)
    elif explicit:
        pal = [explicit.get(i, DEFAULT[i]) for i in range(16)]
    else:
        pal = list(DEFAULT)
    for i, c in explicit.items():
        pal[i] = c
    t = {"name": "ghostty " + (theme or "config")}
    for i, n in enumerate(NAMES):
        t[n] = pal[i]
    t.update({"background": bg, "foreground": fg, "selection": pal[0], "cursor": fg})
    return t


def typed(cmd):
    if '"' not in cmd:
        return '"%s"' % cmd
    if "`" not in cmd:
        return "`%s`" % cmd
    sys.exit("make-tape: the command contains both \" and `; simplify it")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--command", required=True)
    ap.add_argument("--wait", default="", help="regex that appears when the command has finished (recommended)")
    ap.add_argument("--wait-secs", type=int, default=0, help="fixed wait when there is no --wait pattern")
    ap.add_argument("--name", required=True, help="folder name shown in the prompt")
    ap.add_argument("--folder-rgb", default="29,154,243")
    ap.add_argument("--chevron-rgb", default="149,87,176")
    ap.add_argument("--chevron", default="›")
    ap.add_argument("--export", action="append", default=[], help="KEY=VALUE exported before the command (repeatable)")
    ap.add_argument("--highlight", default="/opt/homebrew/share/zsh-fast-syntax-highlighting/fast-syntax-highlighting.plugin.zsh",
                    help="syntax-highlighting plugin to source ('' to skip)")
    ap.add_argument("--ghostty-config", default=os.path.expanduser("~/.config/ghostty/config"))
    ap.add_argument("--palette-json", help="JSON file with a full vhs theme, overrides Ghostty")
    ap.add_argument("--font-size", type=int, default=36)
    ap.add_argument("--width", type=int, default=1680)
    ap.add_argument("--height", type=int, default=880)
    ap.add_argument("--padding", type=int, default=28)
    ap.add_argument("--out", default="assets/demo.tape")
    ap.add_argument("--output", default="assets/.raw/demo.mp4", help="raw mp4 path, relative to the repo root (record.sh deletes it)")
    a = ap.parse_args()
    if os.path.isabs(a.output):
        sys.exit("make-tape: --output must be relative to the repo root (vhs cannot parse long absolute Output paths)")

    theme = json.load(open(a.palette_json)) if a.palette_json else ghostty_theme(a.ghostty_config)
    hl = ""
    if a.highlight and os.path.exists(a.highlight):
        hl = 'Type "source %s"\nEnter\n' % a.highlight
    exports = "".join('Type "export %s"\nEnter\n' % e for e in a.export)
    wait = ("Wait+Screen@60s /%s/" % a.wait) if a.wait else ("Sleep %ds" % (a.wait_secs or 6))
    t = open(TMPL, encoding="utf-8").read()
    subs = {
        "OUTPUT": a.output, "THEME_JSON": json.dumps(theme), "FONT_SIZE": a.font_size, "WIDTH": a.width,
        "HEIGHT": a.height, "PADDING": a.padding, "PROMPT_NAME": a.name, "FOLDER_RGB": a.folder_rgb.replace(",", ";"),
        "CHEVRON_RGB": a.chevron_rgb.replace(",", ";"), "CHEVRON": a.chevron, "HIGHLIGHT": hl, "EXPORTS": exports,
        "COMMAND": typed(a.command), "WAIT": wait,
    }
    for k, v in subs.items():
        t = t.replace("{{%s}}" % k, str(v))
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    open(a.out, "w", encoding="utf-8").write(t)
    print("wrote", a.out)


if __name__ == "__main__":
    sys.exit(main())
