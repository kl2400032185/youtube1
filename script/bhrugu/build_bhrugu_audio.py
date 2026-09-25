#!/usr/bin/env python3
"""
Build the Bhrugu Maharshi narration masters (10-minute video).

Two outputs
-----------
* bhrugu_story_natural_<MMmSSs>.mp3  -> untouched TTS pacing (reference / longer cut)
* bhrugu_story_exact_10m00s.mp3       -> TTS silence gaps tightened to natural
  sentence pauses + a very small atempo, so the total is exactly 600.000 s.

The TTS clips contain ~34% silence (line-break padding). Tightening only those
gaps keeps every spoken word at full natural speed; the final atempo needed is
typically <4%.
"""
import glob
import json
import os
import sys

import numpy as np
import soundfile as sf

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, SCRIPT_DIR)
from build_audio import (  # noqa: E402
    SR, load_trim, assemble, sil, write_wav, loudnorm_two_pass, atempo_file, mmss,
)

ROOT = os.path.dirname(SCRIPT_DIR)
PARTS_DIR = os.path.join(ROOT, "audio", "bhrugu")
OUTDIR = os.path.join(PARTS_DIR, "final")

TARGET_TOTAL = 600.0
LEAD_IN = 0.8
TAIL = 1.6
BOUNDARY_PAUSES = [2.0, 2.0, 2.0, 2.2, 2.0, 2.2, 2.0, 2.4]   # act/part joins
PART_ACTS = [1, 1, 2, 2, 3, 4, 4, 5, 5]

# gap tightening: any silence run longer than KEEP becomes KEEP + FRAC*excess
GAP_KEEP = 0.28
GAP_FRAC = 0.30
QUIET_DB = -52.0


def tighten_gaps(x, sr=SR, keep=GAP_KEEP, frac=GAP_FRAC):
    """Shorten internal silence runs (TTS line padding) without touching speech.

    A silence run of length L (> keep) becomes keep + frac * (L - keep),
    trimmed symmetrically around the middle of the run, so no audio is cut.
    """
    win = int(0.01 * sr)
    n = len(x) // win
    rms = np.sqrt((x[:n * win].reshape(n, win).astype(np.float64) ** 2).mean(1))
    quiet = rms < 10 ** (QUIET_DB / 20)

    pieces, removed, pos = [], 0.0, 0
    i = 0
    while i < n:
        if quiet[i]:
            j = i
            while j < n and quiet[j]:
                j += 1
            start, end = i * win, min(j * win, len(x))
            run = (end - start) / sr
            if run > keep:
                cut = int((run - keep) * (1 - frac) * sr)
                keep_left = (end - start - cut)
                a = start + keep_left // 2
                b = a + cut
                pieces.append(x[pos:a])
                removed += cut / sr
                pos = b
            i = j
        else:
            i += 1
    pieces.append(x[pos:])
    return np.concatenate(pieces), removed


def main():
    os.makedirs(OUTDIR, exist_ok=True)
    tmp = os.path.join(OUTDIR, "_tmp")
    os.makedirs(tmp, exist_ok=True)

    srcs = sorted(glob.glob(os.path.join(PARTS_DIR, "part*.mp3")))
    if len(srcs) != 9:
        sys.exit(f"expected 9 parts, found {len(srcs)}")
    parts = [load_trim(p) for p in srcs]
    speech = sum(len(p) for p in parts) / SR
    print(f"trimmed speech: {speech:.2f}s over {len(parts)} parts")

    # ---------- 1) natural (untouched pacing) ----------
    y_nat, _ = assemble(parts, BOUNDARY_PAUSES, lead=LEAD_IN, tail=TAIL)
    dur_nat = len(y_nat) / SR
    nat_mp3 = os.path.join(
        OUTDIR, f"bhrugu_story_natural_{int(dur_nat // 60)}m{int(round(dur_nat % 60)):02d}s.mp3")
    st = loudnorm_two_pass(write_wav(y_nat, os.path.join(tmp, "natural.wav")), nat_mp3)
    print(f"[natural] {dur_nat:.2f}s = {mmss(dur_nat)} -> {os.path.basename(nat_mp3)}")
    if st:
        print(f"          loudness I={st['input_i']} LUFS TP={st['input_tp']} dBTP")

    # ---------- 2) tight (silence gaps shortened, speech untouched) ----------
    tight, removed = [], 0.0
    for p in parts:
        t, r = tighten_gaps(p)
        tight.append(t)
        removed += r
    speech_tight = sum(len(p) for p in tight) / SR
    print(f"[tight]   removed {removed:.1f}s of padding -> speech {speech_tight:.1f}s")

    # ---------- 3) exact 10:00 ----------
    fixed = LEAD_IN + TAIL + sum(BOUNDARY_PAUSES)
    factor = speech_tight / (TARGET_TOTAL - fixed)
    print(f"[exact]   need {TARGET_TOTAL - fixed:.1f}s from {speech_tight:.1f}s "
          f"-> atempo x{factor:.4f} ({(factor - 1) * 100:+.2f}%)")
    for attempt in range(4):
        fast = []
        for i, p in enumerate(tight):
            w = os.path.join(tmp, f"f{i + 1:02d}.wav")
            sf.write(w, p, SR, subtype="FLOAT")
            fast.append(atempo_file(w, w.replace(".wav", "_a.wav"), factor))
        y_ex, marks = assemble(fast, BOUNDARY_PAUSES, lead=LEAD_IN, tail=TAIL)
        delta = TARGET_TOTAL - len(y_ex) / SR
        print(f"          attempt {attempt + 1}: {len(y_ex) / SR:.3f}s (delta {delta:+.3f}s)")
        if delta >= 0:
            y_ex = np.concatenate([y_ex, sil(delta)])
            break
        if -delta <= TAIL - 0.3:
            y_ex = y_ex[:len(y_ex) + int(round(delta * SR))]
            break
        factor *= (len(y_ex) / SR) / TARGET_TOTAL
    dur_ex = len(y_ex) / SR
    ex_mp3 = os.path.join(OUTDIR, "bhrugu_story_exact_10m00s.mp3")
    st2 = loudnorm_two_pass(write_wav(y_ex, os.path.join(tmp, "exact.wav")), ex_mp3)
    print(f"[exact]   {dur_ex:.3f}s = {mmss(dur_ex)} -> {os.path.basename(ex_mp3)}")
    if st2:
        print(f"          loudness I={st2['input_i']} LUFS TP={st2['input_tp']} dBTP")

    info = {
        "natural": {"file": os.path.basename(nat_mp3), "duration_s": round(dur_nat, 2),
                    "atempo": 1.0, "gap_tightening": False},
        "exact": {"file": os.path.basename(ex_mp3), "duration_s": round(dur_ex, 3),
                  "atempo": round(factor, 4), "gap_tightening": True,
                  "gap_removed_s": round(removed, 1)},
        "pauses_s": BOUNDARY_PAUSES, "lead_in_s": LEAD_IN, "tail_s": TAIL,
        "part_marks_exact": [{"t": round(t, 2), "mmss": mmss(t), "part": p,
                              "act": PART_ACTS[p - 1]} for t, p in marks],
    }
    json.dump(info, open(os.path.join(OUTDIR, "build_info.json"), "w"), indent=1)
    print("\npart marks (exact master):")
    for t, p in marks:
        print(f"   part {p} (act {PART_ACTS[p - 1]}): {mmss(t)}")


if __name__ == "__main__":
    main()
