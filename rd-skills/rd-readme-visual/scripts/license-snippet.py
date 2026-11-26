#!/usr/bin/env python3
"""Print a tailored README license block from the gupload license library.

  license-snippet.py --list
  license-snippet.py gpl --variant free-works
  license-snippet.py mit --variant green --install /path/to/repo   # also copies LICENSE

The library lives in gupload at uploads/files/licenses/<id>/ and holds the
filled-in LICENSE text plus snippet.md, green-snippet.md and
free-works-snippet.md where those variants exist.
"""

import argparse
import filecmp
import json
import os
import shutil
import sys

DEFAULT_ROOT = "/Users/rd/Scripts/Riley/gupload/uploads/files/licenses"
VARIANTS = {"standard": "snippet.md", "green": "green-snippet.md", "free-works": "free-works-snippet.md"}


def available(root):
    rows = []
    for name in sorted(os.listdir(root)):
        folder = os.path.join(root, name)
        if not os.path.isfile(os.path.join(folder, "LICENSE")):
            continue
        variants = [v for v, f in VARIANTS.items() if os.path.isfile(os.path.join(folder, f))]
        title = name
        meta = os.path.join(folder, "metadata.json")
        if os.path.isfile(meta):
            with open(meta, encoding="utf-8") as handle:
                title = json.load(handle).get("name", name)
        rows.append((name, title, variants))
    return rows


def install(source, repo, assume_yes):
    target = os.path.join(repo, "LICENSE")
    if os.path.exists(target):
        if filecmp.cmp(source, target, shallow=False):
            print(f"{target} already matches", file=sys.stderr)
            return
        if not assume_yes:
            answer = input(f"{target} exists and differs. Replace it? [y/N] ").strip().lower()
            if answer != "y":
                print("LICENSE left unchanged", file=sys.stderr)
                return
    shutil.copyfile(source, target)
    print(f"copied LICENSE to {target}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("license", nargs="?", help="license id (folder name), e.g. gpl, mit, cc-by")
    parser.add_argument("--variant", choices=VARIANTS, default="standard")
    parser.add_argument("--list", action="store_true", help="list licenses and their variants")
    parser.add_argument("--install", metavar="REPO", help="copy the tailored LICENSE into REPO")
    parser.add_argument("--yes", action="store_true", help="replace an existing LICENSE without asking")
    parser.add_argument("--root", default=DEFAULT_ROOT, help="license library folder")
    args = parser.parse_args()

    if args.list or not args.license:
        for name, title, variants in available(args.root):
            print(f"{name:<11} {title:<45} {', '.join(variants)}")
        return

    folder = os.path.join(args.root, args.license)
    snippet = os.path.join(folder, VARIANTS[args.variant])
    if not os.path.isfile(snippet):
        ids = ", ".join(name for name, _, _ in available(args.root))
        sys.exit(f"no {args.variant} snippet for {args.license!r} (licenses: {ids})")

    with open(snippet, encoding="utf-8") as handle:
        print('<a name="license"></a>\n')
        print(handle.read().rstrip())
    if args.install:
        install(os.path.join(folder, "LICENSE"), args.install, args.yes)


if __name__ == "__main__":
    main()
