#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
  cat >&2 <<'USAGE'
Usage: scripts/find-action.sh MacroActionType [search-root]

Examples:
  scripts/find-action.sh ExecuteShellScript
  scripts/find-action.sh PromptForUserInput /Users/rd/.config/keyboard-maestro/km-backups

Searches curated real exports first, then Keyboard Maestro backups when available. Handles XML and binary plist exports by reading through plutil.
USAGE
  exit 2
fi

action="$1"
explicit_root="${2:-}"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKUPS="/Users/rd/.config/keyboard-maestro/km-backups"
pattern="<string>${action}</string>"

if [[ -n "$explicit_root" ]]; then
  search_roots=("$explicit_root")
else
  search_roots=("$ROOT/real-exports" "$ROOT/examples")
  if [[ -d "$BACKUPS" ]]; then
    search_roots+=("$BACKUPS")
  fi
fi

found=0
for dir in "${search_roots[@]}"; do
  [[ -d "$dir" ]] || continue
  while IFS= read -r -d '' file; do
    if plutil -convert xml1 -o - "$file" 2>/dev/null | grep -Fq "$pattern"; then
      printf '%s\n' "$file"
      found=1
    fi
  done < <(find "$dir" -name '*.kmmacros' -print0 2>/dev/null)
done

if [[ "$found" -eq 0 ]]; then
  printf 'No exports found containing MacroActionType %s. Export a tiny macro with that action from Keyboard Maestro and use it as the source of truth.\n' "$action" >&2
  exit 1
fi
