import sys
LANG = sys.argv[1]
assert LANG in ("hi","en")
#!/usr/bin/env python3
"""EP3 BGM engine — 10-cue bed synthesized against the REAL scene map, then
duck-mixed under the voice master (recipe inherited from EP2, user-approved levels).
Motif grammar: Q = 3-rise-then-fall bansuri (the question); A = 4-rise veena (Narada's answer).
Themes (blueprint §8): T1 Remembrance (Shivaranjani S01-06) · T2 Morning gold (Hamsadhwani S07-18)
· T2' ritual stillness (Kalyani thinning S19-26) · T3 Samadhi drone (S27-34) · T4 The Lord
(Mohanakalyani S35-41) · T5 Maya-veil shimmer (Bhairavi S42-46) · T6 Jiva sparks (santoor S47-52)
· T7 Bhakti river (Desh S53-58) · T8 Home/composition (Mohanam S59-68).
Instrument synthesizers: EP1/EP2 proven engines, verbatim.
Inputs : episode03/scene_map_ep4_{LANG}.json, episode03/EP04_CLEAN_VOICE_{LANG.upper()}.mp3
Outputs: episode03/EP04_WITH_BGM_{LANG.upper()}.mp3, episode03/EP04_BGM_STEM_{LANG.upper()}.mp3"""
import subprocess, json, os
import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.abspath(__file__)).replace('/postprod', '')
SR = 44100

sm = json.load(open(f"{ROOT}/scene_map_ep4_{LANG}.json"))
SC = {s['n']: s for s in sm['scenes']}
TOTAL = sm['total']
def T(n):   return SC[n]['start']
def TE(n):  return SC[n]['end']
def TVE(n): return SC[n]['vo_end']

SHIVARANJANI = [0, 2, 3, 7, 8]
KALYANI      = [0, 2, 4, 6, 7, 9, 11]
HAMSADHWANI  = [0, 2, 4, 7, 11]
MOHANAKALY   = [0, 2, 4, 7, 9, 11]
MOHANAM      = [0, 2, 4, 7, 9]
DESH         = [0, 2, 4, 5, 7, 9, 11]
BHAIRAVI     = [0, 1, 3, 5, 7, 8, 11]
SA = 130.81
def hz(off, base=SA): return base * 2.0 ** (off / 12.0)

def N(dur): return max(1, int(round(dur * SR)))
def add(buf, t0, sig, gain=1.0):
    i = int(round(t0 * SR))
    if i >= len(buf): return
    j = min(len(buf), i + len(sig))
    if j > i: buf[i:j] += gain * sig[:j - i]

def pluck(freq, dur, amp=0.30, bright=0.7, seed=0):
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n) / SR; y = np.zeros(n)
    for k in range(1, 7):
        fk = freq * k * (1.0 + 0.00035 * k * k)
        y += (1.0 / k ** 1.12) * np.sin(2 * np.pi * fk * t + 0.35 * np.sin(2 * np.pi * fk * t * 0.502)) \
             * np.exp(-t * (0.8 + 0.85 * k) / (max(dur, 0.3) * bright))
    y *= amp
    m = int(0.004 * SR); y[:m] *= np.linspace(0, 1, m)
    y[:m] += rng.standard_normal(m) * np.exp(-np.arange(m) / (0.0016 * SR)) * amp * 0.35
    return y.astype(np.float32)

def rpluck(freq, dur, amp=0.20, bright=0.7, seed=0):
    """reversed pluck — the veil's signature (sound arriving backward)."""
    return pluck(freq, dur, amp, bright, seed)[::-1].copy()

