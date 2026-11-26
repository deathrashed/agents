# Pattern Library

Use these as preferred starting points when authoring or refactoring Typinator content.

## Compact picker

- Use one abbreviation for the picker entry point.
- Keep labels readable.
- Use `label:value` only when inserted text must differ from the label.
- Split into categories once a picker grows past roughly 15 to 20 options.

## Script-backed transform

- Use a single Typinator parameter.
- Keep the runtime script non-interactive.
- Prefer a no-space canonical script path.
- Use for transforms, extraction, formatting, or conversions that become brittle inline.

## Reference-backed lookup

- Store runtime lookup data in `Includes/Reference` or `Includes/Text` depending on whether it behaves like data or reusable text.
- Keep source rows simple, usually `key<TAB>value`.
- Let the wrapper script handle normalization and missing-key cancellation.

## Master menu

- Use one menu row per set, not multiple overlapping menus.
- Keep the menu as a navigational helper, not a dumping ground for every variant.
- Rebuild when abbreviation inventory changes substantially.

## Live-set maintenance

- Use Typinator scripting for installed rule changes.
- Read back the changed rule after mutation.
- Keep comments/descriptions synchronized with current behavior.
