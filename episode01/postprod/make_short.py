#!/usr/bin/env python3
"""Build EP01 YouTube Short (vertical hook cut) from existing EP1 assets.
Audio: real per-scene clean VO (S33 the question, S48 Vyasa's confession,
S65 the arrival) + newly recorded CTA. Video: 1080x1920 animated pans of the
scene key art with shaped-Telugu caption overlays (uharfbuzz + freetype).
Output: episode01/shorts/EP01_YT_SHORT_HOOK.mp4 (<=59s)."""
import subprocess, os, sys, json
import numpy as np, uharfbuzz as hb
import freetype as ft
from PIL import Image, ImageDraw
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = "/home/user/youtube1/episode01"
OUTDIR = f"{ROOT}/shorts"
TMP = "/tmp/shortwork"
os.makedirs(OUTDIR, exist_ok=True); os.makedirs(TMP, exist_ok=True)
FONT = "/tmp/fonts/NotoTelugu.ttf"

# ---------- audio plan ----------
SEG = [
    dict(n="S33", src=f"{ROOT}/audio_clean/EP01_S33.mp3", ss=1.4,
         img=f"{ROOT}/assets/EP01_S33.png",
         cap=["జ్ఞానం మాత్రమే…", "మనసుకు తృప్తిని ఇస్తుందా?"]),
    dict(n="S48", src=f"{ROOT}/audio_clean/EP01_S48.mp3", ss=4.0,
         img=f"{ROOT}/assets/EP01_S48.png",
         cap=["ఇంత జ్ఞానం ఉన్నా…", "శాంతి ఎందుకు లేదు?"]),
    dict(n="S65", src=f"{ROOT}/audio_clean/EP01_S65.mp3", ss=0.0,
         img=f"{ROOT}/assets/EP01_S65.png",
         cap=["అప్పుడు…", "ఒక మహర్షి వచ్చాడు."]),
    dict(n="CTA", src=f"{OUTDIR}/EP01_SHORT_CTA.mp3", ss=0.0,
         img=f"{ROOT}/thumbnail_ep01.jpg",
         cap=["ఆ మహర్షి ఎవరు? ఆ మాట ఏమిటి?", "పూర్తి వీడియో : డిస్క్రిప్షన్ లోని లింక్!"]),
]
GAP = 0.55

def dur(f):
    r = subprocess.run([FF, "-i", f, "-hide_banner"], capture_output=True, text=True)
    ln = [l for l in r.stderr.splitlines() if "Duration" in l][0]
    h, m, s = ln.split("Duration: ")[1].split(",")[0].split(":")
    return int(h)*3600 + int(m)*60 + float(s)

# ---------- Telugu shaping (pattern from make_thumbnail.py) ----------
data = open(FONT, "rb").read()
hbface = hb.Face(data); hbfont = hb.Font(hbface); UPEM = hbface.upem
face = ft.Face(FONT)
try: face.set_var_design_coords([("wght", 800), ("wdth", 100)])
except Exception: pass

def shape(text):
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(hbfont, buf, {}); return buf.glyph_infos, buf.glyph_positions

def line_width(text, size):
    infos, poss = shape(text)
    return sum(p.x_advance for p in poss) * size / UPEM

def render_line(text, size, fill, stroke_px=5):
    infos, poss = shape(text); sc = size / UPEM
    w = int(sum(p.x_advance for p in poss) * sc) + stroke_px*4 + 10
    h = int(size*1.9) + stroke_px*4
    fillL = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    strkL = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    face.set_char_size(int(size*64))
    pen_x = stroke_px*2 + 5; base = int(size*1.30) + stroke_px*2
    for info, pos in zip(infos, poss):
        xo = int(pos.x_offset * sc); yo = int(pos.y_offset * sc)
        face.load_glyph(info.codepoint, ft.FT_LOAD_RENDER)
        slot = face.glyph; bm = slot.bitmap
        if bm.width and bm.rows:
            arr = np.array(bm.buffer, dtype=np.uint8).reshape(bm.rows, bm.width)
            alpha = Image.fromarray(arr)
            gx = pen_x + xo + slot.bitmap_left; gy = base - slot.bitmap_top - yo
            fillL.paste(fill + (255,), (int(gx), int(gy)), alpha)
            for sx in range(-stroke_px, stroke_px+1, 2):
                for sy in range(-stroke_px, stroke_px+1, 2):
                    if sx*sx+sy*sy <= stroke_px*stroke_px:
                        strkL.paste((10, 6, 2, 255), (int(gx)+sx, int(gy)+sy), alpha)
        pen_x += pos.x_advance * sc
    return fillL, strkL, w