def flute(freq, dur, amp=0.22, seed=0, warm=False):
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n) / SR
    vib = 1.0 + 0.0042 * np.sin(2 * np.pi * (4.9 if not warm else 4.4) * t + rng.uniform(0, 6.28))
    f = np.full(n, freq); m = int(0.11 * SR)
    if m > 0: f[:m] = freq * 2.0 ** (np.linspace(-0.45, 0, m) / 12.0)
    ph = 2 * np.pi * np.cumsum(f * vib) / SR
    y = np.sin(ph) * amp
    y += np.convolve(rng.standard_normal(n), np.ones(48) / 48.0, 'same') * amp * 0.05
    a = min(int(0.09 * SR), max(1, n // 4)); r = min(int(0.28 * SR), max(1, n - a))
    e = np.ones(n); e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r)
    e *= (1.0 + 0.14 * np.sin(np.pi * np.minimum(t / max(dur, 0.01), 1.0)))
    return (y * e).astype(np.float32)

def pad(freqs, dur, amp=0.10, seed=0, a_t=1.8, r_t=2.2, wide=1.0):
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n) / SR; y = np.zeros(n)
    for f in freqs:
        for det in (-5.0 * wide, 6.0 * wide):
            fm = f * 2.0 ** (det / 1200.0); ph = 2 * np.pi * fm * t
            for k in range(1, 5):
                y += np.sin(k * ph + rng.uniform(0, 6.28)) / (k * 1.6)
    y = np.convolve(y, np.ones(9) / 9.0, 'same')
    y *= amp / max(1.0, np.abs(y).max())
    a = min(n // 2, int(a_t * SR)); r = min(n // 2, int(r_t * SR))
    e = np.ones(n); e[:a] = np.linspace(0, 1, a) ** 1.5; e[-r:] *= np.linspace(1, 0, r) ** 1.3
    return (y * e).astype(np.float32)

def thump(amp=0.5, dur=0.3, seed=0):
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n) / SR
    f = 95.0 + 75.0 * np.exp(-t / 0.02)
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.075) * amp
    c = int(0.007 * SR)
    y[:c] += rng.standard_normal(c) * np.exp(-np.arange(c) / 18.0) * amp * 0.5
    return y.astype(np.float32)

def tick(amp=0.12, dur=0.05, seed=0):
    rng = np.random.default_rng(seed)
    n = N(dur); nz = rng.standard_normal(n)
    hp = np.concatenate([[0], np.diff(nz)])
    return (hp * np.exp(-np.arange(n) / (0.008 * SR)) * amp).astype(np.float32)

def bell(freq, dur=2.2, amp=0.13, seed=0):
    n = N(dur); t = np.arange(n) / SR; y = np.zeros(n)
    for p, a, tau in [(1.0, 1.0, 2.6), (2.44, 0.5, 1.8), (4.10, 0.28, 1.2), (5.43, 0.16, 0.8)]:
        y += a * np.sin(2 * np.pi * freq * p * t) * np.exp(-t / tau)
    y *= amp
    m = int(0.003 * SR); y[:m] *= np.linspace(0, 1, m)
    return y.astype(np.float32)

def tanpura(buf, t_from, t_to, amp=0.045, base=SA):
    pat = [7, 12, 12, -12]; step = 1.15; t = t_from
    while t < t_to - 1.0:
        for i, off in enumerate(pat):
            add(buf, t + i * step, pluck(hz(off, base), 1.8,
                amp * (1.15 if off == -12 else 1.0), bright=1.4, seed=int(t * 10 + i)))
        t += step * 4

def melody(scale, base, dur_s, rng, density=0.5, amp=0.2, kind='flute', reg=0,
           tmin=0.9, tmargin=1.4):
    notes = []
    t = tmin + rng.uniform(0, 1.6)
    deg = 0 if rng.random() < 0.5 else int(rng.integers(0, len(scale)))
    while t < dur_s - tmargin:
        nd = float(rng.choice([0.7, 0.9, 1.1, 1.4, 1.8])) * (0.72 if density > 0.6 else 1.05)
        deg = int(np.clip(deg + int(rng.integers(-2, 3)), 0, len(scale) + 2))
        o, idx = divmod(deg, len(scale))
        notes.append((t, nd, scale[idx] + 12 * (o + reg)))
        t += nd + float(rng.choice([0.05, 0.15, 0.3, 0.55])) * (1.8 - 1.2 * density)
    out = np.zeros(N(dur_s), dtype=np.float32)
    for t0, nd, off in notes:
        f = hz(off, base)
        sig = flute(f, nd * 1.12, amp, seed=int(t0 * 97)) if kind == 'flute' \
            else pluck(f, nd * 2.0, amp, seed=int(t0 * 97))
        add(out, t0, sig)
    return out

def motif_Q(buf, t0, amp=0.12, seed=7):
    seq = [(0.0, 0, 0.55), (0.55, 2, 0.55), (1.10, 4, 0.7), (1.85, 2, 0.5), (2.35, 0, 0.9)]
    for dt, off, d in seq:
        add(buf, t0 + dt, flute(hz(off, SA * 2), d * 1.25, amp, seed=seed + int(t0)))

