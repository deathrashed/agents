# Typinator Syntax and Dialog UX

## Dialog-only tokens

- `{{?*Section*}}`
- `{{?--}}`
- `{{?_Helper text_}}`
- `{{-- Comment --}}`

These are removed on expansion; surrounding blank lines are not.

## Field patterns

- Text: `{{?Label}}`
- Prefill: `{{?Label<default>}}`
- Empty: `{{?Label<>}}`
- Multiline: `{{?Label//#5}}`
- Dropdown: `{{?Label(A|B|C)}}`
- Mapped dropdown: `{{?Label(A:Output A|B:Output B)}}`
- Checkbox: `{{?Flag(1:Yes output|0:No output)<1>}}`

## Defaults and remembered values

- Without an explicit default, Typinator tends to reuse the last entered/selected value.
- Use `<>` when you want a field or popup to start empty every time.
- This matters especially for pickers and grouped symbol menus.

## Common pitfalls

- Symbolic labels (`$`, `=`) create poor dialog UX.
- Huge nested dropdowns with complex payloads are fragile.
- Branch-specific fields in one expansion show all fields in one dialog.
- Raw `|` or `:` inside option labels can break popup parsing.
- Literal braces that would be misread as markers must be escaped with Typinator’s literal-brace form.
- Symbol-heavy labels often make pickers harder to parse and harder to scan.

## Best practice

Use shared fields in single-expansion menus, or use a two-stage router pattern for per-option forms.
Use plain-text menu labels when punctuation-heavy labels start colliding with parser separators.
