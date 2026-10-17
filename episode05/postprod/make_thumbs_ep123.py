#!/usr/bin/env python3
"""Bake best-CTA thumbnails for EP1-3 in EN + HI (1920x1080), EP5-series layout.
Uses uharfbuzz shaping (Devanagari via NotoSansDevanagari; Latin via DejaVu Serif Bold)."""
import os, uharfbuzz as hb, freetype as ft
import numpy as np
from PIL import Image, ImageDraw

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DEVA = os.path.join(REPO, 'assets', 'fonts', 'NotoSansDevanagari.ttf')
ENF  = '/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf'
W, H = 1920, 1080
GOLD, WHITE, BADGE = (255, 205, 80), (250, 240, 218), (255, 178, 60)

class FontSet:
    def __init__(self, path):
        data = open(path, 'rb').read()
        self.face = hb.Face(data); self.font = hb.Font(self.face)
        self.upem = self.face.upem; self.ft = ft.Face(path)
        self.path_is_deva = 'Devanagari' in path
    def shape(self, text):
        buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
        hb.shape(self.font, buf, {}); return buf.glyph_infos, buf.glyph_positions
    def width(self, text, size, ls=0.0):
        _, poss = self.shape(text)
        return sum(p.x_advance for p in poss) * size / self.upem + ls * size * max(0, len(text)-1)
    def render(self, text, size, fill, ls=0.0, stroke_px=5, lead=0.0):
        infos, poss = self.shape(text); sc = size / self.upem
        w = int(self.width(text, size, ls)) + stroke_px*4 + 10
        h = int(size*(1.95+lead)) + stroke_px*4
        fillL = Image.new('RGBA', (w, h), (0,0,0,0)); strkL = Image.new('RGBA', (w, h), (0,0,0,0))
        self.ft.set_char_size(int(size*64))
        pen_x = stroke_px*2 + 5; base = int(size*(1.32+lead)) + stroke_px*2
        for info, pos in zip(infos, poss):
            gid = info.codepoint
            self.ft.load_glyph(gid, ft.FT_LOAD_RENDER)
            slot = self.ft.glyph; bm = slot.bitmap
            if bm.width and bm.rows:
                arr = np.array(bm.buffer, dtype=np.uint8).reshape(bm.rows, bm.width)
                alpha = Image.fromarray(arr)
                gx = int(pen_x + pos.x_offset*sc + slot.bitmap_left)
                gy = int(base - slot.bitmap_top - pos.y_offset*sc)
                fillL.paste(fill + (255,), (gx, gy), alpha)
                for dx in range(-stroke_px, stroke_px+1, 2):
                    for dy in range(-stroke_px, stroke_px+1, 2):
                        if dx*dx + dy*dy <= stroke_px*stroke_px:
                            strkL.paste((20, 8, 4, 255), (gx+dx, gy+dy), alpha)
            pen_x += pos.x_advance*sc + ls*size
        return fillL, strkL, pen_x - stroke_px*2 - 10

def band(y0, h, a0, a1):
    b = np.zeros((h, W, 4), dtype=np.uint8)
    for yy in range(h):
        t = yy / max(1, h-1)
        b[yy, :, 3] = int(255 * (a0 + (a1-a0)*t))
    b[..., 0] = 12; b[..., 1] = 6; b[..., 2] = 4
    return Image.fromarray(b, 'RGBA')