def motif_A(buf, t0, amp=0.16, seed=11, steps=(0, 2, 4, 7, 12), kind='pluck'):
    dt = 0.0
    for i, off in enumerate(steps):
        d = 0.55 if i < len(steps) - 1 else 1.6
        f = hz(off, SA * 2)
        sig = pluck(f, d * 1.5, amp, bright=1.0, seed=seed + int(t0 * 3 + i)) if kind == 'pluck' \
            else flute(f, d * 1.2, amp, seed=seed + int(t0 * 3 + i))
        add(buf, t0 + dt, sig); dt += d * 0.62

def stinger(buf, t0, seed=3):
    for k, off in enumerate([7, 9, 12]):
        add(buf, t0 + k * 0.22, pluck(hz(off, SA * 2), 0.5, 0.10, bright=1.8, seed=seed + k))
    add(buf, t0 + 0.7, tick(0.10, 0.05, seed=seed + 9))

def gait(buf, t0, t1, step=1.15, amp=0.16, seed=5, double=False):
    t = t0
    while t < t1:
        add(buf, t, thump(amp, 0.3, seed=seed + int(t)))
        if double: add(buf, t + step / 2, thump(amp * 0.6, 0.2, seed=seed + int(t) + 1))
        t += step

def heartbeat(buf, times, amp=0.30):
    for t in times: add(buf, t, thump(amp, 0.32, seed=int(t * 13)))

# ---------- compose the full bed ----------
bgm = np.zeros(N(TOTAL + 2), dtype=np.float32)
R = np.random.default_rng(20261008)

def segment(n0, n1, fn):
    t0, t1 = T(n0), TE(n1)
    fn(t0, t1, t1 - t0)


# ================= EP4 AMBIENT PRIMITIVES =================
rng2 = np.random.default_rng(777)

def river(t_from, t_to, amp=0.013):
    """Brown-noise river under nature scenes."""
    n = N(t_to - t_from)
    noi = rng2.normal(size=n).astype(np.float32)
    b = np.cumsum(noi)
    b = b / (np.abs(b).max() + 1e-9)
    k = int(0.5 * SR)
    sig = np.convolve(np.concatenate([b[:k], b[:n], b[:k]]), np.ones(k)/k, 'same')[k:k+n].astype(np.float32)
    f = int(4 * SR)
    env = np.ones(n, dtype=np.float32)
    env[:f] = np.linspace(0, 1, f); env[-f:] = np.linspace(1, 0, f)
    add(bgm, t_from, sig * amp * env)

