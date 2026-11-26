## Routing heuristics

Route by the real system being described, not by the shape of the source note.

Prefer:

- existing canonical ownership over new file creation
- splitting mixed notes before merging
- one domain owner file per system

Common signals:

- Typinator abbreviations, syntax, sets, includes -> `app/typinator.txt`
- Obsidian vault structure, plugin workflows, note behavior ->
  `directory/obsidian.txt`
- Shell setup, prompt behavior, aliases, terminal tooling -> `util/shell.txt`
- Scripts directory organization, script taxonomy, repo-vault relationships ->
  `directory/scripts.txt`
- Keyboard Maestro automation -> `app/keyboard-maestro.txt`
- Karabiner remaps and HID behavior -> `app/karabiner.txt`
- System profile or machine-level environment summary ->
  `system/system-profile.txt`

Path-driven examples:

- `/Volumes/Apfspace/Icons` -> `directory/icons.txt`
- `/Volumes/Apfspace` -> `directory/apfspace.txt`
- `/Users/rd/Scripts` -> `directory/scripts.txt`
- `/Users/rd/.config/karabiner` -> `app/karabiner.txt`
- `/Users/rd/.config/typinator` -> `app/typinator.txt`

## Lifecycle sequence

1. Read governing docs.
2. Read the full staged source.
3. Identify every domain.
4. Inspect likely canonical owners.
5. Merge into canonical files.
6. Update `_docs/STATUS.md`.
7. Archive the original source into `_extracted/•processed/`.

If the source did not come from `_extracted/`:

- process it as an external input
- update canonical files the same way
- update `_docs/STATUS.md`
- do not archive it into `•processed/` by default

## Non-negotiable rules

- `_extracted/` is staging only, never canonical.
- external source paths are valid ingest inputs but are not auto-archived into
  staging history
- Internal cross-references use Directory-root-relative paths only.
- At least one canonical file must be updated for a successful ingest.
- Do not leave concepts partially migrated across sections or files.
