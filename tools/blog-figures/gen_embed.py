#!/usr/bin/env python3
"""Export standalone 8a-palette SVGs for blog sections 4.1 / 4.2 / 4.3."""

# ---- 8a Memphis palette ----
RECENT = "#2D9CDB"
RETAIN = "#F2C94C"
SINK   = "#EB5757"
BG     = "#F4F1EA"
LINE   = "#ffffff"
INK    = "#1a1a1a"

def hexrgb(h): h=h.lstrip('#'); return tuple(int(h[i:i+2],16) for i in (0,2,4))
def tohex(r,g,b): return f"#{round(r):02X}{round(g):02X}{round(b):02X}"
def mixw(h,f): r,g,b=hexrgb(h); return tohex(r+(255-r)*f,g+(255-g)*f,b+(255-b)*f)
def mixb(h,f): r,g,b=hexrgb(h); return tohex(r*(1-f),g*(1-f),b*(1-f))

def rect(x,y,w,h,fill,line=LINE,sw=1.3,rx=2):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{line}" stroke-width="{sw}"/>'

# Horizontal, centered legend. items: list of (fill, label, outline?) tuples.
LEG_SW=12; LEG_TGAP=5; LEG_IGAP=20; LEG_CHARW=6.4; LEG_FONT=12; LEG_H=22
LEG_TOP=38  # vertical room reserved above the figure when the legend sits on top
            # (gap between the legend swatches and the diagram below)
def legend(items, W, y):
    widths=[LEG_SW+LEG_TGAP+len(lbl)*LEG_CHARW for (_,lbl,_) in items]
    total=sum(widths)+LEG_IGAP*(len(items)-1)
    x=(W-total)/2
    o=[]
    for (fill,lbl,outline),w in zip(items,widths):
        stroke = "#cccccc" if outline else fill
        o.append(rect(x,y,LEG_SW,LEG_SW,fill,line=stroke,sw=1,rx=2))
        o.append(f'<text x="{x+LEG_SW+LEG_TGAP}" y="{y+LEG_SW-2}" font-size="{LEG_FONT}" fill="#555">{lbl}</text>')
        x+=w+LEG_IGAP
    return "\n".join(o)

# =================== 4.1 ===================
N1=15; C1=14; W_WIN=5; S=2; W_STREAM=3; W_EVICT=2
KEEP={5:[0,1,3],6:[0,1,3],7:[0,1,3],8:[1,3,6],9:[1,3,6],10:[3,6,8],11:[3,6,8],12:[6,8,10],13:[6,8,10],14:[8,10,12]}
def c41(mode,i,j):
    if j>i: return BG
    if mode=="window": return RECENT if (i-j)<W_WIN else BG
    if mode=="stream":
        if j<S: return SINK
        return RECENT if (i-j)<W_STREAM else BG
    if mode=="evict":
        if i<=4: return RECENT
        if (i-j)<W_EVICT: return RECENT
        if j in KEEP.get(i,[]): return RETAIN
        return BG
    return BG
def fig41():
    pw=N1*C1; gap=34; titleh=26; TOP=LEG_TOP
    panels=[("Sliding window","window"),("Attention sink","stream"),("KV eviction","evict")]
    W=3*pw+2*gap; H=TOP+titleh+pw
    o=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Georgia,serif">']
    o.append(legend([(RECENT,"recent (kept)",False),(RETAIN,"retained",False),
                     (SINK,"attention sink",False)], W, 6))
    for k,(title,mode) in enumerate(panels):
        x0=k*(pw+gap)
        o.append(f'<text x="{x0+pw/2}" y="{TOP+16}" font-size="13" font-weight="600" text-anchor="middle" fill="{INK}">{title}</text>')
        o.append(f'<g transform="translate({x0},{TOP+titleh})">')
        for i in range(N1):
            for j in range(N1):
                o.append(rect(j*C1,i*C1,C1,C1,c41(mode,i,j)))
        o.append('</g>')
    o.append('</svg>')
    return "\n".join(o)

