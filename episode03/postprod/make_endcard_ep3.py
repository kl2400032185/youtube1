#!/usr/bin/env python3
"""EP3 end card: composes the EXACT 4 mandated lines onto the S68 keyframe.
  SRIMAD BHAGAVATAM  /  EPISODE 3  /  వ్యాస మహర్షి ధ్యానంలో చూసిన దివ్య సత్యం  /  Series by Creations Diary
English: DejaVu Serif Bold (letterspaced); Telugu: NotoSansTelugu shaped via uharfbuzz.
Outputs assets/EP03_S68_card_720.jpg (1600x900) and assets/EP03_S68_card_1080.jpg (2560x1440).
"""
import numpy as np, uharfbuzz as hb, freetype as ft
from PIL import Image
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC  = os.path.join(ROOT, 'assets', 'EP03_S68.jpg')
TEL  = os.path.join(ROOT, '..', 'assets', 'fonts', 'NotoSansTelugu.ttf')
EN   = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
ENR  = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'

LINES = [
    ("SRIMAD BHAGAVATAM",            EN,  1.000, (255, 203, 71),  0.14),  # gold, letterspaced
    ("EPISODE 3",                    EN,  0.560, (245, 236, 215), 0.22),
    ("వ్యాస మహర్షి ధ్యానంలో చూసిన దివ్య సత్యం", TEL, 0.600, (255, 215, 120), 0.0),
    ("Series by Creations Diary",    ENR, 0.420, (226, 214, 188), 0.05),
]
GAPS = [1.00, 1.30, 0.85]  # vertical breathing between line groups

class FontSet:
    def __init__(self, path):
        data = open(path, 'rb').read()
        self.face = hb.Face(data); self.font = hb.Font(self.face)
        self.upem = self.face.upem; self.ft = ft.Face(path)
    def shape(self, text):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.font, buf, {}); return buf.glyph_infos, buf.glyph_positions
    def width(self, text, size, ls=0.0):
        infos, poss = self.shape(text)
        w = sum(p.x_advance for p in poss) * size / self.upem
        return w + ls * size * max(0, len(text) - 1)
    def render(self, text, size, fill, ls=0.0, stroke_px=4):
        infos, poss = self.shape(text); sc = size / self.upem
        w = int(self.width(text, size, ls)) + stroke_px * 4 + 8
        h = int(size * 1.9) + stroke_px * 4
        fillL = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        strkL = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        self.ft.set_char_size(int(size * 64))
        pen_x = stroke_px * 2 + 4; base = int(size * 1.30) + stroke_px * 2
        for info, pos in zip(infos, poss):
            gid = info.codepoint
            xo = int(pos.x_offset * sc)
            self.ft.load_glyph(gid, ft.FT_LOAD_RENDER)
            slot = self.ft.glyph; bm = slot.bitmap
            if bm.width and bm.rows:
                arr = np.array(bm.buffer, dtype=np.uint8).reshape(bm.rows, bm.width)
                alpha = Image.fromarray(arr)
                gx = int(pen_x + xo + slot.bitmap_left)
                gy = int(base - slot.bitmap_top - pos.y_offset * sc)
                fillL.paste(fill + (255,), (gx, gy), alpha)
                for dx in range(-stroke_px, stroke_px + 1, 2):
                    for dy in range(-stroke_px, stroke_px + 1, 2):
                        if dx*dx + dy*dy <= stroke_px*stroke_px:
                            strkL.paste((12, 8, 4, 255), (gx+dx, gy+dy), alpha)
            pen_x += pos.x_advance * sc + ls * size
        return fillL, strkL, pen_x - stroke_px*2 - 8

def build(W, H, out):
    img = Image.open(SRC).convert('RGB').resize((W, H), Image.LANCZOS)
    # vignette + lower scrim for legibility
    canvas = img.convert('RGBA')
    band_h = int(H * 0.62)
    grad = np.zeros((band_h, W, 4), dtype=np.uint8)
    for yy in range(band_h):
        t = max(0.0, (yy - band_h*0.10) / (band_h*0.90))
        grad[yy, :, 3] = int(255 * (t ** 1.20) * 0.86)
    grad[..., 0] = 10; grad[..., 1] = 7; grad[..., 2] = 4
    canvas.alpha_composite(Image.fromarray(grad, 'RGBA'), (0, H - band_h))
    base_s = H // 15
    fonts = {p: FontSet(p) for p in {EN, ENR, TEL}}
    # size each line so the widest fits 84%
    sizes = []
    for text, fp, mul, _, ls in LINES:
        f = fonts[fp]; s = int(base_s * mul)
        while f.width(text, s, ls) > W * 0.84 and s > 14: s -= 1
        sizes.append(s)
    heights = [int(s * 1.9) + 12 for s in sizes]
    gaps = [int(base_s * g) for g in GAPS]
    total = sum(heights) + sum(gaps)
    y = H - band_h + (band_h - total) // 2 + int(H * 0.02)
    for (text, fp, _, color, ls), s, hh in zip(LINES, sizes, heights):
        f = fonts[fp]
        fillL, strkL, lw = f.render(text, s, color, ls, stroke_px=max(3, s // 16))
        x = (W - int(lw)) // 2
        canvas.alpha_composite(strkL, (x - 4, y - 4))
        canvas.alpha_composite(fillL, (x - 4, y - 4))
        y += hh
    canvas.convert('RGB').save(out, quality=95)
    print('WROTE', out, f"{os.path.getsize(out)/1e6:.2f} MB", flush=True)

build(1600, 900,  os.path.join(ROOT, 'assets', 'EP03_S68_card_720.jpg'))
build(2560, 1440, os.path.join(ROOT, 'assets', 'EP03_S68_card_1080.jpg'))
