#!/usr/bin/env python3
"""EP5 thumbnail text bake (1920x1080): exact 4 lines per brief.
  శ్రీమద్భాగవతం (top) · EPISODE 5 (badge) · ఏడు రోజులే మిగిలిన జీవితం! (headline)
  · పరిక్షిత్తు మహారాజు కథ (secondary)
Telugu shaped via uharfbuzz (NotoSansTelugu); English via DejaVu Serif Bold."""
import numpy as np, uharfbuzz as hb, freetype as ft
from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'assets', 'thumb_ep05_base.jpg')
OUT = os.path.join(ROOT, 'assets', 'thumb_ep05_final.jpg')
TEL = os.path.join(ROOT, '..', 'assets', 'fonts', 'NotoSansTelugu.ttf')
EN  = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'

class FontSet:
    def __init__(self, path):
        data = open(path, 'rb').read()
        self.face = hb.Face(data); self.font = hb.Font(self.face)
        self.upem = self.face.upem; self.ft = ft.Face(path)
    def shape(self, text):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.font, buf, {}); return buf.glyph_infos, buf.glyph_positions
    def width(self, text, size, ls=0.0):
        _, poss = self.shape(text)
        return sum(p.x_advance for p in poss) * size / self.upem + ls * size * max(0, len(text) - 1)
    def render(self, text, size, fill, ls=0.0, stroke_px=5):
        infos, poss = self.shape(text); sc = size / self.upem
        w = int(self.width(text, size, ls)) + stroke_px * 4 + 10
        h = int(size * 1.95) + stroke_px * 4
        fillL = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        strkL = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.ft.set_char_size(int(size * 64))
        pen_x = stroke_px * 2 + 5; base = int(size * 1.32) + stroke_px * 2
        for info, pos in zip(infos, poss):
            gid = info.codepoint
            self.ft.load_glyph(gid, ft.FT_LOAD_RENDER)
            slot = self.ft.glyph; bm = slot.bitmap
            if bm.width and bm.rows:
                arr = np.array(bm.buffer, dtype=np.uint8).reshape(bm.rows, bm.width)
                alpha = Image.fromarray(arr)
                gx = int(pen_x + pos.x_offset * sc + slot.bitmap_left)
                gy = int(base - slot.bitmap_top - pos.y_offset * sc)
                fillL.paste(fill + (255,), (gx, gy), alpha)
                for dx in range(-stroke_px, stroke_px + 1, 2):
                    for dy in range(-stroke_px, stroke_px + 1, 2):
                        if dx*dx + dy*dy <= stroke_px*stroke_px:
                            strkL.paste((20, 8, 4, 255), (gx+dx, gy+dy), alpha)
            pen_x += pos.x_advance * sc + ls * size
        return fillL, strkL, pen_x - stroke_px*2 - 10

W, H = 1920, 1080
img = Image.open(SRC).convert('RGB').resize((W, H), Image.LANCZOS)
cv = img.convert('RGBA')

# readability scrim: top + bottom darker bands
def band(y0, h, a0, a1):
    b = np.zeros((h, W, 4), dtype=np.uint8)
    for yy in range(h):
        t = yy / max(1, h - 1)
        b[yy, :, 3] = int(255 * (a0 + (a1 - a0) * t))
    b[..., 0] = 12; b[..., 1] = 6; b[..., 2] = 4
    return Image.fromarray(b, 'RGBA')
cv.alpha_composite(band(0, int(H*0.16), 0.62, 0.0), (0, 0))
bh = int(H*0.40)
cv.alpha_composite(band(0, bh, 0.0, 0.86), (0, H - bh))

fonts = {TEL: FontSet(TEL), EN: FontSet(EN)}
GOLD, WHITE, BADGE = (255, 205, 80), (250, 240, 218), (255, 178, 60)

# 1) top heading (Telugu) — slot y : 14 .. 128
t = "శ్రీమద్భాగవతం"; sz = 64
while fonts[TEL].width(t, sz) > W*0.58 and sz > 36: sz -= 2
f, st, wl = fonts[TEL].render(t, sz, GOLD, stroke_px=6)
y_head = 14
cv.alpha_composite(st, ((W - int(wl))//2 - 5, y_head))
cv.alpha_composite(f, ((W - int(wl))//2 - 5, y_head))

# 2) EPISODE badge (small, centered below top, with plate)
bt = "EPISODE 5"; bsz = 56
plate_h = 100
bf = fonts[EN]
bw = bf.width(bt, bsz, 0.10)
plate_w = int(bw) + 120
plate = Image.new("RGBA", (plate_w, plate_h), (0,0,0,0))
from PIL import ImageDraw
d = ImageDraw.Draw(plate)
d.rounded_rectangle([0,0,plate_w-1,plate_h-1], radius=26, fill=(120, 24, 14, 205), outline=(255,203,71,255), width=5)
py = 146
cv.alpha_composite(plate, ((W-plate_w)//2, py))
f, st, wl = bf.render(bt, bsz, BADGE, ls=0.10, stroke_px=4)
cv.alpha_composite(f, ((W - int(wl))//2 - 4, py + (plate_h - f.size[1])//2 - 2))

# 3) headline (Telugu, largest) — slot y : 0.70H .. 0.865H
t = "ఏడు రోజులే మిగిలిన జీవితం!"; sz = 112
while fonts[TEL].width(t, sz) > W*0.86 and sz > 56: sz -= 2
f, st, wl = fonts[TEL].render(t, sz, GOLD, stroke_px=8)
hy = int(H*0.700)
cv.alpha_composite(st, ((W - int(wl))//2 - 6, hy - (f.size[1] - sz)//2))
cv.alpha_composite(f, ((W - int(wl))//2 - 6, hy - (f.size[1] - sz)//2))

# 4) secondary line (Telugu) — slot y : 0.88H .. 0.965H
t = "పరిక్షిత్తు మహారాజు కథ"; sz = 52
while fonts[TEL].width(t, sz) > W*0.60 and sz > 28: sz -= 2
f2, st2, wl2 = fonts[TEL].render(t, sz, WHITE, stroke_px=4)
sy = int(H*0.885)
cv.alpha_composite(st2, ((W - int(wl2))//2 - 4, sy - (f2.size[1] - sz)//2))
cv.alpha_composite(f2, ((W - int(wl2))//2 - 4, sy - (f2.size[1] - sz)//2))

cv.convert('RGB').save(OUT, quality=94)
print('WROTE', OUT)
