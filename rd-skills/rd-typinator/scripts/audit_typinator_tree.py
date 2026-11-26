#!/usr/bin/env python3
"""Generate a quick Typinator runtime audit report.

Outputs a markdown report for Includes and Sets structure.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime

SETS_ROOT = Path('/Users/rd/.config/typinator/Sets')
INCLUDES = SETS_ROOT / 'Includes'


def list_dirs(base: Path, depth: int = 2):
    out = []
    for p in sorted(base.rglob('*')):
        if p.is_dir() and len(p.relative_to(base).parts) <= depth:
            out.append(p)
    return out


def main() -> int:
    lines = []
    lines.append('# Typinator Runtime Audit')
    lines.append('')
    lines.append(f'Generated: {datetime.now().isoformat(timespec="seconds")}')
    lines.append('')
    lines.append(f'- Sets root: `{SETS_ROOT}`')
    lines.append(f'- Includes root: `{INCLUDES}`')
    lines.append('')

    tysets = sorted(SETS_ROOT.glob('*.tyset'))
    lines.append(f'## Set count: {len(tysets)}')
    for p in tysets:
        lines.append(f'- `{p.name}`')
    lines.append('')

    lines.append('## Includes top-level directories')
    for p in sorted(INCLUDES.iterdir()):
        if p.is_dir():
            lines.append(f'- `{p.name}/`')
    lines.append('')

    scripts = INCLUDES / 'Scripts'
    skripts = INCLUDES / 'Skripts'
    lines.append('## Script path notes')
    lines.append(f'- Scripts exists: `{scripts.exists()}`')
    lines.append(f'- Skripts exists: `{skripts.exists()}`')
    lines.append('')

    out = INCLUDES / 'Documentation' / 'Project' / 'Audits' / 'Typinator Runtime Audit.md'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text('\n'.join(lines), encoding='utf-8')
    print(out)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
