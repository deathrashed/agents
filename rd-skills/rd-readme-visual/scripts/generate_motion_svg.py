#!/usr/bin/env python3
"""Deterministic, editable, README-safe SVG compositions. Standard library only."""
import argparse, html, json, math, random, re
from pathlib import Path

def safe_color(c):
    if not re.fullmatch(r'#[0-9a-fA-F]{6}', c): raise ValueError('colors must be #RRGGBB')
    return c

def esc(v): return html.escape(str(v), quote=True)

def load(path):
    d=json.loads(Path(path).read_text())
    for k in ('background','foreground','accent','muted'):
        d[k]=safe_color(d.get(k,{'background':'#101115','foreground':'#F5F5F5','accent':'#FFDA00','muted':'#717782'}[k]))
    d['title']=str(d.get('title','SIGNAL / SYSTEM'))[:64]
    d['subtitle']=str(d.get('subtitle','VISIBLE OPERATION / VERIFIED COMPONENTS'))[:100]
    d['seed']=int(d.get('seed',17));d['motion']=d.get('motion',True)
    if not isinstance(d['motion'],bool): raise ValueError('motion must be boolean')
    return d

def base(d,w,h,body,style=''):
    title=esc(d['title']); subtitle=esc(d['subtitle']); bg=d['background']; fg=d['foreground']; ac=d['accent']; muted=d['muted']
    anim='''@keyframes march{to{stroke-dashoffset:-42}} @keyframes glow{50%{opacity:.8}} @keyframes sweep{to{transform:translateX(1080px)}} .flow{animation:march 3s linear infinite} .beacon{animation:glow 2.4s ease-in-out infinite} .scan{animation:sweep 7s linear infinite}'''
    style=f'''<style>text{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}} .muted{{fill:{muted}}} .fg{{fill:{fg}}} .accent{{fill:{ac}}} {anim if d['motion'] else ''} @media (prefers-reduced-motion: reduce){{*,*::before,*::after{{animation:none!important}}}} {style}</style>'''
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="t desc"><title id="t">{title}</title><desc id="desc">{subtitle}. Decorative animation is optional; all information is visible without motion.</desc>{style}<rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>'''

def signal(d):
    w,h=1100,360; r=random.Random(d['seed']); fg=d['foreground']; ac=d['accent']; muted=d['muted']
    body='<defs><pattern id="micro" width="22" height="22" patternUnits="userSpaceOnUse"><path d="M22 0H0V22" fill="none" stroke="'+muted+'" stroke-opacity=".12"/></pattern><clipPath id="clip"><rect x="18" y="18" width="1064" height="324" rx="2"/></clipPath></defs>'
    body+='<rect x="18" y="18" width="1064" height="324" fill="url(#micro)" stroke="'+muted+'" stroke-opacity=".3"/>'
    body+=f'<path d="M40 78H1060M40 293H1060" stroke="{muted}" stroke-opacity=".35"/><text x="40" y="56" fill="{ac}" font-size="15" letter-spacing="3">{esc(d["title"].upper())}</text><text x="40" y="319" fill="{fg}" font-size="12" opacity=".85" letter-spacing="1">{esc(d["subtitle"].upper())}</text>'
    nodes=d.get('nodes',['SOURCE','TRANSFORM','ROUTE','OUTPUT']); nodes=[str(n)[:17] for n in nodes[:6]]
    if len(nodes)<2: nodes=['SOURCE','OUTPUT']
    xs=[110+i*880/(len(nodes)-1) for i in range(len(nodes))]
    for i in range(len(nodes)-1):
        x1,x2=xs[i],xs[i+1]; yy=178+(-16 if i%2 else 16)
        body+=f'<path d="M{x1:.1f} 177 C{x1+48:.1f} {yy:.1f} {x2-48:.1f} {yy:.1f} {x2:.1f} 177" fill="none" stroke="{muted}" stroke-width="8" opacity=".13"/>'
        body+=f'<path class="flow" d="M{x1:.1f} 177 C{x1+48:.1f} {yy:.1f} {x2-48:.1f} {yy:.1f} {x2:.1f} 177" fill="none" stroke="{ac}" stroke-width="2" stroke-dasharray="10 11" opacity=".85"/>'
    for i,(x,n) in enumerate(zip(xs,nodes)):
        body+=f'<rect x="{x-12:.1f}" y="165" width="24" height="24" fill="{d["background"]}" stroke="{ac}" stroke-width="2" transform="rotate(45 {x:.1f} 177)"/>'
        body+=f'<circle class="beacon" cx="{x:.1f}" cy="177" r="3" fill="{ac}" style="animation-delay:{i*-.4}s"/>'
        body+=f'<text x="{x:.1f}" y="235" text-anchor="middle" fill="{fg}" font-size="13" letter-spacing="1">{esc(n.upper())}</text><text x="{x:.1f}" y="132" text-anchor="middle" fill="{muted}" font-size="11">{i+1:02d}</text>'
    for _ in range(24):
        x=r.randint(50,1050);y=r.choice([94,108,265,278]); body+=f'<path d="M{x} {y}h{r.randint(4,21)}" stroke="{muted}" stroke-opacity=".2"/>'
    return base(d,w,h,body)

def terminal(d):
    w,h=1100,360; ac=d['accent'];fg=d['foreground'];muted=d['muted']; bg=d['background']
    lines=[str(s)[:95] for s in d.get('lines',['$ ./app --inspect','[ok] dependency graph ready','[ok] pipeline complete','> awaiting next operation'])][:6]
    body=f'<rect x="26" y="26" width="1048" height="308" rx="9" fill="none" stroke="{muted}" stroke-opacity=".6"/><path d="M26 68H1074" stroke="{muted}" stroke-opacity=".45"/>'
    for i,color in enumerate(['#FC6A67','#F5C65B','#5BCBA9']):body+=f'<circle cx="{48+i*23}" cy="47" r="5" fill="{color}"/>'
    body+=f'<text x="1042" y="51" text-anchor="end" font-size="12" fill="{muted}">LOG / {esc(d["title"].upper())}</text>'
    for i,line in enumerate(lines):
        y=114+i*37
        body+=f'<text x="58" y="{y}" font-size="17" fill="{ac if i==0 else fg}" opacity="{1 if i==0 else .85}">{esc(line)}</text>'
        body+=f'<text x="1019" y="{y}" font-size="11" fill="{muted}" text-anchor="end">{i+1:02d}</text>'
    body+=f'<rect class="beacon" x="58" y="{116+len(lines)*37}" width="11" height="19" fill="{ac}"/>' if len(lines)<5 else ''
    return base(d,w,h,body)

def orbital(d):
    w,h=1100,360; ac=d['accent']; fg=d['foreground']; muted=d['muted']; bg=d['background'];r=random.Random(d['seed'])
    cx,cy=774,180; body=f'<path d="M40 61H1060M40 301H1060" stroke="{muted}" stroke-opacity=".35"/>'
    for radius in [61,104,144]:
        body+=f'<circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="{muted}" stroke-opacity=".36" stroke-dasharray="2 8"/>'
    for i,radius in enumerate([61,104,144]):
        angle=(i*130+30)*math.pi/180;x=cx+radius*math.cos(angle);y=cy+radius*math.sin(angle)
        body+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="{5+i}" fill="{ac}"/><path d="M{x:.2f} {y:.2f}L{x+18:.2f} {y-18:.2f}" stroke="{ac}" opacity=".65"/>'
    body+=f'<circle cx="{cx}" cy="{cy}" r="27" fill="{bg}" stroke="{ac}" stroke-width="2"/><path d="M{cx-9} {cy}h18M{cx} {cy-9}v18" stroke="{ac}" stroke-width="2"/>'
    body+=f'<text x="46" y="111" fill="{ac}" font-size="16" letter-spacing="4">{esc(d["title"].upper())}</text><text x="46" y="157" fill="{fg}" font-size="19">{esc(d["subtitle"][:44])}</text>'
    for i,label in enumerate(d.get('nodes',['CORE','ADAPTERS','WORKFLOWS'])[:4]):
        body+=f'<text x="50" y="{208+i*29}" fill="{muted}" font-size="13">[{i+1:02}] {esc(str(label).upper())}</text>'
    body+=f'<text x="1060" y="326" fill="{muted}" text-anchor="end" font-size="11">SEED {d["seed"]:04d} / ORBITAL SYSTEM</text>'
    return base(d,w,h,body)

DISPATCH={'signal':signal,'terminal':terminal,'orbital':orbital}
def main():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--style',choices=DISPATCH,default='signal');p.add_argument('--output',required=True);p.add_argument('--static',action='store_true');a=p.parse_args()
    d=load(a.config)
    if a.static:d['motion']=False
    path=Path(a.output);path.parent.mkdir(parents=True,exist_ok=True);path.write_text(DISPATCH[a.style](d),encoding='utf-8');print(path)
if __name__=='__main__': main()
