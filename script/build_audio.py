#!/usr/bin/env python3
"""
Build the final Telugu Ganesha narration audio from the per-beat TTS parts.

Deliverables
------------
1) ganesha_story_natural_<MMmSSs>.mp3  -> exactly the requested voice settings,
   natural pacing, generous paragraph pauses (no time-compression).
2) ganesha_story_exact_6m08s.mp3        -> identical performance, gently
   time-compressed (pitch preserved) + pauses kept, so the total is exactly
   368.000 s = 6:08 for the video.

Pipeline: trim TTS padding -> assemble timeline -> 2-pass loudnorm (-16 LUFS)
-> 44.1 kHz / 192 kbps mono MP3.
"""
import glob
import json
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

import imageio_ffmpeg

FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
SR = 24000              # TTS native rate
OUT_SR = 44100
TARGET_TOTAL = 368.0    # 6:08
LEAD_IN = 0.50
TAIL = 1.00
PAD = 0.06              # silence kept at the very start/end of every beat
# pauses between beat 1|2, 2|3, ... 7|8  (longer pause = bigger story turn)
BOUNDARY_PAUSES = [0.70, 0.90, 0.70, 1.00, 1.10, 1.00, 1.30]

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTDIR = os.path.join(ROOT, "audio", "final")


def db(x):
    return 20 * np.log10(max(x, 1e-12))


def load_trim(path):
    """Read a part, trim leading/trailing silence down to PAD seconds."""
    x, sr = sf.read(path, dtype="float32", always_2d=False)
    assert sr == SR, f"{path}: expected {SR} Hz, got {sr}"
    if x.ndim > 1:
        x = x.mean(axis=1)
    win = 240  # 10 ms
    rms = np.sqrt(np.convolve(x.astype(np.float64) ** 2, np.ones(win) / win, "same"))
    idx = np.where(rms > 10 ** (-50 / 20))[0]
    if len(idx):
        a = max(0, int(idx[0] - PAD * sr))
        b = min(len(x), int(idx[-1] + PAD * sr))
        x = x[a:b]
    # 5 ms fades so joins are click-free
    n = int(0.005 * sr)
    if len(x) > 2 * n:
        x[:n] *= np.linspace(0, 1, n, dtype="float32")
        x[-n:] *= np.linspace(1, 0, n, dtype="float32")
    return x


def sil(seconds):
    return np.zeros(int(round(seconds * SR)), dtype="float32")


def assemble(parts, pauses, lead=LEAD_IN, tail=TAIL):
    chunks = [sil(lead), parts[0]]
    for p, gap in zip(parts[1:], pauses):
        chunks += [sil(gap), p]
    chunks.append(sil(tail))
    y = np.concatenate(chunks)
    marks, t = [], lead
    for i, p in enumerate(parts):
        marks.append((t, i + 1))
        t += len(p) / SR + (pauses[i] if i < len(pauses) else tail)
    return y, marks


def write_wav(y, path):
    sf.write(path, y, SR, subtype="FLOAT")
    return path


def atempo_file(src, dst, factor):
    subprocess.run(
        [FFMPEG, "-y", "-v", "error", "-i", src,
         "-af", f"atempo={factor:.6f}", "-ar", str(SR), dst],
        check=True)
    x, sr = sf.read(dst, dtype="float32")
    if x.ndim > 1:
        x = x.mean(axis=1)
    return x


def loudnorm_two_pass(src, dst, I=-16.0, TP=-1.5, LRA=11.0):
    """Measure then apply linear loudness normalisation + mp3 encode."""
    probe = subprocess.run(
        [FFMPEG, "-hide_banner", "-i", src, "-af",
         f"loudnorm=I={I}:TP={TP}:LRA={LRA}:print_format=json",
         "-f", "null", "-"],
        capture_output=True, text=True).stderr
    m = re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", probe, re.S)
    stats = json.loads(m[-1]) if m else None
    af = f"loudnorm=I={I}:TP={TP}:LRA={LRA}"
    if stats:
        af = (f"loudnorm=I={I}:TP={TP}:LRA={LRA}:linear=true:"
              f"measured_I={stats['input_i']}:measured_TP={stats['input_tp']}:"
              f"measured_LRA={stats['input_lra']}:measured_thresh={stats['input_thresh']}:"
              f"offset={stats['target_offset']}")
    subprocess.run(
        [FFMPEG, "-y", "-v", "error", "-i", src, "-af", af,
         "-ar", str(OUT_SR), "-ac", "1", "-c:a", "libmp3lame", "-b:a", "192k", dst],
        check=True)
    return stats


