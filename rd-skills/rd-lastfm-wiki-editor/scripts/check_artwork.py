#!/usr/bin/env python3
"""Inspect local JPEG/PNG/GIF files for image type, dimensions and size.

No external requests. No rights, authenticity, or Last.fm acceptance checks.
Run: python3 scripts/check_artwork.py /path/to/image
"""

from __future__ import annotations

import argparse
from pathlib import Path
import struct
import sys

JPEG_SOF = {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}


def identify_image(data: bytes) -> tuple[str, int | None, int | None]:
    """Return (format, width, height); reject unknown/truncated headers."""
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        if len(data) < 24 or data[12:16] != b"IHDR":
            raise ValueError("truncated or malformed PNG IHDR")
        width, height = struct.unpack(">II", data[16:24])
        if not width or not height:
            raise ValueError("PNG has zero dimension")
        return "PNG", width, height

    if data.startswith((b"GIF87a", b"GIF89a")):
        if len(data) < 10:
            raise ValueError("truncated GIF header")
        width, height = struct.unpack("<HH", data[6:10])
        if not width or not height:
            raise ValueError("GIF has zero dimension")
        return "GIF", width, height

    if data.startswith(b"\xff\xd8"):
        pos = 2
        while pos < len(data):
            if data[pos] != 0xFF:
                pos += 1
                continue
            while pos < len(data) and data[pos] == 0xFF:
                pos += 1
            if pos >= len(data):
                break
            marker = data[pos]
            pos += 1
            if marker in (0xD8, 0xD9, 0x01) or 0xD0 <= marker <= 0xD7:
                continue
            if marker == 0xDA:  # start of compressed scan; SOF should already have appeared
                break
            if pos + 2 > len(data):
                break
            size = struct.unpack(">H", data[pos:pos + 2])[0]
            if size < 2 or pos + size > len(data):
                break
            if marker in JPEG_SOF:
                if size < 7:
                    raise ValueError("malformed JPEG frame header")
                height, width = struct.unpack(">HH", data[pos + 3:pos + 7])
                if not width or not height:
                    raise ValueError("JPEG has zero dimension")
                return "JPEG", width, height
            pos += size
        raise ValueError("JPEG frame dimensions not found (possibly truncated)")

    raise ValueError("unrecognized image header; expected JPEG, PNG or GIF")


def inspect(path: Path) -> dict[str, int | str]:
    size_bytes = path.stat().st_size
    # Reading local files only, never fetching image URLs.
    data = path.read_bytes()
    fmt, width, height = identify_image(data)
    return {"format": fmt, "width": width, "height": height, "size_bytes": size_bytes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", help="Locally available image; no downloading or rights determination")
    args = parser.parse_args(argv)
    try:
        props = inspect(Path(args.file))
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(f"Format: {props['format']}")
    print(f"Dimensions: {props['width']} x {props['height']} pixels")
    print(f"File size: {props['size_bytes']} bytes")
    print("Rights: NOT CHECKED; verify permissions before manual Last.fm upload.")
    print("Last.fm acceptance: NOT CHECKED; confirm current site requirements.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
