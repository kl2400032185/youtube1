#!/usr/bin/env python3
"""Catchy YouTube thumbnail: dramatic base + big shaped Telugu title."""
import numpy as np, uharfbuzz as hb
import freetype as ft
from PIL import Image, ImageDraw

FONT = "/tmp/fonts/NotoTelugu.ttf"
SRC  = "/tmp/thumb_base_16x9.png"
OUT  = "/home/user/youtube1/episode01/thumbnail_ep01_catchy.jpg"

img = Image.open(SRC).convert("RGB"); W, H = img.size
data = open(FONT, "rb").read()
hbface = hb.Face(data); hbfont = hb.Font(hbface); UPEM = hbface.upem
face = ft.Face(FONT)

def shape(t):
    b = hb.Buffer(); b.add_str(t); b.guess_segment_properties()
    hb.shape(hbfont, b, {}); return b.glyph_infos, b.glyph_positions

def lw(t, s):
    i_, p_ = shape(t); return sum(p.x_advance for p in p_)*s/UPEM

def render(t, size, fill, sp=5):
    infos, poss = shape(t); sc = size/UPEM
    w = int(sum(p.x_advance for p in poss)*sc) + sp*4 + 10
    h = int(size*1.95) + sp*4
    face.set_char_size(int(size*64))
    F = Image.new("RGBA", (w, h), (0,0,0,0)); S = Image.new("RGBA", (w,h), (0,0,0,0))
    px = sp*2+5; base = int(size*1.32)+sp*2
    for info, pos in zip(infos, poss):
        gid = info.codepoint; xo = int(pos.x_offset*sc); yo = int(pos.y_offset*sc)
        face.load_glyph(gid, ft.FT_LOAD_RENDER); slot = face.glyph; bm = slot.bitmap
        if bm.width and bm.rows:
            arr = np.array(bm.buffer, dtype=np.uint8).reshape(bm.rows, bm.width)
            al = Image.fromarray(arr)
            gx = int(px+xo+slot.bitmap_left); gy = int(base-slot.bitmap_top-yo)
            F.paste(fill+(255,), (gx, gy), al)
            for dx in range(-sp, sp+1, 2):
                for dy in range(-sp, sp+1, 2):
                    if dx*dx+dy*dy <= sp*sp:
                        S.paste((12, 8, 4, 255), (gx+dx, gy+dy), al)
        px += pos.x_advance*sc
    return F, S, px-sp*2-10

L1 = "అన్నీ రాసినా…"
L2 = "వ్యాసుడికి ఎందుకు శాంతి రాలేదు?"
s2 = H//11
while lw(L2, s2) > int(W*0.95) and s2 > 20: s2 -= 2
s1 = int(s2*0.94)

bh = int(H*0.40)
grad = np.zeros((bh, W, 4), np.uint8)
grad[..., 0:3] = (8, 5, 3)
for yy in range(bh):
    t = max(0.0, (yy-bh*0.10)/(bh*0.90))
    grad[yy, :, 3] = int(255*min(0.95, t**1.05*0.95))
band = Image.fromarray(grad, "RGBA")
canvas = img.convert("RGBA"); canvas.alpha_composite(band, (0, H-bh))

GOLD = (255, 205, 66)
f1, g1, w1 = render(L1, s1, GOLD); f2, g2, w2 = render(L2, s2, GOLD)
y2 = H - int(H*0.022) - f2.size[1]
y1 = y2 - int(H*0.006) - f1.size[1]
canvas.alpha_composite(g1, (int((W-w1)/2), y1)); canvas.alpha_composite(f1, (int((W-w1)/2), y1))
canvas.alpha_composite(g2, (int((W-w2)/2), y2)); canvas.alpha_composite(f2, (int((W-w2)/2), y2))

d = ImageDraw.Draw(canvas)
pw, ph = int(W*0.145), int(H*0.105)
px_, py_ = W-pw-int(W*0.02), int(H*0.028)
d.rounded_rectangle([px_, py_, px_+pw, py_+ph], radius=ph//3, fill=(190, 18, 18, 235),
                    outline=(255, 255, 255, 220), width=3)
tag = "భాగం 1"
ts = int(ph*0.52)
tf, tg, tw = render(tag, ts, (255, 255, 255), sp=3)
canvas.alpha_composite(tg, (int(px_+(pw-tw)/2), int(py_+(ph-tf.size[1])/2)))
canvas.alpha_composite(tf, (int(px_+(pw-tw)/2), int(py_+(ph-tf.size[1])/2)))

canvas.convert("RGB").save(OUT, quality=93)
print("saved", OUT, (W, H), "sizes", s1, s2)
