#!/usr/bin/env python3
"""Assemble the 5 Telugu comedy shorts: scenes -> video, VO+music+SFX -> audio, burn subs."""
import os, re, subprocess, sys, glob
import numpy as np, wave
import imageio_ffmpeg

ROOT = "/home/user/youtube1"
FF = imageio_ffmpeg.get_ffmpeg_exe()
BUILD = f"{ROOT}/assets/build"
os.makedirs(f"{BUILD}/tmp", exist_ok=True)
os.makedirs(f"{ROOT}/videos", exist_ok=True)
W, H, FPS = 1080, 1920, 24

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("CMD:", " ".join(cmd)); print(r.stderr[-2500:]); sys.exit(1)
    return r

def probe_dur(p):
    r = subprocess.run([FF, "-i", p], capture_output=True, text=True)
    m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", r.stderr)
    h, mnt, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h * 3600 + mnt * 60 + s

def mp3_to_np(path, sr=44100):
    tmp = f"{BUILD}/tmp/_dec.wav"
    run([FF, "-y", "-i", path, "-ac", "1", "-ar", str(sr), tmp])
    with wave.open(tmp, "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    return x

def wav_to_np(path):
    with wave.open(path, "rb") as w:
        x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float64) / 32768
    return x

def write_wav(path, x):
    x = np.clip(x, -1, 1)
    pcm = (x * 32767).astype(np.int16)
    with wave.open(path, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(44100)
        w.writeframes(pcm.tobytes())

def split_on_silence(x, n_expected, sr=44100, thresh=0.015, min_sil=0.2, pad=0.10):
    """Split VO into n_expected chunks at silence midpoints.
    If too many chunks, merge the pair with the smallest gap (intra-sentence pause).
    If too few, split the longest chunk at its quietest interior point."""
    win = int(0.01 * sr)
    rms = np.sqrt(np.convolve(x ** 2, np.ones(win) / win, mode="same"))
    silent = rms < thresh
    gaps, i = [], 0
    while i < len(silent):
        if silent[i]:
            j = i
            while j < len(silent) and silent[j]:
                j += 1
            if (j - i) / sr >= min_sil:
                gaps.append(((i + j) / 2) / sr)
            i = j
        else:
            i += 1
    idx = np.where(~silent)[0]
    if len(idx) == 0:
        return [(0, len(x))]
    start, end = idx[0] / sr, idx[-1] / sr
    cuts = [c for c in [start] + gaps + [end] if start - 0.01 <= c <= end + 0.01]
    chunks = []
    for a, b in zip(cuts[:-1], cuts[1:]):
        if b - a > 0.12:
            chunks.append((a, b))
    if not chunks:
        chunks = [(start, end)]
    while len(chunks) > n_expected:  # merge closest pair
        gl = [chunks[k + 1][0] - chunks[k][1] for k in range(len(chunks) - 1)]
        k = int(np.argmin(gl))
        chunks = chunks[:k] + [(chunks[k][0], chunks[k + 1][1])] + chunks[k + 2:]
    while len(chunks) < n_expected:  # split longest at quietest interior point
        durs = [b - a for a, b in chunks]
        k = int(np.argmax(durs))
        a, b = chunks[k]
        lo, hi = int((a + 0.25 * (b - a)) * sr), int((a + 0.75 * (b - a)) * sr)
        m = lo + int(np.argmin(rms[lo:hi]))
        t = m / sr
        chunks = chunks[:k] + [(a, t), (t, b)] + chunks[k + 1:]
    return [(int(a * sr), int(b * sr)) for a, b in chunks]

# ---------------- episode config ----------------
# shot: (image, start, end, zoom in|out, crop(fx,fy,fw)|None, tint|None)
EPISODES = [
    dict(id="01-wifi-joke", dur=20.0,
         shots=[("assets/scenes/ep01-a-phone-dead.jpg", 0.0, 3.2, "in", None, None),
                ("assets/scenes/ep01-b-plea.jpg", 3.2, 9.4, "in", None, None),
                ("assets/scenes/ep01-c-collapse.jpg", 9.4, 13.6, "in", None, None),
                ("assets/thumbnails/01-wifi-joke.jpg", 13.6, 20.0, "out", None, None)],
         vo=[("assets/vo/ep01-line1-babu.mp3", 3.2), ("assets/vo/ep01-line2-amma.mp3", 7.0),
             ("assets/vo/ep01-line3-babu.mp3", 9.4), ("assets/vo/ep01-line4-amma.mp3", 13.6)],
         sfx=[("trombone", 1.7), ("whoosh", 5.85), ("boing", 6.15), ("ding", 18.6)],
         music_stop=[(6.9, 7.6), (12.5, 13.2)]),
    dict(id="02-exam-joke", dur=20.0,
         shots=[("assets/thumbnails/02-exam-joke.jpg", 0.0, 6.5, "in", None, None),
                ("assets/scenes/ep02-b-vow.jpg", 6.5, 10.5, "in", None, None),
                ("assets/scenes/ep02-c-lounge.jpg", 10.5, 13.0, "static", None, "dim"),
                ("assets/scenes/ep02-d-mega-prayer.jpg", 13.0, 20.0, "in", None, None)],
         vo=[("assets/vo/ep02-line1-chaitu.mp3", 3.0), ("assets/vo/ep02-line2-chaitu.mp3", 7.4),
             ("assets/vo/ep02-line3-chaitu.mp3", 14.0)],
         sfx=[("ding", 1.9), ("pop", 10.55), ("sting", 13.35), ("ding", 18.4)],
         music_stop=[(10.3, 11.6), (17.9, 18.5)]),
    dict(id="03-diet-joke", dur=15.0,
         shots=[("assets/scenes/ep03-a-confident.jpg", 0.0, 4.0, "in", None, None),
                ("assets/scenes/ep03-b-oath.jpg", 4.0, 6.2, "in", None, None),
                ("assets/scenes/ep03-c-smell.jpg", 6.2, 9.0, "in", None, None),
                ("assets/thumbnails/03-diet-joke.jpg", 9.0, 12.5, "in", None, None),
                ("assets/scenes/ep03-e-eating.jpg", 12.5, 15.0, "out", None, None)],
         vo=[("assets/vo/ep03-line1-chinni.mp3", 1.2), ("assets/vo/ep03-line2-chinni.mp3", 4.4),
             ("assets/vo/ep03-line3-chinni.mp3", 9.0)],
         sfx=[("snap", 1.0), ("sniff", 6.45), ("sniff", 7.1), ("ding", 7.6), ("pop", 9.15), ("ding", 13.5)],
         music_stop=[(4.25, 4.75), (8.85, 9.35)]),
    dict(id="04-alarm-joke", dur=20.0,
         shots=[("assets/scenes/ep02-b-vow.jpg", 0.0, 4.5, "in", None, "night"),
                ("assets/scenes/ep02-c-lounge.jpg", 4.5, 12.0, "in", None, "night"),
                ("assets/thumbnails/04-alarm-joke.jpg", 12.0, 16.5, "in", (0.02, 0.02, 0.52), None),
                ("assets/thumbnails/04-alarm-joke.jpg", 16.5, 20.0, "out", None, None)],
         vo_split=("assets/audio/04-alarm-vo.mp3", 3, [1.6, 6.2, 16.6]),
         sfx=[("alarm", 4.6), ("whoosh", 5.5), ("alarm", 8.2), ("whoosh", 9.0),
              ("alarm", 10.6), ("whoosh", 11.3), ("chirp", 12.1), ("boing", 16.55), ("ding", 19.0)],
         music_stop=[(15.8, 16.6)]),
    dict(id="05-phone-battery-joke", dur=20.0,
         shots=[("assets/thumbnails/05-phone-battery-joke.jpg", 0.0, 3.5, "in", (0.52, 0.03, 0.42), "horror"),
                ("assets/thumbnails/05-phone-battery-joke.jpg", 3.5, 8.5, "in", (0.12, 0.22, 0.48), None),
                ("assets/thumbnails/05-phone-battery-joke.jpg", 8.5, 13.5, "in", (0.55, 0.32, 0.44), None),
                ("assets/thumbnails/05-phone-battery-joke.jpg", 13.5, 20.0, "out", None, None)],
         vo_split=("assets/audio/05-phone-battery-vo.mp3", 4, [3.0, 6.0, 9.4, 13.6]),
         sfx=[("sting", 0.15), ("whoosh", 4.6), ("whoosh", 5.7), ("whoosh", 7.0),
              ("sadviolin", 13.3), ("ding", 18.6)],
         music_stop=[(8.9, 9.5), (13.2, 13.9)]),
]

def img_dims(p):
    r = subprocess.run([FF, "-i", p], capture_output=True, text=True)
    m = re.search(r"Video:.*?(\d{2,5})x(\d{2,5})[ ,]", r.stderr)
    return int(m.group(1)), int(m.group(2))

def build_shot(img, start, end, zoom, crop, tint, idx, tmpdir):
    dur = end - start
    nframes = int(round(dur * FPS))
    pre = ""
    if crop:
        fx, fy, fw = crop
        iw, ih = img_dims(f"{ROOT}/{img}")
        cw = int(iw * fw)
        ch = min(int(cw * 16 / 9), ih)
        cx = min(int(iw * fx), iw - cw)
        cy = min(int(ih * fy), ih - ch)
        pre += f"crop={cw}:{ch}:{cx}:{cy},"
    pre += "scale=1350:2400,"
    if zoom == "in":
        z = "min(1+0.0013*on,1.14)"
    elif zoom == "out":
        z = "max(1.14-0.0013*on,1.0)"
    else:
        z = "1.0"
    vf = pre + f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={nframes}:s={W}x{H}:fps={FPS}"
    if tint == "night":
        vf += ",eq=brightness=-0.06:saturation=0.82:contrast=1.05,colorbalance=bs=0.12"
    elif tint == "horror":
        vf += ",eq=contrast=1.18:saturation=0.7:brightness=-0.04,colorbalance=rs=0.22:rm=0.08"
    elif tint == "dim":
        vf += ",eq=brightness=-0.07:saturation=0.85"
    vf += ",format=yuv420p"
    seg = f"{tmpdir}/seg_{idx:02d}.mp4"
    run([FF, "-y", "-i", f"{ROOT}/{img}", "-vf", vf, "-frames:v", str(nframes),
         "-r", str(FPS), "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", seg])
    return seg

def build_episode(ep):
    eid = ep["id"]
    tmpdir = f"{BUILD}/tmp/{eid}"
    os.makedirs(tmpdir, exist_ok=True)
    print(f"== {eid}: shots")
    segs = [build_shot(f"{s[0]}", s[1], s[2], s[3], s[4], s[5], i, tmpdir)
            for i, s in enumerate(ep["shots"])]
    lst = f"{tmpdir}/list.txt"
    with open(lst, "w") as f:
        for s in segs:
            f.write(f"file '{s}'\n")
    vid = f"{tmpdir}/video.mp4"
    run([FF, "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", vid])
    vlen = probe_dur(vid)
    print(f"   video length {vlen:.2f}s (want {ep['dur']})")

    # ---- audio mix ----
    sr = 44100
    total = int(ep["dur"] * sr)
    mix = np.zeros(total)
    music = wav_to_np(f"{BUILD}/music_bed.wav")[:total]
    if len(music) < total:
        music = np.pad(music, (0, total - len(music)))
    # music stop windows (soft ramps)
    ramp = int(0.03 * sr)
    gate = np.ones(total)
    for (a, b) in ep["music_stop"]:
        a, b = int(a * sr), min(int(b * sr), total)
        gate[a:b] = 0.0
        gate[max(0, a - ramp):a] = np.linspace(1, 0, min(ramp, a))
        gate[b:b + ramp] = np.linspace(0, 1, min(ramp, total - b))
    mix += music * 0.16 * gate

    sfx_gain = {"ding": 0.32, "trombone": 0.34, "boing": 0.30, "whoosh": 0.26,
                "alarm": 0.30, "pop": 0.30, "chirp": 0.26, "sting": 0.34,
                "sadviolin": 0.30, "sniff": 0.30, "snap": 0.34}
    for (name, t) in ep.get("sfx", []):
        x = wav_to_np(f"{BUILD}/sfx/{name}.wav")
        s = int(t * sr)
        e = min(total, s + len(x))
        mix[s:e] += x[: e - s] * sfx_gain.get(name, 0.3)

    if "vo" in ep:
        vo_items = [(mp3_to_np(f"{ROOT}/{p}"), t) for p, t in ep["vo"]]
    else:
        src, n_exp, starts = ep["vo_split"]
        x = mp3_to_np(f"{ROOT}/{src}")
        chunks = split_on_silence(x, n_exp)
        print(f"   split {src} -> {len(chunks)} chunks for {n_exp} lines")
        vo_items = [(x[a:b], t) for (a, b), t in zip(chunks, starts)]
    for x, t in vo_items:
        s = int(t * sr)
        e = min(total, s + len(x))
        mix[s:e] += x[: e - s] * 0.95

    peak = np.max(np.abs(mix)) or 1
    if peak > 0.98:
        mix *= 0.98 / peak
    aud = f"{tmpdir}/audio.wav"
    write_wav(aud, mix)

    # ---- mux + burn subtitles ----
    srt = f"{ROOT}/episodes/subtitles/{eid}.te.srt"
    out = f"{ROOT}/videos/{eid}-short.mp4"
    style = ("FontName=Noto Sans Telugu,Fontsize=13,PrimaryColour=&H00FFFFFF,"
             "OutlineColour=&H6A000000,BackColour=&H80000000,Outline=2,Shadow=1,"
             "Bold=1,MarginV=52,Alignment=2")
    vf = f"subtitles={srt}:fontsdir={ROOT}/assets/fonts:force_style='{style}'"
    run([FF, "-y", "-i", vid, "-i", aud, "-vf", vf,
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-c:a", "aac", "-b:a", "160k", "-shortest", out])
    print(f"   -> {out}  ({os.path.getsize(out)//1024} KB, {probe_dur(out):.2f}s)")

if __name__ == "__main__":
    only = sys.argv[1] if len(sys.argv) > 1 else None
    for ep in EPISODES:
        if only and only not in ep["id"]:
            continue
        build_episode(ep)
    print("ALL DONE")
