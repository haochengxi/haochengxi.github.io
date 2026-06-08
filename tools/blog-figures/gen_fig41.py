#!/usr/bin/env python3
"""15x15 attention panels, 5 kept/row. KV eviction colors recent vs retained differently.
32 palettes across 16 style families (2 each)."""

CELL = 13
N = 15
W_WIN = 5
S = 2
W_STREAM = 3
W_EVICT = 2

KEEP_BY_ROW = {
    5:[0,1,3], 6:[0,1,3], 7:[0,1,3],
    8:[1,3,6], 9:[1,3,6],
    10:[3,6,8], 11:[3,6,8],
    12:[6,8,10], 13:[6,8,10],
    14:[8,10,12],
}

# label -> (recent, retained, sink, bg, line)
PALETTES = [
    ("5a · Mediterranean",  "#2E6F95", "#8ECAE6", "#E9C46A", "#F4F1E8", "#ffffff"),
    ("8a · Memphis",        "#2D9CDB", "#F2C94C", "#EB5757", "#F4F1EA", "#ffffff"),
    ("12a · Art Deco",      "#E0BC6B", "#4F9E8A", "#C98A4B", "#0F2A2E", "#1E3A3E"),
]

def cell_color(mode, i, j, recent, retained, sink, bg):
    if j > i:
        return bg
    if mode == "window":
        return recent if (i - j) < W_WIN else bg
    if mode == "stream":
        if j < S:
            return sink
        return recent if (i - j) < W_STREAM else bg
    if mode == "evict":
        if i <= 4:
            return recent
        if (i - j) < W_EVICT:
            return recent
        if j in KEEP_BY_ROW.get(i, []):
            return retained
        return bg
    return bg

def matrix_svg(mode, recent, retained, sink, bg, line):
    side = N * CELL
    out = [f'<svg viewBox="0 0 {side} {side}" width="{side}" height="{side}" xmlns="http://www.w3.org/2000/svg">']
    for i in range(N):
        for j in range(N):
            out.append(f'<rect x="{j*CELL}" y="{i*CELL}" width="{CELL}" height="{CELL}" rx="2" '
                       f'fill="{cell_color(mode,i,j,recent,retained,sink,bg)}" stroke="{line}" stroke-width="1.3"/>')
    out.append('</svg>')
    return "\n".join(out)

PANELS = [("Sliding window", "window"), ("+ Attention sink", "stream"), ("KV eviction", "evict")]

rows = ""
for label, recent, retained, sink, bg, line in PALETTES:
    panels = "".join(
        f'<div class="card"><div class="t">{t}</div>{matrix_svg(m,recent,retained,sink,bg,line)}</div>'
        for t, m in PANELS)
    sw = (f'<span class="k" style="background:{recent}"></span>recent'
          f'<span class="k" style="background:{retained}"></span>retained'
          f'<span class="k" style="background:{sink}"></span>sink'
          f'<span class="k" style="background:{bg};outline:1px solid #ccc"></span>evicted')
    rows += f'<section><h4>{label} &nbsp;<small style="font-weight:400;color:#888">{sw}</small></h4><div class="row">{panels}</div></section>'

html = f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<style>
  body{{font-family:Georgia,serif;padding:28px 36px;background:#fff;color:#1a1a1a;}}
  section{{margin-bottom:30px;}}
  h4{{font-weight:600;font-size:14px;margin:0 0 9px;color:#333;}}
  .row{{display:flex;gap:34px;}}
  .card .t{{font-weight:600;margin-bottom:7px;font-size:12px;color:#666;}}
  .k{{display:inline-block;width:10px;height:10px;vertical-align:-1px;margin:0 3px 0 10px;}}
</style></head><body>
  <h3 style="font-weight:600;">4.1 &middot; Look at less of the past</h3>
  <p style="color:#666;font-size:13px;">Each row = one generation step &middot; each column = one past token in the KV cache. Pick a palette, e.g. "5a".</p>
  {rows}
</body></html>'''

with open("fig41_preview.html", "w") as f:
    f.write(html)
print("wrote fig41_preview.html with", len(PALETTES), "palettes")
