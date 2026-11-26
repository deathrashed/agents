#!/usr/bin/env python3
"""Generate GitHub-safe ShieldCN image URLs / HTML for headers, badge groups, charts,
contributor and sponsor grids, individual provider badges, or custom JSON badges.
No third-party dependencies, no remote fetch and no repository modification.

Examples:
 python3 scripts/shieldcn_visual.py header --title 'MY APP' --subtitle 'Fast and small' --preset graph --logo 'lu:Zap' --style presets/white-yellow-outline.json
 python3 scripts/shieldcn_visual.py chart --kind github-issues --repo owner/repo --title 'Issue trends' --style presets/white-yellow-outline.json
 python3 scripts/shieldcn_visual.py group --segments github/stars/owner/repo github/forks/owner/repo --style presets/white-yellow-outline.json
 python3 scripts/shieldcn_visual.py badge --label Skills --value 10 --logo lu:Zap --style presets/white-yellow-outline.json
 python3 scripts/shieldcn_visual.py dynamic --json-url https://raw.githubusercontent.com/OWNER/REPO/main/stats/badges.json --query '$.skills' --label Skills --style presets/white-yellow-outline.json
"""
import argparse
import html
import json
from pathlib import Path
from urllib.parse import quote, urlencode
BASE='https://shieldcn.dev'

def params(d):
 return urlencode({k:str(v).lower() if isinstance(v,bool) else str(v) for k,v in d.items() if v is not None},quote_via=quote)
def escape_segment(s):
 # Static endpoint is hyphen separated. Double literal hyphens in labels.
 return quote(str(s).replace('-','--'),safe='')
def style(path):
 return json.loads(Path(path).read_text()) if path else {}
def render(path,base,adaptive=True,link=None,alt=None,width=None):
 q=dict(base); q['mode']='light'; light=f'{BASE}/{path}?{params(q)}'
 q['mode']='dark'; dark=f'{BASE}/{path}?{params(q)}'
 ea=lambda x:html.escape(x,quote=True)
 if adaptive:
  markup=f'<picture>\n  <source media="(prefers-color-scheme: dark)" srcset="{ea(dark)}">\n  <img src="{ea(light)}" alt="{ea(alt or path)}"'+(f' width="{int(width)}"' if width else '')+'>\n</picture>'
 else:
  markup=f'<img src="{ea(dark)}" alt="{ea(alt or path)}">'
 return f'<a href="{ea(link)}">{markup}</a>' if link else markup

def main():
 ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
 sub=ap.add_subparsers(dest='type',required=True)
 for kind in ('badge','dynamic','header','group','chart','contributors','sponsors','views'):
  p=sub.add_parser(kind)
  p.add_argument('--style');p.add_argument('--link');p.add_argument('--alt');p.add_argument('--single',action='store_true');p.add_argument('--param',action='append',default=[],metavar='KEY=VALUE');p.add_argument('--format',choices=['html','urls','json'],default='html')
  if kind=='badge':p.add_argument('--label',required=True);p.add_argument('--value',required=True);p.add_argument('--logo')
  if kind=='dynamic':p.add_argument('--json-url',required=True);p.add_argument('--query',required=True);p.add_argument('--label',required=True);p.add_argument('--logo')
  if kind=='header':p.add_argument('--preset',choices=['surface','gradient','dots','grid','graph','glow','transparent'],default='grid');p.add_argument('--title',required=True);p.add_argument('--subtitle');p.add_argument('--logo');p.add_argument('--width',type=int,default=1280);p.add_argument('--height',type=int,default=400)
  if kind=='group':p.add_argument('--segments',nargs='+',required=True)
  if kind=='chart':p.add_argument('--kind',choices=['github-issues','github-stars','github-commits','npm','json'],required=True);p.add_argument('--repo');p.add_argument('--user');p.add_argument('--package');p.add_argument('--json-url');p.add_argument('--query');p.add_argument('--date-query');p.add_argument('--values');p.add_argument('--title');p.add_argument('--width',type=int,default=800);p.add_argument('--height',type=int,default=350)
  if kind=='contributors':p.add_argument('--repo',required=True)
  if kind=='sponsors':p.add_argument('--user',required=True)
  if kind=='views':p.add_argument('--repo',required=True)
 a=ap.parse_args(); theme=style(a.style); style_params=dict(theme.get('base',{})); visual_params=dict(theme.get(a.type,{})); style_params.update(visual_params)
 for v in a.param:
  if '=' not in v:ap.error('--param requires KEY=VALUE')
  k,value=v.split('=',1);style_params[k]=value
 if a.type=='badge':
  path='badge/'+'-'.join(map(escape_segment,(a.label,a.value,style_params.get('color','ffffff')))) + '.svg';style_params['logo']=a.logo or style_params.get('logo')
 elif a.type=='dynamic':
  path='badge/dynamic/json.svg';style_params.update(url=a.json_url,query=a.query,label=a.label)
  if a.logo: style_params['logo']=a.logo
 elif a.type=='header':
  path='header/'+a.preset+'.svg'; style_params.update(title=a.title,subtitle=a.subtitle,width=a.width,height=a.height)
  if a.logo:style_params['logo']=a.logo
 elif a.type=='group':
  segs=[s.strip().strip('/') for s in a.segments]
  if any(s.startswith('http') or '?' in s or '..' in s for s in segs):ap.error('group segments must be provider paths (no URL or query)')
  path='group/'+'+'.join(segs)+'.svg'
 elif a.type=='chart':
  if a.kind in ('github-issues','github-stars'):
   if not a.repo:ap.error('--repo is required')
   path='chart/github/'+a.kind.split('-')[1]+'/'+a.repo+'.svg'
  elif a.kind=='github-commits':
   if not a.user:ap.error('--user is required')
   path='chart/github/commits/'+a.user+'.svg'
  elif a.kind=='npm':
   if not a.package:ap.error('--package is required')
   path='chart/npm/'+a.package+'.svg'
  else:
   if not a.values and not (a.json_url and a.query):ap.error('JSON chart requires --values or --json-url and --query')
   path='chart/json.svg';style_params.update(values=a.values,url=a.json_url,query=a.query,dateQuery=a.date_query)
  style_params.update(title=a.title,width=a.width,height=a.height)
 elif a.type=='contributors':path='contributors/'+a.repo+'.svg'
 elif a.type=='sponsors':path='sponsors/'+a.user+'.svg'
 else:path='views/repo/'+a.repo+'.svg'
 # URL output and markup all come from same params, so URLs can be checked externally.
 q=dict(style_params);q['mode']='light'; light=f'{BASE}/{path}?{params(q)}';q['mode']='dark';dark=f'{BASE}/{path}?{params(q)}'
 if a.format=='json':print(json.dumps({'light':light,'dark':dark},indent=2))
 elif a.format=='urls':print('light:',light,'\ndark:',dark)
 else: print(render(path,style_params,not a.single,a.link,a.alt or a.type, getattr(a,'width',None) if a.type in ('header','chart') else None))
if __name__=='__main__':main()
