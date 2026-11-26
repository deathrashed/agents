# Core Typinator Doc Notes

## Local authority

Primary local authority lives in:
- `Includes/Documentation`
- `Includes/Text`

Use Ergonis-origin docs first for scripting and regex behavior, then use local derivative notes/examples for patterns and project conventions.

## Authoritative syntax and behavior

1. Input fields:
- Text: `{{?Label}}`
- Default: `{{?Label<default>}}`
- Empty default: `{{?Label<>}}`
- Multi-line: `{{?Label//#5}}`
- Alternatives: `{{?Label(A|B|C)}}`
- Mapped alternatives: `{{?Label(A:Expanded A|B:Expanded B)}}`
- Checkbox/option: `{{?Label(1:Checked|0:Unchecked)}}`

2. Variables:
- Assign literal: `{{var=value}}`
- Assign from field: `{{var=?Label(...)}}`
- Reuse: `{{var}}`

3. Dialog-only UI tokens:
- Section header: `{{?*Section*}}`
- Separator: `{{?--}}`
- Helper text: `{{?_help text_}}`
- Comment: `{{-- comment --}}`

4. Literal brace escaping:
- Literal `{M}` becomes `{.M.}`
- For mixed literal braces and real markers, escape only the literal brace pair that would otherwise be misread.

5. Defaults and remembered values:
- Without an explicit default, Typinator tends to remember the last entered/selected value.
- Use `<>` when you want the field to start empty each time.

6. Script placeholder behavior:
- Typinator placeholders use `{Scripts/... argument}`
- One argument only
- Paths with spaces are fragile when combined with parameters
- No-space wrappers are often the safest pattern

7. Live set editing:
- `.tyset` directories are live package data
- Direct raw editing of package internals is unsafe
- Use Typinator’s AppleScript API for live rule creation, updates, deletions, and descriptions
