#!/usr/bin/env python3
"""4.3 — Keep everything, store it for less. Triptych: 1 / 3 / 5 blocks.
Diagonal blocks full precision (dark); older off-diagonal blocks quantized (pale).
KV-cache strip below grows with the number of blocks. Rendered in 3 palettes."""

N = 15
CELL = 13
BLK = 3

def hexrgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i+2], 16) for i in (0, 2, 4))
def tohex(r, g, b):
    return f"#{round(r):02X}{round(g):02X}{round(b):02X}"
def mixw(h, f):
    r, g, b = hexrgb(h); return tohex(r+(255-r)*f, g+(255-g)*f, b+(255-b)*f)

# (tag, recent/full, bg, line)
PALS = [
    ("5a",  "#2E6F95", "#F4F1E8", "#ffffff"),
    ("8a",  "#2D9CDB", "#F4F1EA", "#ffffff"),
    ("12a", "#E0BC6B", "#0F2A2E", "#1E3A3E"),
]

def panel(b, FULL, QUANT, BG, LINE):
    rows = b * BLK
    side = N * CELL
    strip_y = side + 16
    H = strip_y + CELL + 4
    o = [f'<svg viewBox="0 0 {side} {H}" width="{side}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(N):
        for j in range(N):
            fill = BG
            if i < rows and j <= i:
                fill = FULL if (i // BLK) == (j // BLK) else QUANT
            o.append(f'<rect x="{j*CELL}" y="{i*CELL}" width="{CELL}" height="{CELL}" rx="2" '
                     f'fill="{fill}" stroke="{LINE}" stroke-width="1.2"/>')
    for g in range(0, N + 1, BLK):
        p = g * CELL
        o.append(f'<line x1="{p}" y1="0" x2="{p}" y2="{side}" stroke="{LINE}" stroke-width="2.6"/>')
        o.append(f'<line x1="0" y1="{p}" x2="{side}" y2="{p}" stroke="{LINE}" stroke-width="2.6"/>')
    for j in range(N):
        fill = (FULL if (j // BLK) == (b - 1) else QUANT) if j < rows else BG
        o.append(f'<rect x="{j*CELL}" y="{strip_y}" width="{CELL}" height="{CELL}" rx="2" '
                 f'fill="{fill}" stroke="{LINE}" stroke-width="1.2"/>')
    for g in range(0, N + 1, BLK):
        p = g * CELL
        o.append(f'<line x1="{p}" y1="{strip_y}" x2="{p}" y2="{strip_y+CELL}" stroke="{LINE}" stroke-width="2.6"/>')
    o.append('</svg>')
    return "\n".join(o)

blocks = "".join(
    f'<div class="fig"><div class="tag">{tag}</div><div class="row">'
    + "".join(panel(b, recent, mixw(recent, 0.62), bg, line) for b in (1, 3, 5))
    + '</div></div>'
    for tag, recent, bg, line in PALS)

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>body{{font-family:Georgia,serif;padding:36px;background:#fff;}}
.fig{{margin-bottom:30px;}} .tag{{font-size:12px;color:#999;margin-bottom:6px;}}
.row{{display:flex;gap:24px;align-items:flex-start;}}</style>
</head><body>{blocks}</body></html>'''

with open("fig43_preview.html", "w") as f:
    f.write(html)
print("wrote fig43_preview.html")