# =================== 4.2 ===================
N2=6; C2=20
SUM=mixb(RECENT,0.38); DIAG=RECENT; OFF=mixw(RECENT,0.55); QUERY=SINK
QX=0; SX=2*C2+4; MX=SX+C2+26
def fig42():
    side=N2*C2; sub=MX+side; gap=30; TOP=LEG_TOP
    W=3*sub+2*gap; H=TOP+side
    o=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Georgia,serif">']
    o.append('<defs><marker id="ar" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
             f'<path d="M0,0 L6,3 L0,6 Z" fill="#9a9a9a"/></marker></defs>')
    o.append(legend([(QUERY,"query",False),(SUM,"running state &#931;",False),
                     (DIAG,"current step",False),(OFF,"earlier context",False)], W, 6))
    for idx,n in enumerate((1,3,5)):
        x0=idx*(sub+gap); cy=(n-1)*C2+C2/2
        o.append(f'<g transform="translate({x0},{TOP})">')
        for r in range(N2):
            o.append(rect(QX,r*C2,C2,C2,QUERY))
        o.append(f'<text x="{C2+C2/2-3}" y="{cy+4}" font-size="15" text-anchor="middle" fill="#9a9a9a">&#215;</text>')
        o.append(rect(SX,(n-1)*C2,C2,C2,SUM))
        o.append(f'<text x="{SX+C2/2}" y="{cy+5}" font-size="13" text-anchor="middle" fill="#fff">&#931;</text>')
        o.append(f'<line x1="{MX-4}" y1="{cy}" x2="{SX+C2+4}" y2="{cy}" stroke="#9a9a9a" stroke-width="1.4" marker-end="url(#ar)"/>')
        for i in range(N2):
            for j in range(N2):
                fill=BG
                if i<n and j<=i: fill=DIAG if i==j else OFF
                o.append(rect(MX+j*C2,i*C2,C2,C2,fill))
        o.append('</g>')
    o.append('</svg>')
    return "\n".join(o)

# =================== 4.3 ===================
N3=15; C3=12; BLK=3
FULL=RECENT; QUANT=mixw(RECENT,0.62)
def fig43():
    side=N3*C3; strip_y=side+26; ph=strip_y+C3; gap=28; TOP=LEG_TOP
    W=3*side+2*gap; H=TOP+ph
    o=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Georgia,serif">']
    o.append(legend([(FULL,"full precision (current block)",False),
                     (QUANT,"quantized (older blocks)",False)], W, 6))
    for idx,b in enumerate((1,3,5)):
        x0=idx*(side+gap); rows=b*BLK
        o.append(f'<g transform="translate({x0},{TOP})">')
        for i in range(N3):
            for j in range(N3):
                fill=BG
                if i<rows and j<=i: fill=FULL if (i//BLK)==(j//BLK) else QUANT
                o.append(rect(j*C3,i*C3,C3,C3,fill,sw=1.1))
        for g in range(0,N3+1,BLK):
            p=g*C3
            o.append(f'<line x1="{p}" y1="0" x2="{p}" y2="{side}" stroke="{LINE}" stroke-width="2.4"/>')
            o.append(f'<line x1="0" y1="{p}" x2="{side}" y2="{p}" stroke="{LINE}" stroke-width="2.4"/>')
        o.append(f'<text x="0" y="{strip_y-6}" font-size="11" font-style="italic" fill="#777">KV cache</text>')
        for j in range(N3):
            fill=(FULL if (j//BLK)==(b-1) else QUANT) if j<rows else BG
            o.append(rect(j*C3,strip_y,C3,C3,fill,sw=1.1))
        for g in range(0,N3+1,BLK):
            p=g*C3
            o.append(f'<line x1="{p}" y1="{strip_y}" x2="{p}" y2="{strip_y+C3}" stroke="{LINE}" stroke-width="2.4"/>')
        o.append('</g>')
    o.append('</svg>')
    return "\n".join(o)

import os
# Write directly into the post's published media dir (this script lives in tools/blog-figures/).
OUT = os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "..",
                                    "static", "posts", "forgetting-wall", "media"))
for name,svg in [("fig41.svg",fig41()),("fig42.svg",fig42()),("fig43.svg",fig43())]:
    path = os.path.join(OUT, name)
    with open(path,"w") as f: f.write(svg)
    print("wrote", path)
