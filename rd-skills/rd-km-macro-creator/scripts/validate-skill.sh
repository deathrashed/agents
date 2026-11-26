#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

printf 'Validating bundled Keyboard Maestro macro exports...\n'
if find examples real-exports -name '*.kmmacros' -print -quit | grep -q .; then
  find examples real-exports -name '*.kmmacros' -print0 | xargs -0 -n1 plutil -lint
else
  printf 'No .kmmacros files found under examples/ or real-exports/.\n' >&2
  exit 1
fi

printf '\nChecking for stale lowercase/old documentation references...\n'
stale_refs='actions\.md|macro-structure\.txt|KEYBOARD_MAESTRO_MACRO_GUIDE|TROUBLESHOOTING_AND_PROCESS|tldr\.md'
if rg -n "$stale_refs" SKILL.md README.md docs references real-exports examples templates; then
  printf '\nStale references found. Update them before relying on this skill.\n' >&2
  exit 1
fi

printf '\nChecking required reliability files...\n'
required=(
  "references/ACTIONS.md"
  "references/ACTION-SOURCING.md"
  "references/MACRO-STRUCTURE.txt"
  "docs/MACRO-GUIDE.md"
  "docs/TROUBLESHOOTING.md"
  "docs/TLDR.md"
  "templates/status-menu-wrapper.xml"
  "scripts/find-action.sh"
)
for path in "${required[@]}"; do
  if [[ ! -f "$path" ]]; then
    printf '\nMissing required file: %s\n' "$path" >&2
    exit 1
  fi
done
printf ' OK\n'

printf '\nSkill validation passed. Remember: plutil proves plist syntax only, not Keyboard Maestro import behavior.\n'
