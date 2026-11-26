# Script Manifest

The script manifest is the canonical mapping layer for Typinator script paths used by exports and large migration work.

## Purpose

1. Prevent alias-path drift in exported CSVs.
2. Preserve compatibility history while enforcing canonical runtime paths.
3. Support hard-fail validation for deprecated alias usage.
4. Provide a stable canonical path layer when old aliases or renamed script files still exist.

## Format

CSV with headers:

- `alias_path`
- `canonical_path`
- `status` (`active` or `deprecated`)
- `category`
- `interactive_allowed` (`yes`, `no`, or `unknown`)

## Generation

```bash
python3 scripts/build_script_manifest.py \
  --includes-root /Users/rd/.config/typinator/Sets/Includes
```

Default output path:

`/Users/rd/.config/typinator/Sets/Includes/Documentation/Generated/script-manifest.csv`

## Usage rules

1. `status=active` rows define supported runtime paths.
2. `status=deprecated` rows identify alias/legacy paths that must not appear in final exports.
3. Always rewrite exports to `canonical_path` before removing aliases.
4. Run export validation with `--manifest` before marking work complete.
5. Prefer no-space canonical/runtime paths when placeholders need parameters.
