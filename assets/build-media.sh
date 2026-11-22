#!/usr/bin/env bash
# Rebuild the README media from source.
#   1. vhs records assets/demo.tape (zsh with fast-syntax-highlighting, Ghostty Breeze colours).
#   2. ffmpeg crops the recording to its content, pads it evenly, and adds a macOS-style
#      window bar (three dots drawn with rsvg-convert), and writes a lossless animated WebP.
#   3. rsvg-convert checks that assets/flow.svg renders.
# Needs: vhs (with ttyd), zsh, zsh-fast-syntax-highlighting, ffmpeg, rsvg-convert.
#   brew install vhs zsh-fast-syntax-highlighting ffmpeg librsvg
set -euo pipefail
cd "$(dirname "$0")/.."

for tool in vhs ffmpeg rsvg-convert; do
  command -v "$tool" >/dev/null || { echo "build-media: $tool not found" >&2; exit 2; }
done

tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

pad=56    # even space around the terminal text (2x scale)
bar=72    # window bar height (2x scale)

# 1. Record, then move the raw recording out of assets/.
vhs assets/demo.tape
mv assets/demo.mp4 "$tmp/raw.mp4"

# 2. Crop to the content: the union of every frame's bounding box of bright pixels (the
#    #1e1e1e background is darker than min_val), then pad evenly and add the window bar.
read -r x1 x2 y1 y2 < <(ffmpeg -hide_banner -i "$tmp/raw.mp4" -vf "bbox=min_val=55" -f null - 2>&1 \
  | grep -o 'x1:[0-9]* x2:[0-9]* y1:[0-9]* y2:[0-9]*' \
  | awk '{split($1,a,":"); split($2,b,":"); split($3,c,":"); split($4,d,":");
          if (NR==1||a[2]<x1) x1=a[2]; if (NR==1||b[2]>x2) x2=b[2];
          if (NR==1||c[2]<y1) y1=c[2]; if (NR==1||d[2]>y2) y2=d[2]}
          END {print x1, x2, y1, y2}')
[ -n "${x1:-}" ] || { echo "build-media: no content found in the recording" >&2; exit 1; }
cw=$((x2 - x1 + 1)); ch=$((y2 - y1 + 1))
# The recording's own background colour, so the padding and the bar blend in exactly.
bg=$(ffmpeg -hide_banner -loglevel error -i "$tmp/raw.mp4" -vf "format=rgb24,crop=1:1:0:0" -frames:v 1 -f rawvideo -pix_fmt rgb24 - | xxd -p | head -c 6)
crop="crop=${cw}:${ch}:${x1}:${y1}"
out_w=$((cw + 2 * pad))
out_h=$((ch + 2 * pad + bar))

cat > "$tmp/bar.svg" <<SVG
<svg xmlns="http://www.w3.org/2000/svg" width="$out_w" height="$bar" viewBox="0 0 $out_w $bar">
  <rect width="$out_w" height="$bar" fill="#$bg"/>
  <circle cx="44" cy="38" r="13" fill="#ff5f57"/>
  <circle cx="84" cy="38" r="13" fill="#febc2e"/>
  <circle cx="124" cy="38" r="13" fill="#28c840"/>
</svg>
SVG
rsvg-convert "$tmp/bar.svg" -o "$tmp/bar.png"

ffmpeg -hide_banner -loglevel error -y -i "$tmp/raw.mp4" -i "$tmp/bar.png" -filter_complex \
  "[0:v]${crop},pad=${out_w}:${out_h}:${pad}:$((pad + bar)):color=0x${bg}[v];[v][1:v]overlay=0:0,fps=25[o]" \
  -map "[o]" -c:v libwebp_anim -lossless 1 -compression_level 6 -loop 0 assets/demo.webp

# 3. Check the diagram.
rsvg-convert -w 940 assets/flow.svg -o "$tmp/flow-check.png" && echo "flow.svg renders"

ls -l assets
