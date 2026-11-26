#!/usr/bin/env python3
"""Generic, standard-library README metrics publisher. Run in the target repository.

Metric configuration is explicit and auditable; no arbitrary shell command execution.
"""
import argparse
import fnmatch
import json
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


def git_files(root):
    raw = subprocess.check_output(['git', 'ls-files', '-z'], cwd=root)
    return sorted({p.decode('utf-8') for p in raw.split(b'\0') if p})


def selected(paths, patterns, excludes):
    return [p for p in paths if any(fnmatch.fnmatchcase(p, x) for x in patterns)
            and not any(fnmatch.fnmatchcase(p, x) for x in excludes)]


def value_at(data, dotpath):
    value = data
    for component in dotpath.split('.'):
        value = value[int(component)] if isinstance(value, list) else value[component]
    return value


def evaluate(root, tracked, definition):
    kind = definition['type']
    if kind == 'json_value':
        src = (root / definition['path']).resolve()
        if not src.is_relative_to(root.resolve()):
            raise ValueError('JSON path escapes repository')
        if not src.is_file():
            raise FileNotFoundError(src)
        value = value_at(json.loads(src.read_text(encoding='utf-8')), definition['key'])
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError('json_value must resolve to a numeric value')
        return value
    patterns = definition.get('include', [])
    if not patterns:
        raise ValueError('include patterns are required')
    matches = selected(tracked, patterns, definition.get('exclude', []))
    files = [p for p in matches if (root / p).is_file()]
    if kind == 'files':
        return len(files)
    if kind == 'directories':
        # count matched directory names explicitly, or unique parent dirs of matching files
        depth = int(definition.get('parent_depth', 1))
        return len({str(Path(p).parents[depth - 1]) for p in files})
    if kind == 'lines':
        return sum(len((root / p).read_bytes().splitlines()) for p in files)
    if kind == 'bytes':
        return sum((root / p).stat().st_size for p in files)
    if kind == 'regex_matches':
        regex = re.compile(definition['pattern'], flags=re.MULTILINE)
        return sum(len(regex.findall((root / p).read_text(encoding='utf-8', errors='replace'))) for p in files)
    raise ValueError(f'Unknown metric type: {kind}')


def main():
    ap = argparse.ArgumentParser(description='Generate general-purpose README metrics and history')
    ap.add_argument('--root', type=Path, default=Path.cwd())
    ap.add_argument('--config', default='.readme-metrics.json')
    ap.add_argument('--output-dir', default='stats')
    ap.add_argument('--date', help='UTC date override for testing (YYYY-MM-DD)')
    args = ap.parse_args()
    root = args.root.resolve()
    cfg = json.loads((root / args.config).read_text(encoding='utf-8'))
    paths = git_files(root)
    counts = {}
    for name, spec in cfg['metrics'].items():
        if not re.fullmatch(r'[a-z][a-z0-9_]*', name):
            raise ValueError('Metric names must be lowercase snake_case')
        try:
            counts[name] = evaluate(root, paths, spec)
        except Exception as e:
            raise RuntimeError(f'Metric {name!r} failed: {e}') from e
    today = args.date or datetime.now(timezone.utc).date().isoformat()
    datetime.strptime(today, '%Y-%m-%d')
    out = (root / args.output_dir).resolve()
    if not out.is_relative_to(root):
        raise ValueError('output directory must be inside the repository')
    out.mkdir(parents=True, exist_ok=True)
    latest = {'updated': today, **counts}
    latest_file, hist_file = out / 'badges.json', out / 'history.json'
    previous = json.loads(hist_file.read_text(encoding='utf-8')).get('history', []) if hist_file.exists() else []
    previous = [p for p in previous if p.get('date') != today]
    previous.append({'date': today, **counts})
    previous.sort(key=lambda x: x['date'])
    latest_file.write_text(json.dumps(latest, indent=2) + '\n', encoding='utf-8')
    hist_file.write_text(json.dumps({'history': previous}, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(latest, indent=2))


if __name__ == '__main__':
    main()
