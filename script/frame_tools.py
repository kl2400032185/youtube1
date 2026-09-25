#!/usr/bin/env python3
"""
Small helpers for the keyframe images.

1) crop16x9: centre-crop every image to exactly 16:9 (video-ready)
2) thumbnail: overlay Telugu (or any) text on an image and save 1280x720

Usage
-----
  python3 script/frame_tools.py crop16x9 keyframes/bhrugu keyframes/bhrugu/16x9
  python3 script/frame_tools.py thumbnail <in.jpg> <out.jpg> "top text" ["bottom text"]
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

FONT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                    "assets", "fonts", "NotoSansTelugu.ttf")
TARGET = 16 / 9


def crop16x9(src, dst, size=None):
    im = Image.open(src).convert("RGB")
    w, h = im.size
    if w / h > TARGET:
        nw = int(h * TARGET)
        im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
    else:
        nh = int(w / TARGET)
        im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    if size:
        im = im.resize(size, Image.LANCZOS)
    im.save(dst, "JPEG", quality=92, subsampling=0)
    return im.size


def _shadow(d, xy, txt, font, fill, sh=(0, 0, 0)):
    x, y = xy
    for dx, dy in ((3, 3), (0, 3), (3, 0)):
        d.text((x + dx, y + dy), txt, font=font, fill=sh)
    d.text((x, y), txt, font=font, fill=fill)


def thumbnail(src, dst, top, bottom="", w=1280, h=720):
    im = Image.open(src).convert("RGB")
    nw, nh = crop16x9(src, "/tmp/_t.jpg", (w, h))  # crop logic reuse
    im = Image.open("/tmp/_t.jpg")
    ov = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(ov)
    for i in range(int(h * 0.2)):
        d.line([(0, i), (w, i)], fill=int(150 * (1 - i / (h * 0.2))))
    for i in range(int(h * 0.13)):
        d.line([(0, h - i), (w, h - i)], fill=int(160 * (1 - i / (h * 0.13))))
    im = Image.composite(Image.new("RGB", (w, h), (6, 4, 10)), im, ov)
    d = ImageDraw.Draw(im)
    f1 = ImageFont.truetype(FONT, int(h * 0.122))
    b = d.textbbox((0, 0), top, font=f1)
    _shadow(d, ((w - (b[2] - b[0])) // 2, int(h * 0.035)), top, f1, (255, 215, 90))
    if bottom:
        f2 = ImageFont.truetype(FONT, int(h * 0.047))
        b = d.textbbox((0, 0), bottom, font=f2)
        _shadow(d, ((w - (b[2] - b[0])) // 2, int(h * 0.885)), bottom, f2, (255, 235, 190))
    im.save(dst, "JPEG", quality=92, subsampling=0)
    return (w, h)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    cmd = sys.argv[1]
    if cmd == "crop16x9":
        src, dst = sys.argv[2], sys.argv[3]
        os.makedirs(dst, exist_ok=True)
        for f in sorted(os.listdir(src)):
            if f.lower().endswith((".jpg", ".png")) and not f.startswith("_"):
                print(f, "->", crop16x9(os.path.join(src, f), os.path.join(dst, f)))
    elif cmd == "thumbnail":
        src, dst, top = sys.argv[2], sys.argv[3], sys.argv[4]
        bottom = sys.argv[5] if len(sys.argv) > 5 else ""
        print("saved", thumbnail(src, dst, top, bottom), dst)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
