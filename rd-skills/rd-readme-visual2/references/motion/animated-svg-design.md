# Animated SVG design and accessibility

SVG is an image in GitHub README `<img>`, not an interactive JavaScript app. Use paths, text, gradients sparingly, and self-contained CSS animation. Avoid script, remote fonts, external images, foreignObject, event handlers and CSS @import. GitHub's SVG processing can limit features: always test the *actual embedded README*, not only a local browser opened SVG.

## Motion grammars
- **Routing event**: one luminous event follows a real pipeline connection; node labels remain stationary.
- **Pulse reading**: a short waveform pattern conveys periodic sampling; labels never blink.
- **Timeline trace**: time markers are fixed while a cursor traverses ordered events.
- **Blueprint reveal**: a single path draws once, then remains visible; supply a full static version.
- **System orbit**: use only when the product genuinely has a hub-and-satellite architecture; avoid making everything an orbit.
- **Terminal trace**: show accurately captured state; avoid fabricated prompts or cursor loops that suggest real live data.

Use `@media (prefers-reduced-motion: reduce)` to disable animation, and always include `<title>`, `<desc>`, a `viewBox`, readable labels and a static alternative. Prefer transforms/opacity; avoid huge blur or thousands of filter operations. Keep SVG filesize and CPU usage measured. For pure static documentation choose static SVG instead.

Production: `scripts/generate_motion_svg.py --config templates/motion/signal.example.json --style signal --output assets/signal.svg`. Generate static comparison with `--static`. Validate with `scripts/check_motion_svg.py`. Look at both in GitHub dark/light and at mobile widths; transparent vs opaque background must be chosen explicitly.
