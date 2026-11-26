# Typinator Runtime Structure

## Primary runtime root

`/Users/rd/.config/typinator/Sets`

## Important subpaths

- Includes root:
`/Users/rd/.config/typinator/Sets/Includes`
- Includes documentation:
`/Users/rd/.config/typinator/Sets/Includes/Documentation`
- Includes text resources:
`/Users/rd/.config/typinator/Sets/Includes/Text`
- Includes scripts:
`/Users/rd/.config/typinator/Sets/Includes/Scripts`
- Exported sets:
`/Users/rd/.config/typinator/Sets/Includes/Exported`
- Direct-export baseline:
`/Users/rd/.config/typinator/Sets/Includes/Exported/Direct Exports`

## Active set storage

Each live Typinator set is a `.tyset` directory under:
`/Users/rd/.config/typinator/Sets/*.tyset`

These are application-managed package directories. Treat them as live runtime data, not casual text-edit targets.

## Practical implications

1. `Includes/Documentation` and `Includes/Text` are the primary local knowledge base for Typinator behavior, syntax, and patterns.
2. `Includes/Scripts` is the runtime script tree used by live placeholders.
3. `Direct Exports` is the import-format authority for CSV/TXT exports.
4. Live set changes should generally be applied through Typinator’s AppleScript API.
5. Export changes should preserve dialect, quoting, encoding, and column shape unless explicit format migration is requested.
6. Prefer one organized canonical `Scripts/` tree.
7. For placeholders with parameters, filenames with spaces are fragile; prefer wrapper scripts or no-space canonical names.
