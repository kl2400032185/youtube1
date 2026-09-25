#!/usr/bin/env python3
"""
Build time-stamped versions of the keyframes + a single timeline contact sheet.

Usage
-----
  python3 script/make_timeline_sheet.py          # uses the frames listed below
  python3 script/make_timeline_sheet.py 6:15     # start from a given timecode

Outputs
-------
  keyframes/bhrugu/labeled/<same name>.jpg   -> each frame with a golden timecode
                                                chip + Telugu scene caption
  keyframes/bhrugu/_timeline_6m15s_to_10m00s.jpg -> one sheet, all frames in order
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KDIR = os.path.join(ROOT, "keyframes", "bhrugu")
FONT = os.path.join(ROOT, "assets", "fonts", "NotoSansTelugu.ttf")

# (file, timecode, Telugu caption, synopsis line for the sheet)
FRAMES = [
    ("10_6m15s_ksheera_sagara_vishnu.jpg", "6:15",
     "క్షీరసాగరం — ఆదిశేషుడిపై విష్ణువు, లక్ష్మీదేవి",
     "పాల సముద్రంలో యోగనిద్ర — శాంతికి నిలయం"),
    ("11_7m00s_the_kick_impact.jpg", "7:00",
     "భృగువు సవాలు — విష్ణువు కళ్లు తెరవడం, అలలు",
     "పరీక్షలో అత్యున్నత క్షణం — నిశ్శబ్దం"),
    ("12_7m45s_srivatsa_impact_mark.jpg", "7:45",
     "శ్రీవత్స చిహ్నం — దివ్యమైన బంగారు కాంతి",
     "పాదముద్ర శాశ్వత చిహ్నంగా మారిన క్షణం"),
    ("13_8m15s_vishnu_holding_feet.jpg", "8:15",
     "విష్ణువు లేచి భృగువు పాదాలు పట్టుకోవడం",
     "కోపం కాదు — ప్రేమ, వినయం"),
    ("14_8m50s_bhrigu_in_tears.jpg", "8:50",
     "భృగువు కన్నీళ్లతో క్షమాపణ అడగడం",
     "పశ్చాత్తాపం — కథకు హృదయం"),
    ("15_9m15s_bhrigu_returns_to_assembly.jpg", "9:15",
     "సభలో తీర్పు — విష్ణువే శాంతమూర్తి",
     "మునుల సభకు తిరిగి — సమాధానం"),
    ("16_9m45s_srivatsa_glowing_ending.jpg", "9:45",
     "శ్రీవత్స చిహ్నం మెరుస్తూ ముగింపు",
     "క్షమ · వినయం · ప్రేమ — నిజమైన బలం"),
]


def font(size):
    return ImageFont.truetype(FONT, size)


def label_frame(src, tcode, caption, dst):
    im = Image.open(src).convert("RGB")
    W, H = im.size
    bar = int(H * 0.135)                      # bottom caption band
    canvas = Image.new("RGB", (W, H + bar), (8, 7, 12))
    canvas.paste(im, (0, 0))
    d = ImageDraw.Draw(canvas)

    # bottom caption band: dim gradient
    for i in range(bar):
        a = int(30 + 90 * (i / bar))
        d.line([(0, H + i), (W, H + i)], fill=(10 + a // 6, 7 + a // 8, 16 + a // 5))

    # golden timecode chip (top-left) with outline
    f_tc = font(int(H * 0.062))
    tw = d.textbbox((0, 0), tcode, font=f_tc)
    pad = int(H * 0.022)
    d.rounded_rectangle([pad, pad, pad + (tw[2] - tw[0]) + 2 * pad, pad + (tw[3] - tw[1]) + 2 * pad],
                        radius=int(pad * 0.6), fill=(12, 9, 4), outline=(226, 178, 68), width=3)
    d.text((pad * 2, pad + pad * 0.75), tcode, font=f_tc, fill=(255, 214, 96))

    # Telugu caption centred in the band
    f_cap = font(int(H * 0.055))
    cb = d.textbbox((0, 0), caption, font=f_cap)
    d.text(((W - (cb[2] - cb[0])) // 2, H + (bar - (cb[3] - cb[1])) // 2 - int(H * 0.008)),
           caption, font=f_cap, fill=(245, 236, 214))
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    canvas.save(dst, "JPEG", quality=92, subsampling=0)
    return canvas.size


def build_sheet(items, out, title="క్షీరసాగరం నుండి ముగింపు వరకు  •  6:15 – 10:00"):
    cols, cell_w = 3, 620
    cell_h = int(cell_w * 9 / 16) + 62
    gap = 16
    header = 96
    rows = (len(items) + cols - 1) // cols
    W = cols * cell_w + (cols + 1) * gap
    H = header + rows * cell_h + (rows + 1) * gap
    sheet = Image.new("RGB", (W, H), (10, 9, 15))
    d = ImageDraw.Draw(sheet)
    tb = d.textbbox((0, 0), title, font=font(40))
    d.text(((W - (tb[2] - tb[0])) // 2, 26), title, font=font(40), fill=(255, 214, 96))

    for i, (src, tcode, caption, syn) in enumerate(items):
        im = Image.open(src if os.path.isabs(src) else os.path.join(KDIR, src)).convert("RGB")
        im.thumbnail((cell_w - 8, cell_h - 62))
        cx = gap + (i % cols) * (cell_w + gap)
        cy = header + (i // cols) * (cell_h + gap)
        d.rounded_rectangle([cx - 4, cy - 4, cx + cell_w + 2, cy + cell_h - 4],
                            radius=10, outline=(60, 52, 40), width=2)
        sheet.paste(im, (cx + (cell_w - im.width) // 2, cy))
        f_tc, f_cap = font(30), font(24)
        d.text((cx + 10, cy + im.height + 6), tcode, font=f_tc, fill=(255, 200, 80))
        tw = d.textbbox((0, 0), tcode, font=f_tc)[2]
        d.text((cx + 20 + tw, cy + im.height + 12), syn, font=f_cap, fill=(228, 222, 208))
    sheet.save(out, "JPEG", quality=90)
    return sheet.size


def main():
    start = sys.argv[1] if len(sys.argv) > 1 else "6:15"
    items = [f for f in FRAMES if f[1] != ""]
    print(f"building labelled frames from {start} -> {len(items)} images")
    ldir = os.path.join(KDIR, "labeled")
    for f, tc, cap, _ in items:
        p = os.path.join(KDIR, f)
        if not os.path.exists(p):
            print("  MISSING", f)
            continue
        size = label_frame(p, tc, cap, os.path.join(ldir, f))
        print(f"  {tc}  {f}  ->  labeled {size[0]}x{size[1]}")
    out = os.path.join(KDIR, "_timeline_6m15s_to_10m00s.jpg")
    sheet_items = [(os.path.join(KDIR, f), tc, cap, syn) for f, tc, cap, syn in items]
    print("timeline sheet:", build_sheet(sheet_items, out))


if __name__ == "__main__":
    main()