def put(cv, font, text, size, color, y, maxw, minsize, stroke, lsy=0):
    sz = size
    while font.width(text, sz) > maxw and sz > minsize: sz -= 2
    lead = 0.42 if font.path_is_deva else 0.0
    f, st, wl = font.render(text, sz, color, stroke_px=stroke, lead=lead)
    cv.alpha_composite(st, ((W-int(wl))//2 - 5, y))
    cv.alpha_composite(f,  ((W-int(wl))//2 - 5, y))
    return sz

JOBS = [
 # (ep, lang, base, out, top, topfont, badge, head, headfont, hmax, sub, subfont, submax)
 ('01','en', f'{REPO}/episode01/assets/thumb_ep01_base.jpg', f'{REPO}/episode01/thumb_ep01_en.jpg',
  'SRIMAD BHAGAVATAM', ENF, 'EPISODE 1',
  'The Sage Who Had EVERYTHING… Yet Was Empty!', ENF, 100, 'The Question That Changed Everything', ENF, 56),
 ('01','hi', f'{REPO}/episode01/assets/thumb_ep01_base.jpg', f'{REPO}/episode01/thumb_ep01_hi.jpg',
  'श्रीमद्भागवतम्', DEVA, 'भाग 1',
  'सब कुछ होते हुए भी… खालीपन!', DEVA, 104, 'वह प्रश्न जिसने सब बदल दिया', DEVA, 54),
 ('02','en', f'{REPO}/episode02/assets/thumb_ep02_base.jpg', f'{REPO}/episode02/thumb_ep02_en.jpg',
  'SRIMAD BHAGAVATAM', ENF, 'EPISODE 2',
  'One Evening. One Veena — A Scripture Began!', ENF, 96, 'The Wandering Sage Narada Arrives', ENF, 54),
 ('02','hi', f'{REPO}/episode02/assets/thumb_ep02_base.jpg', f'{REPO}/episode02/thumb_ep02_hi.jpg',
  'श्रीमद्भागवतम्', DEVA, 'भाग 2',
  'एक संध्या, एक वीणा — ग्रंथ का जन्म!', DEVA, 102, 'संचरन करने वाले नारद का आगमन', DEVA, 52),
 ('03','en', f'{REPO}/episode03/assets/thumb_ep03_base.jpg', f'{REPO}/episode03/thumb_ep03_en.jpg',
  'SRIMAD BHAGAVATAM', ENF, 'EPISODE 3',
  'What Vyasa Saw in Deepest Meditation…', ENF, 102, 'The Divine Truth Revealed', ENF, 56),
 ('03','hi', f'{REPO}/episode03/assets/thumb_ep03_base.jpg', f'{REPO}/episode03/thumb_ep03_hi.jpg',
  'श्रीमद्भागवतम्', DEVA, 'भाग 3',
  'गहन ध्यान में व्यास ने देखा दिव्य सत्य!', DEVA, 102, 'परम सत्य का दर्शन', DEVA, 54),
]

cache = {}
for ep, lang, src, out, top, topf, badge, head, headf, hmax, sub, subf, submax in JOBS:
    for p in (topf, headf, subf, ENF):
        if p not in cache: cache[p] = FontSet(p)
    cv = Image.open(src).convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
    cv.alpha_composite(band(0, int(H*0.16), 0.62, 0.0), (0, 0))
    bh = int(H*0.40)
    cv.alpha_composite(band(0, bh, 0.0, 0.86), (0, H-bh))
    # 1) top heading
    put(cv, cache[topf], top, 64, GOLD, 14, W*0.60, 36, 6)
    # 2) badge plate
    bsz = 56; bw = cache[ENF if lang=='en' else topf].width(badge, bsz, 0.10)
    plate_w = int(bw) + 120; plate_h = 100
    plate = Image.new('RGBA', (plate_w, plate_h), (0,0,0,0))
    d = ImageDraw.Draw(plate)
    d.rounded_rectangle([0,0,plate_w-1,plate_h-1], radius=26, fill=(120,24,14,205), outline=(255,203,71,255), width=5)
    py = 146
    cv.alpha_composite(plate, ((W-plate_w)//2, py))
    f, st, wl = cache[topf].render(badge, bsz, BADGE, ls=0.10, stroke_px=4, lead=0.42 if cache[topf].path_is_deva else 0.0)
    cv.alpha_composite(f, ((W-int(wl))//2 - 4, py + (plate_h - f.size[1])//2 - 2))
    # 3) big headline
    put(cv, cache[headf], head, hmax, GOLD, int(H*0.700), W*0.86, 56, 8)
    # 4) secondary
    put(cv, cache[subf], sub, submax, WHITE, int(H*0.885), W*0.62, 28, 4)
    cv.convert('RGB').save(out, quality=94)
    print('WROTE', out)
