# Authentic demo GIF / WebP production

Choose demonstrations that prove a core claim: real command invocation, actual TUI interactions, real file conversion, truthful before/after or UI workflow. Do not use mock terminal output as if it were a recording.

## Capture plan
1. Inspect runnable entry point and safe fixtures; redact tokens, names, paths and secrets.
2. Storyboard 3–8 seconds of one task with one obvious beginning and end. No unexplained mouse flailing.
3. Terminal: use installed VHS or Asciinema + agg if available; run commands to verify. Desktop: capture with native screen recorder, OBS or ffmpeg capture as appropriate; ensure permission and safe content. Never claim recorded evidence unless actual commands ran.
4. Crop tightly; target ~800–1100px width. Preserve legible text at 375px and add a static screenshot.
5. Encode 8–15fps for terminal GIF, choose animated WebP when supported, compare file sizes and browser compatibility. Pillow generator is **illustrative motion** and not proof of real program execution.
6. Optimize with gifsicle/gifski/ffmpeg only when available; verify first/middle/final frames, looping, file sizes and that the GIF doesn't run too fast.

The included `scripts/render_motion_frames.py` makes deterministic illustrated signal-flow animations, not recordings. Use it for explanatory diagrams and tests; use real capture for product demos. Never state an illustrated demo is an application screen recording.

Example: `python3 scripts/render_motion_frames.py --config templates/motion/signal.example.json --output assets/trace.webp --format webp --fps 12 --seconds 3`. Depends on Pillow. Use `<img src="assets/trace.webp" alt="...">` and provide a meaningful static screenshot alongside.