def mmss(t):
    return f"{int(t // 60)}:{t % 60:05.2f}"


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    tmp = os.path.join(OUTDIR, "_tmp")
    os.makedirs(tmp, exist_ok=True)

    srcs = sorted(glob.glob(os.path.join(ROOT, "audio", "part*.mp3")))
    if len(srcs) != 8:
        sys.exit(f"expected 8 parts, found {len(srcs)}")
    parts = [load_trim(p) for p in srcs]
    speech = sum(len(p) for p in parts) / SR
    print(f"trimmed speech: {speech:.2f}s over {len(parts)} beats")

    # ---------- 1) natural ----------
    y_nat, marks_nat = assemble(parts, BOUNDARY_PAUSES)
    dur_nat = len(y_nat) / SR
    nat_mp3 = os.path.join(OUTDIR, f"ganesha_story_natural_{int(dur_nat // 60)}m{int(round(dur_nat % 60)):02d}s.mp3")
    st = loudnorm_two_pass(write_wav(y_nat, os.path.join(tmp, "natural.wav")), nat_mp3)
    print(f"[natural] {dur_nat:.2f}s = {mmss(dur_nat)} -> {os.path.basename(nat_mp3)}")
    if st:
        print(f"          loudness: I={st['input_i']} LUFS, TP={st['input_tp']} dBTP")

    # ---------- 2) exact 6:08 ----------
    fixed = LEAD_IN + TAIL + sum(BOUNDARY_PAUSES)
    speech_target = TARGET_TOTAL - fixed
    factor = speech / speech_target
    print(f"[exact] need speech {speech_target:.2f}s from {speech:.2f}s -> atempo x{factor:.4f} "
          f"(~{(factor - 1) * 100:.1f}% faster)")
    if factor > 1.15:
        print("        WARNING: compression is getting audible; consider trimming script")
    for attempt in range(4):
        fast = []
        for i, p in enumerate(parts):
            w = os.path.join(tmp, f"fast{i + 1:02d}.wav")
            sf.write(w, p, SR, subtype="FLOAT")
            fast.append(atempo_file(w, w.replace(".wav", "_a.wav"), factor))
        y_ex, marks_ex = assemble(fast, BOUNDARY_PAUSES)
        delta = TARGET_TOTAL - len(y_ex) / SR
        if delta >= 0:                      # pad the tail with silence
            y_ex = np.concatenate([y_ex, sil(delta)])
            break
        if -delta <= TAIL - 0.25:           # absorb the excess in the tail pad
            y_ex = y_ex[:len(y_ex) + int(round(delta * SR))]
            break
        factor *= (len(y_ex) / SR) / TARGET_TOTAL
        print(f"[exact] retry {attempt + 1}: adjusting atempo -> x{factor:.4f}")
    dur_ex = len(y_ex) / SR
    ex_mp3 = os.path.join(OUTDIR, "ganesha_story_exact_6m08s.mp3")
    st2 = loudnorm_two_pass(write_wav(y_ex, os.path.join(tmp, "exact.wav")), ex_mp3)
    print(f"[exact] {dur_ex:.3f}s = {mmss(dur_ex)} -> {os.path.basename(ex_mp3)}")
    if st2:
        print(f"        loudness: I={st2['input_i']} LUFS, TP={st2['input_tp']} dBTP")

    info = {
        "natural": {"file": os.path.basename(nat_mp3), "duration_s": round(dur_nat, 2),
                    "spoken_speech_s": round(speech, 2), "atempo": 1.0},
        "exact": {"file": os.path.basename(ex_mp3), "duration_s": round(dur_ex, 3),
                  "atempo": round(factor, 4)},
        "pauses_s": BOUNDARY_PAUSES, "lead_in_s": LEAD_IN, "tail_s": TAIL,
        "marks_exact": [{"t": round(t, 2), "mmss": mmss(t), "beat": i} for t, i in marks_ex],
    }
    json.dump(info, open(os.path.join(OUTDIR, "build_info.json"), "w"), indent=1)
    for t, i in marks_ex:
        print(f"   beat {i}: {mmss(t)}")


if __name__ == "__main__":
    main()
