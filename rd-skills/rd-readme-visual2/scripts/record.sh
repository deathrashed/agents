#!/usr/bin/env bash
# record.sh TAPE OUT.webp [PAD] [BAR]
# Record a vhs tape (written by make-tape.py) and turn it into a sharp, evenly padded, lossless animated
# WebP with a macOS-style window bar. Run it from the repo root. Needs vhs (with ttyd), zsh, ffmpeg with
# libwebp, rsvg-convert. PAD and BAR are in pixels at the tape's 2x scale (defaults 56 and 72).
set -euo pipefail

tape=${1:?usage: record.sh TAPE OUT.webp [PAD] [BAR]}
out=${2:?usage: record.sh TAPE OUT.webp [PAD] [BAR]}
pad=${3:-56}
bar=${4:-72}

for tool in vhs ffmpeg rsvg-convert; do
  command -v "$tool" >/dev/null || { echo "record: $tool not found" >&2; exit 2; }
done
raw=$(awk '$1=="Output"{print $2; exit}' "$tape")
[ -n "$raw" ] || { echo "record: no Output line in $tape" >&2; exit 2; }
mkdir -p "$(dirname "$raw")" "$(dirname "$out")"

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

vhs "$tape"

# Crop to the content: union of every frame's bounding box of bright pixels (the dark background is below
# min_val), then pad evenly and add the window bar.
read -r x1 x2 y1 y2 < <(ffmpeg -hide_banner -i "$raw" -vf "bbox=min_val=55" -f null - 2>&1 \
  | grep -o 'x1:[0-9]* x2:[0-9]* y1:[0-9]* y2:[0-9]*' \
  | awk '{split($1,a,":"); split($2,b,":"); split($3,c,":"); split($4,d,":");
          if (NR==1||a[2]<x1) x1=a[2]; if (NR==1||b[2]>x2) x2=b[2];
          if (NR==1||c[2]<y1) y1=c[2]; if (NR==1||d[2]>y2) y2=d[2]}
          END {print x1, x2, y1, y2}')
[ -n "${x1:-}" ] || { echo "record: no content found in the recording" >&2; exit 1; }
cw=$((x2 - x1 + 1)); ch=$((y2 - y1 + 1))
bg=$(ffmpeg -hide_banner -loglevel error -i "$raw" -vf "format=rgb24,crop=1:1:0:0" -frames:v 1 -f rawvideo -pix_fmt rgb24 - | xxd -p | head -c 6)
out_w=$((cw + 2 * pad)); out_h=$((ch + 2 * pad + bar))
r=$((bar * 13 / 72)); cy=$((bar / 2))
cat > "$tmp/bar.svg" <<SVG
<svg xmlns="http://www.w3.org/2000/svg" width="$out_w" height="$bar" viewBox="0 0 $out_w $bar">
  <rect width="$out_w" height="$bar" fill="#$bg"/>
  <circle cx="$((bar * 44 / 72))" cy="$cy" r="$r" fill="#ff5f57"/>
  <circle cx="$((bar * 84 / 72))" cy="$cy" r="$r" fill="#febc2e"/>
  <circle cx="$((bar * 124 / 72))" cy="$cy" r="$r" fill="#28c840"/>
</svg>
SVG
rsvg-convert "$tmp/bar.svg" -o "$tmp/bar.png"

ffmpeg -hide_banner -loglevel error -y -i "$raw" -i "$tmp/bar.png" -filter_complex \
  "[0:v]crop=${cw}:${ch}:${x1}:${y1},pad=${out_w}:${out_h}:${pad}:$((pad + bar)):color=0x${bg}[v];[v][1:v]overlay=0:0,fps=25[o]" \
  -map "[o]" -c:v libwebp_anim -lossless 1 -compression_level 6 -loop 0 "$out"
rm -f "$raw"; rmdir "$(dirname "$raw")" 2>/dev/null || true
echo "wrote $out ($(wc -c < "$out" | tr -d ' ') bytes, ${out_w}x${out_h}; display it at half that width)"
