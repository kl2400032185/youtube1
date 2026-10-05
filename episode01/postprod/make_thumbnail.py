#!/usr/bin/env python3
"""Thumbnail with proper Telugu shaping: uharfbuzz shapes, freetype rasterizes."""
import numpy as np, uharfbuzz as hb
import freetype as ft
from PIL import Image, ImageDraw, ImageFilter

FONT = "/tmp/fonts/NotoTelugu.ttf"
SRC  = "/home/user/youtube1/episode01/thumbnail_ep01.jpg"
OUT  = "/home/user/youtube1/episode01/thumbnail_ep01_text.jpg"

img = Image.open(SRC).convert("RGB")
W, H = img.size
UPEM = None

data = open(FONT, "rb").read()
hbface = hb.Face(data); hbfont = hb.Font(hbface)
UPEM = hbface.upem
face = ft.Face(FONT)

def shape(text):
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {})
    return buf.glyph_infos, buf.glyph_positions

def line_width(text, size):
    infos, poss = shape(text)
    return sum(p.x_advance for p in poss) * size / UPEM

def render_line(text, size, fill, stroke_px=4):
    infos, poss = shape(text)
    sc = size / UPEM
    w = int(sum(p.x_advance for p in poss) * sc) + stroke_px*4 + 8
    h = int(size*1.9) + stroke_px*4
    face.set_char_size(int(size*64))
    fillL  = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    strkL  = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pen_x = stroke_px*2 + 4
    base  = int(size*1.30) + stroke_px*2
    for info, pos in zip(infos, poss):
        gid = info.codepoint
        xo = int(pos.x_offset * sc); yo = int(pos.y_offset * sc)
        face.load_glyph(gid, ft.FT_LOAD_RENDER)
        slot = face.glyph; bm = slot.bitmap
        if bm.width and bm.rows:
            arr = np.array(bm.buffer, dtype=np.uint8).reshape(bm.rows, bm.width)
            gl = Image.fromarray(255 - arr)                      # freetype gives 0=empty
            alpha = Image.fromarray(arr)
            gx = pen_x + xo + slot.bitmap_left
            gy = base - slot.bitmap_top - yo
            fillL.paste(fill + (255,), (int(gx), int(gy)), alpha)
            for dx, dy in [(sx, sy) for sx in range(-stroke_px, stroke_px+1, 2)
                                     for sy in range(-stroke_px, stroke_px+1, 2)
                                     if sx*sx+sy*sy <= stroke_px*stroke_px]:
                strkL.paste((15, 10, 5, 255), (int(gx)+dx, int(gy)+dy), alpha)
        pen_x += pos.x_advance * sc
    return fillL, strkL, pen_x - stroke_px*2 - 8

L1 = "అన్నీ రాసినా…"
L2 = "వ్యాసుడికి ఎందుకు శాంతి రాలేదు?"
TARGET = int(W*0.94)
s2 = H//13
while line_width(L2, s2) > TARGET and s2 > 20: s2 -= 2
s1 = int(s2*0.92)

band_h = int(H*0.42)
band = Image.new("RGBA", (W, band_h), (0, 0, 0, 0))
grad = np.zeros((band_h, W, 4), dtype=np.uint8)
grad[..., 3] = (np.linspace(0, 0.88, band_h)[:, None]*255).astype(np.uint8)
for yy in range(band_h):
    grad[yy, :, 3] = int(255*(0.0 if yy < band_h*0.18 else ((yy-band_h*0.18)/(band_h*0.82))**1.15*0.90))
grad[..., 0] = 8; grad[..., 1] = 6; grad[..., 2] = 4
band = Image.fromarray(grad, "RGBA")

canvas = img.convert("RGBA")
canvas.alpha_composite(band, (0, H-band_h))

GOLD = (255, 203, 71)
f1, st1, w1 = render_line(L1, s1, GOLD)
f2, st2, w2 = render_line(L2, s2, GOLD)
y1 = H - band_h + int(band_h*0.24)
y2 = y1 + f1.size[1] + int(H*0.015)
canvas.alpha_composite(st1, (int((W-w1)/2), y1)); canvas.alpha_composite(f1, (int((W-w1)/2), y1))
canvas.alpha_composite(st2, (int((W-w2)/2), y2)); canvas.alpha_composite(f2, (int((W-w2)/2), y2))

d = ImageDraw.Draw(canvas)
pn_w, pn_h = int(W*0.16), int(H*0.085)
px, py = W - pn_w - int(W*0.022), int(H*0.035)
d.rounded_rectangle([px, py, px+pn_w, py+pn_h], radius=pn_h//3, fill=(178, 24, 24, 235),
                    outline=(255, 255, 255, 210), width=max(2, H//384))
tag = "భాగం 1"
tw = line_width(tag, int(pn_h*0.52))
ft_, st_, twr = render_line(tag, int(pn_h*0.52), (255, 255, 255), stroke_px=3)
canvas.alpha_composite(st_, (int(px+(pn_w-twr)/2), int(py+(pn_h-ft_.size[1])/2)))
canvas.alpha_composite(ft_, (int(px+(pn_w-twr)/2), int(py+(pn_h-ft_.size[1])/2)))

canvas.convert("RGB").save(OUT, quality=93)
print("saved", OUT, f"{W}x{H}", "line sizes", s1, s2)
