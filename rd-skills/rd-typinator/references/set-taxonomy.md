# Typinator Set Taxonomy

## Practical groups

- Templates and forms
- Pickers and selector sets
- Scripts and automation
- Paths and system helpers
- Text transforms and clipboard tools
- Domain-specific sets such as music, web, genres, or yt-dlp
- Test/experimental sets

## Recommended naming pattern for new abbreviations

- Menus: `...menu`
- Pickers: `...pick`
- Wrapper/selectors in dedicated picker sets: `>name`
- Test variants in test sets rather than production sets

## Recommended set-level strategy

- Keep experimental abbreviations in dedicated test sets.
- Promote to production sets after validation.
- Keep picker-specific abbreviations in dedicated picker sets when they start cluttering domain sets.
- Keep one concise master menu or picker per large set when it improves discoverability.
