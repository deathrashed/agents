#!/usr/bin/env python3
"""Draw purpose-built deterministic animation frames to GIF/WebP with Pillow."""
import argparse,json,math
from pathlib import Path

def run():
    p=argparse.ArgumentParser();p.add_argument('--config',required=True);p.add_argument('--output',required=True);p.add_argument('--format',choices=['gif','webp']);p.add_argument('--fps',type=int,default=12);p.add_argument('--seconds',type=float,default=3);p.add_argument('--width',type=int,default=960);p.add_argument('--height',type=int,default=300);a=p.parse_args()
    from PIL import Image,ImageDraw,ImageFont
    if a.width<320 or a.height<130 or not 2<=a.fps<=30 or not .5<=a.seconds<=12: raise ValueError('outside safe animation dimensions/rates')
    d=json.loads(Path(a.config).read_text()); cols=[d.get(k,default) for k,default in [('background','#101115'),('foreground','#F5F5F5'),('accent','#FFDA00'),('muted','#717782')]]
    bg,fg,ac,muted=cols;nodes=[str(x)[:16] for x in d.get('nodes',['SOURCE','TRANSFORM','OUTPUT'])][:6]
    if len(nodes)<2:nodes=['SOURCE','OUTPUT']
    total=round(a.fps*a.seconds); frames=[]; ys=a.height*.54;xs=[70+i*(a.width-140)/(len(nodes)-1) for i in range(len(nodes))]
    for frame in range(total):
        t=frame/total;im=Image.new('RGB',(a.width,a.height),bg);dr=ImageDraw.Draw(im)
        for x in range(0,a.width,25):dr.line((x,0,x,a.height), fill='#202329',width=1)
        for y in range(0,a.height,25):dr.line((0,y,a.width,y), fill='#202329',width=1)
        dr.line((30,40,a.width-30,40),fill=muted,width=1)
        dr.text((32,15),str(d.get('title','SYSTEM')).upper()[:56],fill=ac)
        for i in range(len(xs)-1):
            dr.line((xs[i],ys,xs[i+1],ys),fill=muted,width=2)
            for k in range(3):
                frac=(t*1.2+k/3-i*.14)%1;x=xs[i]+frac*(xs[i+1]-xs[i]);dr.ellipse((x-4,ys-4,x+4,ys+4),fill=ac)
        for i,(x,n) in enumerate(zip(xs,nodes)):
            dr.rectangle((x-12,ys-12,x+12,ys+12),fill=bg,outline=ac,width=2)
            dr.text((x-4*len(n),ys+26),n.upper(),fill=fg)
        dr.text((32,a.height-27),str(d.get('subtitle','LIVE SIGNAL TRACE'))[:100].upper(),fill=fg)
        frames.append(im)
    target=Path(a.output);target.parent.mkdir(parents=True,exist_ok=True);fmt=a.format or target.suffix.lower().strip('.');
    if fmt not in ['gif','webp']:raise ValueError('choose GIF or WebP')
    opts={'save_all':True,'append_images':frames[1:],'duration':round(1000/a.fps),'loop':0}
    if fmt=='webp':opts.update(quality=80,method=4)
    frames[0].save(target,format=fmt.upper(),**opts);print(f'{target} {len(frames)} frames ({fmt})')
if __name__=='__main__':run()
