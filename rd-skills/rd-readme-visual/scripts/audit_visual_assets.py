#!/usr/bin/env python3
"""Audit README <img>/<source> URLs, link anchors and remote image availability.
No destructive actions. --remote fetches only remote image links with limits/timeouts.
"""
import argparse, html, re, sys
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request,urlopen
from urllib.error import HTTPError,URLError

def main():
 p=argparse.ArgumentParser();p.add_argument('readme',type=Path);p.add_argument('--remote',action='store_true');p.add_argument('--timeout',type=float,default=8);p.add_argument('--max-assets',type=int,default=60);a=p.parse_args()
 source=a.readme.read_text(); urls=[html.unescape(x) for x in re.findall(r'(?:src|srcset)\s*=\s*["\']([^"\']+)',source)]
 # srcset may contain multiple density choices; handle simple 1x/2x entries.
 urls=[v.split()[0] for u in urls for v in u.split(',')]
 anchors=set(re.findall(r'<a\s+(?:name|id)=["\']([^"\']+)',source,re.I))
 headings=re.findall(r'^#{1,6}\s+(.+)$',source,re.M)
 for h in headings:
  h=re.sub('<[^>]*>','',h);h=re.sub(r'[^a-z0-9 _-]','',h.lower()).strip().replace(' ','-');anchors.add(h)
 problems=[]
 for anchor in re.findall(r'href=["\']#([^"\']+)',source):
  if anchor not in anchors:problems.append(f'UNRESOLVED ANCHOR: #{anchor} (automatic GitHub heading IDs may differ)')
 for u in dict.fromkeys(urls):
  scheme=urlparse(u).scheme
  if scheme in ('http','https'):
   if not a.remote:continue
   if len([x for x in urls if urlparse(x).scheme in ('http','https')])>a.max_assets:
    print('Too many remote asset occurrences; raise --max-assets to inspect them all.',file=sys.stderr);return 2
   try:
    req=Request(u,headers={'User-Agent':'readme-visual-validator/1.0','Accept':'image/svg+xml,image/*;q=0.8'})
    with urlopen(req,timeout=a.timeout) as r:
     typ=r.headers.get('Content-Type',''); data=r.read(256)
     if 'image/' not in typ and not data.lstrip().startswith(b'<svg') and b'<svg' not in data[:256]:problems.append(f'NOT AN IMAGE ({typ}): {u}')
   except (HTTPError,URLError,TimeoutError) as ex:problems.append(f'REMOTE ERROR {ex}: {u}')
  elif scheme=='data':continue
  else:
   if not (a.readme.parent / u.split('#')[0].split('?')[0]).is_file():problems.append(f'MISSING LOCAL IMAGE: {u}')
 for item in problems:print(item)
 print(f'Checked {len(set(urls))} image references, {len(anchors)} possible anchors; {len(problems)} findings.')
 return 1 if problems else 0
if __name__=='__main__':sys.exit(main())