def birds(t_from, t_to, density=0.14, amp=0.05, seed=9):
    """Tiny dawn birdsong: up-down sine glisses, sparse."""
    r = np.random.default_rng(seed)
    t = t_from + 1.0
    while t < t_to - 1.2:
        f1, f2 = r.uniform(1800, 3200), r.uniform(3500, 4800)
        dd = r.uniform(0.16, 0.42)
        n = N(dd); tt = np.arange(n) / SR
        fr = np.linspace(f1, f2, n // 2 + 1)
        mirror = fr[::-1]
        fr = np.concatenate([fr, mirror])[:n]
        if len(fr) < n: fr = np.pad(fr, (0, n - len(fr)), mode='edge')
        sw = np.sin(2 * np.pi * np.cumsum(fr) / SR) * r.uniform(0.5, 1.0)
        env = np.exp(-tt / (dd * 0.5)) * np.sin(np.linspace(0, np.pi, n))
        add(bgm, t, (sw * env * amp).astype(np.float32))
        t += r.uniform(1.0 / density, 1.5 / density)

# ================= EP4 TEN CUES (blueprint M1..M10) =================
def Q0(t0, t1, d):  # M1 S01-04 RECAP MEMORY (shivaranjani, carries EP3 breath)
    tanpura(bgm, t0, t1, amp=0.030)
    add(bgm, t0, melody(SHIVARANJANI, SA, d, R, density=0.16, amp=0.07, kind='flute'))
    motif_A(bgm, T(1) + 2.0, amp=0.10, seed=701)
    add(bgm, T(2) + 0.3, bell(hz(7, SA * 2), 2.0, 0.06))
    motif_A(bgm, T(4) + 0.5, amp=0.10, seed=702)
    add(bgm, TE(4) - 0.2, bell(hz(0, SA * 2), 2.6, 0.08))

def Q1(t0, t1, d):  # M2 S05-11 COMPOSING (deep peaceful veena, day-night lamp)
    tanpura(bgm, t0, t1, amp=0.034)
    add(bgm, t0, melody(MOHANAM, SA, d, R, density=0.20, amp=0.075, kind='pluck'))
    tt = T(5) + 1.0
    while tt < TE(10) - 0.5:
        add(bgm, tt, tick(0.05, 0.05, seed=int(tt * 13)))
        tt += float(R.uniform(1.4, 2.6))
    add(bgm, T(8) + 0.8, bell(hz(4, SA * 2), 1.8, 0.055))
    add(bgm, T(9) + 0.6, bell(hz(7, SA * 2), 2.2, 0.070))
    motif_Q(bgm, T(11) + 0.6, amp=0.09)

def Q2(t0, t1, d):  # M3 S12-21 SHUKA NATURE (light bansuri + river + birds)
    river(t0 - 1.0, T(40) + 2.0)
    birds(t0 + 0.5, TE(16) + 1.0, density=0.42, amp=0.045)
    tanpura(bgm, t0, t1, amp=0.028)
    add(bgm, t0, melody(HAMSADHWANI, SA * 2, d, R, density=0.30, amp=0.075, kind='flute'))
    motif_A(bgm, T(13) + 1.2, amp=0.11, kind='flute', seed=713)
    add(bgm, T(14) + 0.9, tick(0.07, 0.06, seed=714))
    add(bgm, T(14) + 1.5, tick(0.05, 0.06, seed=715))
    for i, n in enumerate((17, 18, 19)):
        add(bgm, T(n) + 0.8, bell(hz(7 - i * 2, SA * 2), 1.6, 0.05))
    add(bgm, T(20) + 0.6, flute(hz(0, SA * 2), 2.2, 0.085, seed=720, warm=True))
    motif_A(bgm, T(21) + 0.4, amp=0.12, kind='flute', seed=721)

def Q3(t0, t1, d):  # M4 S22-26 CONTRAST (santoor side vs flute side - both warm)
    tanpura(bgm, t0, t1, amp=0.024)
    add(bgm, t0, melody(DESH, SA, d * 0.55, R, density=0.34, amp=0.07, kind='pluck'))
    add(bgm, T(24), melody(HAMSADHWANI, SA * 2, d * 0.5, R, density=0.20, amp=0.065, kind='flute'))
    add(bgm, TE(26) - 0.5, bell(hz(0, SA * 2), 2.2, 0.06))

def Q4(t0, t1, d):  # M5 S27-31 FATHER-SON (warm cello-ish pad + soft Q&A)
    add(bgm, t0, pad([hz(0, SA), hz(7, SA), hz(12, SA)], d, 0.052, a_t=2.5, r_t=3.0))
    motif_Q(bgm, T(28) + 0.5, amp=0.095)
    motif_A(bgm, T(30) + 0.7, amp=0.115, kind='flute', seed=730)
    add(bgm, TE(31) - 0.4, bell(hz(7, SA * 2), 2.6, 0.075))

def Q5(t0, t1, d):  # M6 S32-40 DEPARTURE (sparse bhairavi veena, steps, canyon echo)
    tanpura(bgm, t0, t1, amp=0.026)
    add(bgm, t0, melody(BHAIRAVI, SA, d, R, density=0.11, amp=0.07, kind='pluck'))
    gait(bgm, T(34) + 0.5, TE(40), step=2.0, amp=0.05, seed=732)
    heartbeat(bgm, [T(34) + 2.0], amp=0.16)
    add(bgm, T(37) + 0.9, bell(hz(4, SA * 2), 1.6, 0.06))
    add(bgm, T(38) + 1.8, bell(hz(4, SA * 2), 2.2, 0.035))
    add(bgm, T(38) + 4.4, bell(hz(4, SA * 2), 2.6, 0.020))
    heartbeat(bgm, [TE(40) - 1.0], amp=0.14)

def Q6(t0, t1, d):  # M7 S41-44 BECOMING (two brightening steps)
    add(bgm, t0, melody(HAMSADHWANI, SA * 2, d, R, density=0.42, amp=0.09, kind='flute'))
    add(bgm, T(42) + 0.5, pad([hz(0, SA * 2), hz(7, SA * 2)], d * 0.5, 0.05, a_t=1.5))
    motif_A(bgm, T(44) + 0.3, amp=0.15, seed=744)
    add(bgm, T(44) + 1.6, bell(hz(0, SA * 2), 2.8, 0.11))
    add(bgm, T(44) + 2.2, bell(hz(7, SA * 2), 2.8, 0.085))

def Q7(t0, t1, d):  # M8 S45-48 REMEMBRANCE (home veena, quiet)
    tanpura(bgm, t0, t1, amp=0.026)
    add(bgm, t0, melody(SHIVARANJANI, SA, d, R, density=0.18, amp=0.065, kind='pluck'))
    add(bgm, T(47) + 0.8, bell(hz(0, SA * 2), 2.4, 0.06))
    add(bgm, T(48) + 2.0, flute(hz(4, SA * 2), 2.0, 0.05, seed=748, warm=True))

def Q8(t0, t1, d):  # M9 S49-52 FORESHADOW (low hanging bells + heartbeat)
    add(bgm, t0, pad([hz(0, SA)], d, 0.045, a_t=2.0, wide=1.3))
    tt = T(49) + 0.6
    while tt < t1:
        add(bgm, tt, bell(hz(-5, SA), 2.8, 0.055)); tt += 2.4
    heartbeat(bgm, [T(49) + 0.4, T(51) + 0.2], amp=0.18)
    add(bgm, T(52) + 1.5, flute(hz(4, SA * 2), 1.8, 0.07, seed=752, warm=True))

def Q9(t0, t1, d):  # M10 S53-56 QUESTIONS -> CARD (three suspense pulls, rising swell)
    at = T(55)
    for k, off in enumerate((2.5, 5.0, 7.5)):
        add(bgm, at + off, tick(0.10, 0.06, seed=755 + k))
        add(bgm, at + off + 0.30, tick(0.07, 0.06, seed=758 + k))
    add(bgm, T(53), pad([hz(0, SA), hz(7, SA)], t1 - T(53), 0.045, a_t=4.0))
    add(bgm, T(56) + 1.0, bell(hz(0, SA * 2), 3.2, 0.13))
    add(bgm, T(56) + 3.4, flute(hz(0, SA * 2), 2.0, 0.10, seed=756, warm=True))
    add(bgm, T(56) + 5.6, flute(hz(7, SA * 2), 2.6, 0.09, seed=757, warm=True))
    heartbeat(bgm, [T(56) + 8.0], amp=0.20)
    add(bgm, TE(56) - 1.2, bell(hz(7, SA * 2), 3.0, 0.10))

for n0, n1, fn in [(1, 4, Q0), (5, 11, Q1), (12, 21, Q2), (22, 26, Q3), (27, 31, Q4),
                   (32, 40, Q5), (41, 44, Q6), (45, 48, Q7), (49, 52, Q8), (53, 56, Q9)]:
    segment(n0, n1, fn)

f = int(2.0 * SR); bgm[:f] *= np.linspace(0, 1, f); bgm[-f:] *= np.linspace(1, 0, f)
bgm *= 0.9 / max(1e-6, np.abs(bgm).max())

def decode(fpath):
    out = subprocess.run([FF, '-v', 'error', '-i', fpath, '-f', 'f32le', '-ac', '1',
                          '-ar', str(SR), '-'], capture_output=True, check=True)
    return np.frombuffer(out.stdout, dtype=np.float32)

voice = decode(f"{ROOT}/EP04_CLEAN_VOICE_{LANG.upper()}.mp3")
L = min(len(voice), len(bgm)); voice = voice[:L]; bed = bgm[:L]
env = np.abs(voice)
w = int(0.09 * SR); env = np.convolve(env, np.ones(w) / w, 'same')
mask = np.clip(env / 0.06, 0, 1)
DUCK = 0.80
gain = 1.0 - DUCK * mask
bed = bgm[:L].copy(); bed *= gain * 0.38
mix = voice + bed
peak = np.abs(mix).max()
if peak > 0.89: mix *= 0.89 / peak

def write_mp3(sig, out, q='2', norm=True):
    wav = "/tmp/_bgmx3.wav"
    subprocess.run([FF, '-y', '-v', 'error', '-f', 'f32le', '-ac', '1', '-ar', str(SR),
                    '-i', '-', '-c:a', 'pcm_s16le', wav], input=sig.tobytes(), check=True)
    args = [FF, '-y', '-v', 'error', '-i', wav]
    if norm: args += ['-af', 'loudnorm=I=-16:TP=-1.5:LRA=11']
    args += ['-ar','44100','-c:a', 'libmp3lame', '-q:a', q, out]
    subprocess.run(args, check=True)

write_mp3(mix, f"{ROOT}/EP04_WITH_BGM_{LANG.upper()}.mp3")
write_mp3(bgm[:L], f"{ROOT}/EP04_BGM_STEM_{LANG.upper()}.mp3", q='3', norm=False)
rms = np.sqrt(np.mean(mix ** 2)); print(f"OK EP04_WITH_BGM_{LANG.upper()}.mp3 {L/SR/60:.1f} min | mix RMS {20*np.log10(max(rms,1e-9)):.1f} dBFS | stem saved")
