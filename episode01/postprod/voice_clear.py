#!/usr/bin/env python3
"""
v4 CLARITY MIX — request: words crystal-clear, calm, pleasant; length can grow.
- narration at 100% natural TTS pace (NO atempo, NO hard time-fits)
- pauses kept generous (capped 0.95s — calm, not sleepy)
- background = optional ultra-soft tanpura+pad bed only (no birds/bells/fire/steps)
- video timeline expands per scene so nothing is squeezed
Outputs: EP01_CLEAN_VOICE.mp3 (narration only) · EP01_SOFT_BED.mp3 (voice + faint bed)
         audio_clean/EP01_Snn.mp3 (66) · /tmp/scenes_v4.json (expanded scene windows)
"""
import os, json, subprocess, numpy as np, imageio_ffmpeg
from wave import open as wopen

FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 22050
ROOT = "/home/user/youtube1/episode01"; WORK = "/tmp/bgmwork"
os.makedirs(WORK, exist_ok=True)

DESIGN = [10,10,10,11,12,13,12,12,13,13,12,12,13,14,13,12,13,13,13,14,15,12,12,12,13,
          13,13,13,14,13,15,13,13,13,13,15,15,13,13,13,14,13,13,13,13,13,13,13,13,14,
          12,12,12,12,12,12,12,12,12,12,12,12,10,13,13,15]           # scenes 1..66 seconds

# ---------- voice helpers (from bgm_mix, quiet edition) ----------
def N(d): return max(1, int(round(d*SR)))

def compress_pauses(vo, sr, max_pause=0.95, floor=0.012):
    fl = int(0.02*sr); nf = len(vo)//fl
    if nf == 0: return vo
    rms = np.sqrt(np.mean(vo[:nf*fl].reshape(nf, fl)**2, axis=1))
    speech = rms > max(floor, rms.max()*0.06)
    out = []; i = 0
    while i < nf:
        j = i
        if speech[i]:
            while j < nf and speech[j]: j += 1
            out.append(vo[i*fl:j*fl])
        else:
            while j < nf and not speech[j]: j += 1
            run = (j-i)*fl/sr
            out.append(vo[i*fl:i*fl+int(min(run, max_pause)*sr)])
        i = j
    if not out: return vo
    res = np.concatenate(out).astype(np.float32)
    m = int(0.015*sr)
    if len(res) > 2*m: res[:m] *= np.linspace(0,1,m); res[-m:] *= np.linspace(1,0,m)
    return res

def add(buf, t0, sig, gain=1.0):
    i = int(round(t0*SR))
    if i >= len(buf): return
    j = min(len(buf), i+len(sig))
    if j > i: buf[i:j] += gain*sig[:j-i]

SA = 130.81
def hz(o, base=SA): return base*2.0**(o/12.0)

def pluck(freq, dur, amp=0.2, bright=0.7, seed=0):
    rng = np.random.default_rng(seed); n = N(dur); t = np.arange(n)/SR; y = np.zeros(n)
    for k in range(1, 6):
        fk = freq*k*(1.0+0.00035*k*k)
        y += (1.0/k**1.15)*np.sin(2*np.pi*fk*t)*np.exp(-t*(0.9+0.9*k)/(max(dur,0.3)*bright))
    y *= amp; m = max(2, int(0.004*SR)); y[:m] *= np.linspace(0,1,m)
    return y.astype(np.float32)

