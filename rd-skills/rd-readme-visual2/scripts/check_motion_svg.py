#!/usr/bin/env python3
"""Lint generated SVG for README portability and safety."""
import argparse,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('svg',nargs='+');a=p.parse_args();failed=False
for name in a.svg:
    data=Path(name).read_text(); issues=[]
    try:
        root=ET.fromstring(data)
        if not root.tag.endswith('svg'):issues.append('not SVG root')
        if not any(x.tag.endswith('title') for x in root):issues.append('missing title')
        if not any(x.tag.endswith('desc') for x in root):issues.append('missing description')
    except ET.ParseError as e:issues.append(f'invalid XML: {e}')
    if re.search(r'<\s*(script|foreignObject)\b|\bon\w+\s*=',data,re.I):issues.append('script, foreignObject or event handler')
    if re.search(r'(?:href|url\s*\()\s*[=\"\']*\s*(?:https?://|data:)',data,re.I):issues.append('external/data reference requires review')
    if '@media (prefers-reduced-motion: reduce)' not in data and '@keyframes' in data:issues.append('missing reduced-motion rule')
    print(f'{name}: '+('FAIL '+ '; '.join(issues) if issues else 'OK'))
    failed|=bool(issues)
sys.exit(1 if failed else 0)