def make_caption(idx, lines, out):
    W, H = 1080, 1920
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(canvas)
    GOLD = (255, 203, 71); WHITE = (252, 248, 240)
    # bottom scrim for legibility
    band_h = 620
    grad = np.zeros((band_h, W, 4), dtype=np.uint8)
    for yy in range(band_h):
        a = max(0.0, (yy/band_h - 0.15) / 0.85) ** 1.2 * 0.82
        grad[yy, :, 3] = int(a*255)
    canvas.alpha_composite(Image.fromarray(grad, "RGBA"), (0, H-band_h))
    # episode badge top-left
    pn_w, pn_h = 300, 106
    d.rounded_rectangle([48, 60, 48+pn_w, 60+pn_h], radius=pn_h//3,
                        fill=(178, 24, 24, 235), outline=(255, 255, 255, 220), width=4)
    ts = 66
    tf, tst, twr = render_line("భాగం 1", ts, WHITE, stroke_px=3)
    canvas.alpha_composite(tst, (int(48+(pn_w-twr)/2), int(60+(pn_h-tf.size[1])/2)))
    canvas.alpha_composite(tf,  (int(48+(pn_w-twr)/2), int(60+(pn_h-tf.size[1])/2)))
    # caption lines centered in lower third
    y = H - band_h + 150
    for k, ln in enumerate(lines):
        size = 86 if k == 0 else 74
        while line_width(ln, size) > W*0.92 and size > 40: size -= 2
        f, s, wr = render_line(ln, size, GOLD if k == 0 else WHITE)
        canvas.alpha_composite(s, (int((W-wr)/2), y)); canvas.alpha_composite(f, (int((W-wr)/2), y))
        y += f.size[1] + 46
    canvas.save(out)

# ---------- build ----------
D = []
for i, sg in enumerate(SEG):
    a = dur(sg["src"]) - sg["ss"]
    D.append(a); sg["vdur"] = a + GAP
total = sum(D) + GAP*len(SEG)
print("audio segs:", [f"{x:.1f}" for x in D], "total with gaps:", f"{total:.1f}s")
assert total <= 59.0, "too long for a Short"

caps = []
for i, sg in enumerate(SEG):
    p = f"{TMP}/cap{i}.png"; make_caption(i, sg["cap"], p); caps.append(p)

vfiles = []
for i, sg in enumerate(SEG):
    out = f"{TMP}/seg{i}.mp4"; vfiles.append(out)
    durv = sg["vdur"]
    flt = (f"[0:v]scale=1242:2208:force_original_aspect_ratio=increase,"
           f"crop=1242:2208,eq=contrast=1.05:saturation=1.06[bg];"
           f"[bg]crop=1080:1920:x='(iw-1080)/2':y='(ih-1920)*t/{durv:.2f}'[p];"
           f"[p][1:v]overlay=0:0[o];"
           f"[o]fade=t=in:st=0:d=0.30,fade=t=out:st={durv-0.30:.2f}:d=0.30,format=yuv420p")
    subprocess.run([FF, "-y", "-v", "error", "-loop", "1", "-t", f"{durv:.3f}", "-i", sg["img"],
                    "-loop", "1", "-t", f"{durv:.3f}", "-i", caps[i],
                    "-filter_complex", flt, "-r", "30", "-c:v", "libx264",
                    "-preset", "medium", "-crf", "20", out], check=True)
    print("seg", i, "ok", f"{durv:.1f}s")

lst = f"{TMP}/vlist.txt"
open(lst, "w").write("\n".join(f"file '{v}'" for v in vfiles))
subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                "-c", "copy", f"{TMP}/video.mp4"], check=True)

# audio: trim segs, insert gaps, loudnorm
inputs, chain, lbls = [], [], []
for i, sg in enumerate(SEG):
    inputs += ["-ss", f"{sg['ss']:.2f}", "-i", sg["src"]]
    chain.append(f"[{i}:a]aresample=44100,atrim=0:{D[i]:.3f},asetpts=PTS-STARTPTS[a{i}]")
    lbls.append(f"[a{i}]")
    nxt = f"[g{i}]"
    chain.append(f"anullsrc=r=44100:cl=mono,atrim=0:{GAP}[g{i}_]")
    chain.append(f"[g{i}_]aformat=channel_layouts=stereo{nxt.replace('[','[').replace(']','x]')[:-1]}]")
    lbls.append(f"[g{i}x]")
fc = ";".join(chain) + ";" + "".join(lbls) + f"concat=n={len(lbls)}:v=0:a=1[cat];[cat]loudnorm=I=-16:TP=-1.5:LRA=11[out]"
subprocess.run([FF, "-y", "-v", "error"] + inputs + ["-filter_complex", fc,
                "-map", "[out]", "-c:a", "libmp3lame", "-q:a", "3", f"{TMP}/audio.mp3"], check=True)

out = f"{OUTDIR}/EP01_YT_SHORT_HOOK.mp4"
subprocess.run([FF, "-y", "-v", "error", "-i", f"{TMP}/video.mp4", "-i", f"{TMP}/audio.mp3",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", out], check=True)
print("FINAL:", out, f"{dur(out):.1f}s", f"{os.path.getsize(out)/1e6:.1f}MB")
