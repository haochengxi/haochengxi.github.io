#!/usr/bin/env python3
"""4.2 — Summarize the past into a fixed state (linear attention).
Triptych: step 1 / 3 / 5. Query column (own color) x 1x1 running state (darkest)
=> 6x6 causal map (diagonal darker, off-diagonal lighter). Arrow flows right->left
(map cumulative-sum folds into the 1x1 state). Rendered in 3 palettes, no captions."""

N = 6
CELL = 20

def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def tohex(r, g, b):
    return f"#{round(r):02X}{round(g):02X}{round(b):02X}"
def mixw(h, f):
    r, g, b = hexrgb(h); return tohex(r+(255-r)*f, g+(255-g)*f, b+(255-b)*f)
def mixb(h, f):
    r, g, b = hexrgb(h); return tohex(r*(1-f), g*(1-f), b*(1-f))

# (tag, recent(=map family), accent(=query), bg, line)
PALS = [
    ("5a",  "#2E6F95", "#E9C46A", "#F4F1E8", "#ffffff"),
    ("8a",  "#2D9CDB", "#EB5757", "#F4F1EA", "#ffffff"),
    ("12a", "#E0BC6B", "#4F9E8A", "#0F2A2E", "#1E3A3E"),
]

QX = 0
SX = 2 * CELL + 4
MX = SX + CELL + 26

def panel(tag, n, recent, accent, bg, line):
    SUM  = mixb(recent, 0.38)
    DIAG = recent
    OFF  = mixw(recent, 0.55)
    QUERY = accent
    side = N * CELL
    W = MX + side + 4
    cy = (n - 1) * CELL + CELL / 2
    o = [f'<svg viewBox="0 0 {W} {side+4}" width="{W}" xmlns="http://www.w3.org/2000/svg">']
    o.append(f'<defs><marker id="ar{tag}{n}" markerWidth="8" markerHeight="8" refX="6" refY="3" orient="auto">'
             f'<path d="M0,0 L6,3 L0,6 Z" fill="#9a9a9a"/></marker></defs>')
    # query column (uniform)
    for r in range(N):
        o.append(f'<rect x="{QX}" y="{r*CELL}" width="{CELL}" height="{CELL}" rx="2" '
                 f'fill="{QUERY}" stroke="{line}" stroke-width="1.3"/>')
    # x sign
    o.append(f'<text x="{CELL+CELL/2-3}" y="{cy+4}" font-size="15" text-anchor="middle" fill="#9a9a9a">&#215;</text>')
    # 1x1 state (darkest)
    o.append(f'<rect x="{SX}" y="{(n-1)*CELL}" width="{CELL}" height="{CELL}" rx="2" '
             f'fill="{SUM}" stroke="{line}" stroke-width="1.3"/>')
    o.append(f'<text x="{SX+CELL/2}" y="{cy+5}" font-size="13" text-anchor="middle" fill="#fff">&#931;</text>')
    # arrow: right -> left
    o.append(f'<line x1="{MX-4}" y1="{cy}" x2="{SX+CELL+4}" y2="{cy}" stroke="#9a9a9a" stroke-width="1.4" marker-end="url(#ar{tag}{n})"/>')
    # 6x6 map (diagonal darker, off-diagonal lighter)
    for i in range(N):
        for j in range(N):
            fill = bg
            if i < n and j <= i:
                fill = DIAG if i == j else OFF
            o.append(f'<rect x="{MX+j*CELL}" y="{i*CELL}" width="{CELL}" height="{CELL}" rx="2" '
                     f'fill="{fill}" stroke="{line}" stroke-width="1.3"/>')
    o.append('</svg>')
    return "\n".join(o)

figs = "".join(
    f'<div class="fig"><div class="tag">{tag}</div><div class="row">'
    + "".join(panel(tag, n, recent, accent, bg, line) for n in (1, 3, 5))
    + '</div></div>'
    for tag, recent, accent, bg, line in PALS)

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{font-family:Georgia,serif;padding:36px;background:#fff;}}
.fig{{margin-bottom:28px;}} .tag{{font-size:12px;color:#999;margin-bottom:6px;}}
.row{{display:flex;gap:30px;align-items:flex-start;flex-wrap:wrap;}}</style>
</head><body>{figs}</body></html>'''

with open("fig42_preview.html", "w") as f:
    f.write(html)
print("wrote fig42_preview.html")
