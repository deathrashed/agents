#!/usr/bin/env python3
"""Generate a composable README hero fragment from JSON config (stdout or --output).
Never modifies the README by itself. Uses shieldcn_visual.py for valid URL/HTML output.
"""
import argparse, json, subprocess, sys
from pathlib import Path
from html import escape

def image(kind, args, preset, link=None, alt=None):
 cmd=[sys.executable,str(Path(__file__).with_name('shieldcn_visual.py')),kind,'--style',str(preset)]
 for key,val in args.items():
  if key=='segments':cmd+=['--segments',*map(str,val)]
  elif val is not None:cmd+=['--'+key.replace('_','-'),str(val)]
 if link:cmd+=['--link',link]
 if alt:cmd+=['--alt',alt]
 return subprocess.check_output(cmd,text=True).strip()

def main():
 p=argparse.ArgumentParser();p.add_argument('config');p.add_argument('--output'); a=p.parse_args()
 data=json.loads(Path(a.config).read_text()); preset=(Path(a.config).resolve().parent / data['preset']).resolve()
 parts=['<!-- BEGIN generated README hero: review before merging -->','<div align="center">']
 h=data.get('header')
 if h:parts.append(image('header', {k:v for k,v in h.items() if k not in ('link','alt')},preset,h.get('link'),h.get('alt')))
 title=data.get('title')
 if title:parts.append(f'<h1>{escape(title)}</h1>')
 tagline=data.get('tagline')
 if tagline:parts.append(f'<p>{escape(tagline)}</p>')
 for row in data.get('rows',[]):
  parts.append('<p align="center">')
  for item in row:
   kind=item.get('type','badge');opts={k:v for k,v in item.items() if k not in ('type','link','alt')}
   parts.append(image(kind,opts,preset,item.get('link'),item.get('alt')))
  parts.append('</p>')
 nav=data.get('nav',[])
 if nav: parts.append('<p>'+' &nbsp; · &nbsp; '.join(f'<a href="#{escape(x["anchor"],quote=True)}">{escape(x["label"])}</a>' for x in nav)+'</p>')
 parts+=['</div>','<!-- END generated README hero -->']
 output='\n'.join(parts)+'\n'
 if a.output:Path(a.output).write_text(output)
 else:print(output,end='')
if __name__=='__main__':main()