def pad(freqs, dur, amp=0.05, seed=0):
    rng = np.random.default_rng(seed); n = N(dur); t = np.arange(n)/SR; y = np.zeros(n)
    for f in freqs:
        for det in (-5.0, 6.0):
            ph = 2*np.pi*f*2.0**(det/1200.0)*t
            for k in range(1, 4): y += np.sin(k*ph + rng.uniform(0, 6.28))/(k*1.8)
    y = np.convolve(y, np.ones(9)/9.0, 'same'); y *= amp/max(1e-9, np.abs(y).max())
    a = min(n//2, int(2.5*SR)); e = np.ones(n)
    e[:a] = np.linspace(0,1,a)**1.4; e[-a:] *= np.linspace(1,0,a)**1.4
    return (y*e).astype(np.float32)

def tanpura(buf, dur, amp=0.014, base=SA):
    t = 0.2
    while t < dur-1.0:
        for i, off in enumerate([7, 12, 12, -12]):
            if t+i*1.15 < dur-0.5:
                add(buf, t+i*1.15, pluck(hz(off, base), 1.8, amp*(1.15 if off==-12 else 1.0), 1.4, int(t*13+i)))
        t += 4.6

def motif(buf, dur, kind, amp=0.055):
    """faint emotional hints only at the key moments"""
    offs = [0,2,3,-4] if kind == 'q' else [0,4,7,12]
    t = 1.0
    for o in offs:
        add(buf, t, pluck(hz(o, SA*2), 1.5, amp, 1.3, int(o*7+t*10)))
        t += 0.9

# ---------- build ----------
print("v4: natural-pace narration…")
Q_SCENES = {20, 30, 33, 37, 48, 65}; A_SCENES = {53, 54, 56, 59, 61, 64, 66}
vos, durs = [], []
for n in range(1, 67):
    mp3 = os.path.join(ROOT, 'audio', f'EP01_S{n:02d}.mp3')
    o = subprocess.run([FF, '-v', 'error', '-i', mp3, '-f', 'f32le', '-ac', '1',
                        '-ar', str(SR), '-'], capture_output=True)
    raw = np.frombuffer(o.stdout, dtype=np.float32).copy()
    assert len(raw) > SR, f"S{n:02d} decode failed/empty!"
    vo = compress_pauses(raw, SR, 0.95)
    vos.append(vo)
    durs.append(max(float(DESIGN[n-1]), len(vo)/SR + 0.9))
starts = np.cumsum([0.0] + durs[:-1]).tolist()
TOTAL = starts[-1] + durs[-1]
print(f"  new runtime: {TOTAL/60:.2f} min (design 13:58) — visuals will expand to match")

vob = np.zeros(N(TOTAL), dtype=np.float32)
for (vo, t0) in zip(vos, starts):
    add(vob, t0 + 0.45, vo*0.98)

print("v4: ultra-soft bed…")
bed = np.zeros(N(TOTAL), dtype=np.float32)
for i in range(66):
    d = durs[i]; seg = np.zeros(N(d), dtype=np.float32)
    seg += pad([hz(-24), hz(-12)], d, amp=0.045, seed=900+i)
    tanpura(seg, d)
    n = i+1
    if n in Q_SCENES: motif(seg, d, 'q')
    if n in A_SCENES: motif(seg, d, 'a')
    add(bed, starts[i], seg)

env = np.abs(vob); k = np.ones(int(0.30*SR))/int(0.30*SR)
mask = np.clip(np.convolve((env > 0.010).astype(np.float32), k, 'same')*2.2, 0, 1)
bed *= (1.0 - 0.78*mask)                                                # bed nearly vanishes under speech

def master(sig, name):
    sig = sig/max(1e-9, np.abs(sig).max())*0.94
    w = os.path.join(WORK, name + '.wav')
    with wopen(w, 'wb') as f:
        f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR)
        f.writeframes((np.clip(sig, -1, 1)*32767).astype('<i2').tobytes())
    nm = os.path.join(WORK, name + '_n.wav')
    subprocess.run([FF, '-y', '-v', 'error', '-i', w,
                    '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-ac', '2', nm], check=True)
    out = os.path.join(ROOT, name + '.mp3')
    subprocess.run([FF, '-y', '-v', 'error', '-i', nm, '-b:a', '192k', out], check=True)
    print("  →", out)
    return nm

n_clean = master(vob, 'EP01_CLEAN_VOICE')
master(vob*1.0 + bed*0.65, 'EP01_SOFT_BED')

oc = os.path.join(ROOT, 'audio_clean'); os.makedirs(oc, exist_ok=True)
for i in range(66):
    outp = os.path.join(oc, f'EP01_S{i+1:02d}.mp3')
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{starts[i]:.2f}', '-t', f'{durs[i]:.2f}',
                    '-i', n_clean, '-af', 'afade=t=in:st=0:d=0.08', '-b:a', '160k', outp], check=True)
json.dump({'scenes': [{'n': i+1, 'start': starts[i], 'dur': durs[i]} for i in range(66)],
           'total': TOTAL}, open('/tmp/scenes_v4.json', 'w'))
print(f"  66 clean clips → {oc}; scene map → /tmp/scenes_v4.json")
