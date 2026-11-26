# Master Menu And Picker Patterns

## Problem

Large sets with complex expansion payloads cannot safely be embedded in one giant Typinator options mapping.

## Recommended solutions

### CSV-lookup master menu

Use this when the payloads are large, multiline, or difficult to embed safely:

1. Dropdown lists abbreviations.
2. Selection stored in `{{sel}}`.
3. Inline shell/python reads the CSV and outputs matching expansion text.

Important limitation:

- This pattern is only safe when the lookup source already contains final plain-text
  output.
- Do not aim it at exported live Typinator rules that still contain `{{?...}}`
  forms, shell blocks, or script expansions, because the returned text is inserted
  literally and will not be reinterpreted as a fresh Typinator expansion.
- For form-heavy or script-heavy live rules, use a two-stage router or generate a
  dedicated plain-text reference source first.

## Why it works

- Stable with complex/multiline payloads
- No delimiter collisions in option values
- One-abbreviation discovery UX

## Minimal shape

```typinator
{{sel=?Abbreviation(a:a|b:b|c:c)}}
{/Shell
python3 - <<'PY'
import csv
path = '/absolute/path/to/set.csv'
target = "{{sel}}"
with open(path, encoding='utf-8', newline='') as f:
    for row in csv.reader(f):
        if row and row[0] == target:
            print(row[1], end='')
            break
PY
}
```

### Grouped picker

Use this when the outputs are small but numerous and user-facing selection matters:

1. Split the menu into category dropdowns.
2. Keep labels human-readable.
3. Use explicit empty defaults `<>` when you do not want Typinator to remember the prior selection.
4. Remove unrelated helper menus from the same picker when they belong in their own abbreviation.

## Notes

- Absolute CSV path is required for reliability.
- Keep source CSV in a stable location.
- Includes can host helper scripts and lookup files.
- For installed live sets, prefer direct `.tyset` updates and keep exports only when needed.
