# Live Set Editing

## Default rule

If the user wants the installed Typinator sets changed, edit the live `.tyset` through Typinator’s AppleScript API.

Do not patch `.tyset/Index` or `X*` files directly unless the user explicitly asks for risky raw package editing.

## Why

`.tyset` directories are application-managed package storage. Typinator keeps internal structure there, and direct file edits are easy to corrupt.

## Safe operations through Typinator scripting

- list rule sets
- find rules by abbreviation
- create rules
- update expansions
- update descriptions/comments
- delete rules
- read back rules for verification

## Verification pattern

After any live change:
1. Re-read the affected rule from Typinator.
2. Confirm abbreviation, expansion, and description/comment.
3. For larger edits, confirm rule counts or spot-check multiple entries.

## Drift Checks

When live sets and export artifacts both matter:

1. Run `scripts/sync_live_and_exports.py`.
2. Review `missing_from_live`, `missing_from_export`, and `expansion_differs` findings.
3. Resolve drift before treating exports as a reliable backup or migration baseline.

## When exports still matter

Exports are still useful when:
- the user wants importable CSV/TXT artifacts
- the user wants content changed in `Direct Exports`
- the user wants a format-preserving export workflow

But exports are not required just to modify the installed Typinator sets.
