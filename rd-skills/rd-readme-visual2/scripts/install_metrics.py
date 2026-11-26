#!/usr/bin/env python3
"""Install repository metrics assets from this skill into a target Git repository.

Does not overwrite existing files without --force. Does not run the collector,
modify README or commit changes.
"""
import argparse
import shutil
import subprocess
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
ASSETS = {
    SKILL / 'scripts/repo_metrics.py': Path('scripts/repo_metrics.py'),
    SKILL / 'templates/readme-metrics.example.json': Path('.readme-metrics.json'),
    SKILL / 'templates/readme-metrics.yml': Path('.github/workflows/readme-metrics.yml'),
}


def install(target, *, force=False, dry_run=False):
    root = target.resolve()
    if not root.is_dir():
        raise ValueError(f'Not a directory: {root}')
    if not (root / '.git').exists():
        subprocess.run(['git', 'rev-parse', '--show-toplevel'], cwd=root, check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for source, relative in ASSETS.items():
        dest = root / relative
        if dest.exists() and not force:
            print(f'SKIP (exists): {dest}')
            continue
        print(f'{"PLAN" if dry_run else "COPY"}: {source.name} -> {dest}')
        if not dry_run:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, dest)
    print('Review .readme-metrics.json and the default branch in the workflow before enabling.')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('repository', type=Path)
    p.add_argument('--force', action='store_true', help='overwrite existing installed files')
    p.add_argument('--dry-run', action='store_true')
    a = p.parse_args()
    install(a.repository, force=a.force, dry_run=a.dry_run)


if __name__ == '__main__':
    main()
