#!/usr/bin/env python3
"""Vendor HTTPS SVG/PNG image assets as local files and optionally replace exact README URLs.
Only downloads supplied URLs. Refuses redirects outside HTTPS and rejects non-image content.
Never overwrite without --force. Does not commit any changes.
"""
import argparse, hashlib, re, sys
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse

def main():
 p=argparse.ArgumentParser();p.add_argument('readme',type=Path);p.add_argument('--dir',default='assets/readme-external');p.add_argument('--apply',action='store_true');p.add_argument('--force',action='store_true');p.add_argument('--limit',type=int,default=30);a=p.parse_args()
 text=a.readme.read_text(); urls=list(dict.fromkeys(re.findall(r'https://[^\s"<>]+?\.(?:svg|png)(?:\?[^\s"<>]*)?',text)))
 urls=[u.replace('&amp;','&') for u in urls][:a.limit]
 dest=(a.readme.parent/a.dir).resolve();dest.mkdir(parents=True,exist_ok=True)
 for u in urls:
  try:
   ext=Path(urlparse(u).path).suffix.lower();name=hashlib.sha256(u.encode()).hexdigest()[:16]+ext;target=dest/name
   if target.exists() and not a.force:print('KEEP',target);continue
   with urlopen(Request(u,headers={'User-Agent':'readme-visual-cache/1.0'}),timeout=12) as r:
    if urlparse(r.url).scheme!='https':raise ValueError('HTTPS redirect required')
    content=r.read(4_000_001)
    if len(content)>4_000_000:raise ValueError('Asset larger than 4MB')
    if ext=='.svg' and b'<svg' not in content[:2000]:raise ValueError('Response is not an SVG')
    if ext=='.png' and not content.startswith(b'\x89PNG\r\n\x1a\n'):raise ValueError('Response is not PNG')
   target.write_bytes(content);print('SAVED',target)
   if a.apply:
    rel=target.relative_to(a.readme.parent).as_posix()
    text=text.replace(u,rel).replace(u.replace('&','&amp;'),rel)
  except Exception as exc:print(f'FAILED {u}: {exc}',file=sys.stderr)
 if a.apply:a.readme.write_text(text);print('Updated README references (review diff).')
 else:print('Dry run for README modifications; add --apply to replace URLs.')
if __name__=='__main__':main()
