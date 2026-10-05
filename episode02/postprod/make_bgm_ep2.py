#!/usr/bin/env python3
"""EP2 BGM engine — 6-theme bed synthesized against the REAL scene map, then
duck-mixed under the voice master.
Themes (blueprint §8): T1 Question Remains (Shivaranjani) · T2 Answer Arriving
(MohanaKalyani veena) · T3 Greatness Accounted (Kalyani) · T4 Teaching Metaphors
(Hamsadhwani bamboo) · T5 Narada's Story (Desh/Bhairavi memory-gold) · T6 Sankalpa
home (Mohanam). Motif grammar: Q = 3-rise-then-fall bansuri; A = 4-rise veena.
Instrument synthesizers are the proven EP1 engines (bgm_mix.py lineage).

Inputs : episode02/scene_map_ep2.json, episode02/EP02_CLEAN_VOICE.mp3
Outputs: episode02/EP02_WITH_BGM.mp3 (narration + soft bed master)
         episode02/EP02_BGM_STEM.mp3 (the bed alone, for the picture mix)
"""
import subprocess, json, os, sys
import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.abspath(__file__)).replace('/postprod', '')
SR = 44100

sm = json.load(open(f"{ROOT}/scene_map_ep2.json"))
SC = {s['n']: s for s in sm['scenes']}
TOTAL = sm['total']
def T(n):   return SC[n]['start']
def TE(n):  return SC[n]['end']
def TVE(n): return SC[n]['vo_end']

# ---------- scales / motifs ----------
SHIVARANJANI = [0, 2, 3, 7, 8]
KALYANI      = [0, 2, 4, 6, 7, 9, 11]
HAMSADHWANI  = [0, 2, 4, 7, 11]
MOHANAKALY   = [0, 2, 4, 7, 9, 11]
MOHANAM      = [0, 2, 4, 7, 9]
DESH         = [0, 2, 4, 5, 7, 9, 11]
SA = 130.81
def hz(off, base=SA): return base * 2.0 ** (off / 12.0)

# ---------- proven EP1 synthesizers (identical engines) ----------
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

def pad(freqs, dur, amp=0.10, seed=0, a_t=1.8, r_t=2.2):
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n) / SR; y = np.zeros(n)
    for f in freqs:
        for det in (-5.0, 6.0):
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

# ---------- motifs / set-pieces ----------
def motif_Q(buf, t0, amp=0.12, seed=7):
    """3-rise bansuri then the falling tail (the question)."""
    seq = [(0.0, 0, 0.55), (0.55, 2, 0.55), (1.10, 4, 0.7), (1.85, 2, 0.5), (2.35, 0, 0.9)]
    for dt, off, d in seq:
        add(buf, t0 + dt, flute(hz(off, SA * 2), d * 1.25, amp, seed=seed + int(t0)))

def motif_A(buf, t0, amp=0.16, seed=11, steps=(0, 2, 4, 7, 12), kind='pluck'):
    """4-rise veena answer (the episode's grammar)."""
    dt = 0.0
    for i, off in enumerate(steps):
        d = 0.55 if i < len(steps) - 1 else 1.6
        f = hz(off, SA * 2)
        sig = pluck(f, d * 1.5, amp, bright=1.0, seed=seed + int(t0 * 3 + i)) if kind == 'pluck' \
            else flute(f, d * 1.2, amp, seed=seed + int(t0 * 3 + i))
        add(buf, t0 + dt, sig); dt += d * 0.62

def stinger(buf, t0, seed=3):
    """playful dotara triplet + tick — humour beats (S20/S33/S43)."""
    for k, off in enumerate([7, 9, 12]):
        add(buf, t0 + k * 0.22, pluck(hz(off, SA * 2), 0.5, 0.10, bright=1.8, seed=seed + k))
    add(buf, t0 + 0.7, tick(0.10, 0.05, seed=seed + 9))

def gait(buf, t0, t1, step=1.15, amp=0.16, seed=5, double=False):
    """festival mridangam walk."""
    t = t0
    while t < t1:
        add(buf, t, thump(amp, 0.3, seed=seed + int(t)))
        if double: add(buf, t + step / 2, thump(amp * 0.6, 0.2, seed=seed + int(t) + 1))
        t += step

def heartbeat(buf, times, amp=0.30):
    for t in times: add(buf, t, thump(amp, 0.32, seed=int(t * 13)))

# ---------- compose the full bed ----------
bgm = np.zeros(N(TOTAL + 2), dtype=np.float32)
R = np.random.default_rng(20261005)

def segment(n0, n1, fn):
    t0, t1 = T(n0), TE(n1)
    fn(t0, t1, t1 - t0)

def P0(t0, t1, d):  # S01–06 · T1 Question Remains
    tanpura(bgm, t0, t1, amp=0.035)
    for tt in [t0, t0 + d * 0.45]:
        add(bgm, tt, pad([hz(0), hz(7), hz(-12)], d * 0.55, 0.055, a_t=3.0, r_t=3.0))
    motif_Q(bgm, T(4) + 0.5, amp=0.10)
    heartbeat(bgm, [T(4) + 2.0, T(6) + 0.5], amp=0.22)
    add(bgm, T(5) + 0.5, melody(SHIVARANJANI, SA * 2, TE(6) - T(5), R, density=0.22, amp=0.08, kind='flute'))

def P1(t0, t1, d):  # S07–15 · T2 Answer Arriving
    tanpura(bgm, t0, t1, amp=0.045)
    add(bgm, t0, pad([hz(0), hz(7), hz(12)], d, 0.06, a_t=2.5, r_t=2.5))
    add(bgm, t0, melody(MOHANAKALY, SA * 2, d, R, density=0.42, amp=0.11, kind='pluck'))
    gait(bgm, T(11), TE(15), step=1.15, amp=0.13)       # the walking rhythm enters with him
    motif_A(bgm, T(13) + 0.3, amp=0.15)                  # the veena completes its own theme
    add(bgm, T(14) + 0.5, melody(HAMSADHWANI, SA * 2, TE(15) - T(14), R, density=0.35, amp=0.09, kind='flute'))
    add(bgm, T(15) + 1.0, bell(hz(12, SA), 2.4, 0.10))

def P2(t0, t1, d):  # S16–23 · T3 Greatness Accounted (welcome)
    tanpura(bgm, t0, t1, amp=0.04)
    add(bgm, t0, pad([hz(0), hz(4), hz(7)], d, 0.055, a_t=2.0, r_t=2.0))
    add(bgm, t0, melody(KALYANI, SA * 2, d, R, density=0.32, amp=0.10, kind='pluck'))
    stinger(bgm, T(20) + 1.2, seed=21)                   # humour beat 1
    add(bgm, T(23) + 0.5, pad([hz(0), hz(-7)], TE(23) - T(23), 0.05, a_t=1.2, r_t=2.0))  # shadow seed

def P3(t0, t1, d):  # S24–33 · the probe & THE CONFESSION
    tanpura(bgm, t0, T(29), amp=0.035)
    add(bgm, t0, pad([hz(0), hz(7)], T(29) - t0, 0.045, a_t=2.0, r_t=2.0))
    add(bgm, T(26), melody(KALYANI, SA, T(29) - T(26), R, density=0.28, amp=0.09, kind='pluck'))
    heartbeat(bgm, [T(25) + 1.0, T(25) + 3.4, T(29) + 4.0], amp=0.24)
    # S30 — everything naked except ONE sustained low string under the whole scene:
    sd = TE(30) - T(30)
    add(bgm, T(30) - 0.4, pad([hz(-12, SA)], sd + 0.8, 0.075, a_t=0.6, r_t=2.0))
    add(bgm, TVE(30) + 0.3, pluck(hz(12, SA), 2.6, 0.10, bright=1.5, seed=30))   # harmonic after the line
    motif_Q(bgm, T(31) + 0.8, amp=0.08)                  # whisper-frag
    add(bgm, T(32) + 0.6, pluck(hz(0, SA * 2), 2.0, 0.13, bright=1.1, seed=32))  # answer's first note
    stinger(bgm, T(33) + 1.0, seed=33)                   # humour beat 2

def P4(t0, t1, d):  # S34–46 · T4 Teaching Metaphors
    tanpura(bgm, t0, t1, amp=0.042)
    add(bgm, t0, pad([hz(0), hz(7), hz(12)], d, 0.05, a_t=2.0, r_t=2.0))
    add(bgm, t0, melody(HAMSADHWANI, SA * 2, d, R, density=0.5, amp=0.11, kind='flute'))
    add(bgm, T(35), melody(MOHANAM, SA * 4, TE(38) - T(35), R, density=0.3, amp=0.05, kind='pluck'))  # santoor sprinkle
    motif_A(bgm, T(34) + 2.0, amp=0.12)                  # the 'but' opens the answer
    add(bgm, T(40) + 0.5, bell(hz(0, SA * 2), 2.2, 0.10)); add(bgm, T(40) + 3.5, bell(hz(7, SA * 2), 2.0, 0.08))
    for k in range(3):                                    # S41 three ascent chimes
        add(bgm, T(41) + 0.8 + k * 1.1, bell(hz([0, 4, 7][k], SA * 2), 1.6, 0.075))
    stinger(bgm, T(43) + 0.8, seed=43)                   # veena joke pat
    # S45 — the QUESTION played REVERSED upward (understanding turns):
    dt = 0.0
    for off in [0, 2, 4, 7]:
        add(bgm, T(45) + 0.5 + dt, flute(hz(off, SA * 2), 0.75, 0.11, seed=int(T(45)) + off)); dt += 0.55
    add(bgm, T(45) + 0.5, pad([hz(0), hz(4)], TE(45) - T(45) + TE(46) - T(46), 0.05))

def P5(t0, t1, d):  # S47–56 · T5 Narada's own story (memory-gold)
    tanpura(bgm, t0, t1, amp=0.038, base=SA)
    add(bgm, t0, melody(DESH, SA * 2, d, R, density=0.38, amp=0.10, kind='flute'))
    gait(bgm, T(49), TE(52), step=1.6, amp=0.10)         # dotara home-heartbeat
    add(bgm, T(47), pad([hz(0), hz(5)], d * 0.6, 0.05, a_t=3.0))     # warm golden memory pad
    add(bgm, T(53) - 0.5, pad([hz(-12, SA), hz(0)], TE(53) - T(53) + 1.5, 0.07, a_t=1.0, r_t=2.5))  # empty-hut held note
    gait(bgm, T(54), TE(54), step=1.0, amp=0.09)         # the lone walk
    # S55 the vision — soft chorus-ish wide pad + shimmer:
    add(bgm, T(55) - 0.3, pad([hz(0, SA * 2), hz(4, SA * 2), hz(7, SA * 2), hz(12, SA * 2)],
        TE(55) - T(55) + 1.0, 0.075, a_t=1.6, r_t=2.2))
    for k in range(3):
        add(bgm, T(55) + 1.5 + k * 1.7, bell(hz([0, 7, 12][k], SA * 4), 2.6, 0.045))
    motif_A(bgm, T(51) + 1.0, amp=0.11, kind='flute')    # katha plants the whole answer on bamboo
    motif_A(bgm, T(56) + 0.5, amp=0.13)                  # handoff resolve

def P6(t0, t1, d):  # S57–62 · the charge & departure
    tanpura(bgm, t0, T(62), amp=0.045)
    add(bgm, t0, pad([hz(0), hz(7), hz(12)], T(62) - t0, 0.055, a_t=1.5, r_t=2.0))
    motif_A(bgm, t0 + 0.3, amp=0.15)
    add(bgm, T(57), melody(MOHANAKALY, SA * 2, T(62) - T(57), R, density=0.45, amp=0.11, kind='pluck'))
    add(bgm, T(58) + 1.0, bell(hz(12, SA), 2.6, 0.11))   # the charge placed
    gait(bgm, T(60), TE(60), step=0.575, amp=0.16, double=True)  # ★ CREST festival stroke
    motif_A(bgm, T(60) + 0.5, amp=0.18)
    add(bgm, T(61), pad([hz(0), hz(4)], TE(61) - T(61), 0.055, a_t=0.8, r_t=2.5))       # decrescendo bow
    motif_A(bgm, T(62) + 0.5, amp=0.11, steps=(0, 2, 4, 7))  # solo veena leaves with him
    add(bgm, TE(62) - 1.5, pad([hz(0)], TE(62) - T(62) + 1.0, 0.03, a_t=0.4))

def P7(t0, t1, d):  # S63–69 · T6 Sankalpa / new dawn
    tanpura(bgm, t0, T(68), amp=0.042)
    add(bgm, t0, melody(MOHANAM, SA * 2, T(66) - T(63), R, density=0.4, amp=0.10, kind='flute'))
    add(bgm, t0, pad([hz(0), hz(7)], T(67) - t0, 0.05, a_t=2.0))
    # S64 — Q and A together; the ANSWER carries the phrase:
    motif_Q(bgm, T(64) + 0.3, amp=0.08)
    motif_A(bgm, T(64) + 1.2, amp=0.15)
    add(bgm, T(65) + 0.5, bell(hz(0, SA * 2), 2.0, 0.07))
    add(bgm, T(66), melody(DESH, SA * 4, TE(66) - T(66), R, density=0.3, amp=0.05, kind='pluck'))  # santoor desk-ritual
    motif_A(bgm, T(67) + 0.5, amp=0.12, kind='flute')    # meditation tempo
    # S68 — final full cadence then decrescendo:
    motif_A(bgm, T(68) + 0.5, amp=0.17)
    add(bgm, T(68) + 0.5, pad([hz(0, SA * 2), hz(7, SA * 2)], TE(68) - T(68) + 1.0, 0.06, a_t=0.7, r_t=2.5))
    heartbeat(bgm, [TE(68) - 1.0], amp=0.22)
    # S69 — harmonic, two open notes, ONE heartbeat at the last frame:
    add(bgm, T(69) + 0.8, pluck(hz(12, SA), 3.0, 0.09, bright=1.6, seed=69))
    add(bgm, T(69) + 2.5, flute(hz(0, SA * 2), 1.4, 0.09, seed=691))
    add(bgm, T(69) + 4.0, flute(hz(2, SA * 2), 2.2, 0.09, seed=692))
    heartbeat(bgm, [TE(69) - 0.8], amp=0.30)

for n0, n1, fn in [(1, 6, P0), (7, 15, P1), (16, 23, P2), (24, 33, P3),
                   (34, 46, P4), (47, 56, P5), (57, 62, P6), (63, 69, P7)]:
    segment(n0, n1, fn)

# fade the very head/tail of the bed
f = int(2.0 * SR); bgm[:f] *= np.linspace(0, 1, f); bgm[-f:] *= np.linspace(1, 0, f)
bgm *= 0.9 / max(1e-6, np.abs(bgm).max())

# ---------- duck-mix under the voice ----------
def decode(f):
    out = subprocess.run([FF, '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '1',
                          '-ar', str(SR), '-'], capture_output=True, check=True)
    return np.frombuffer(out.stdout, dtype=np.float32)

voice = decode(f"{ROOT}/EP02_CLEAN_VOICE.mp3")
L = min(len(voice), len(bgm)); voice = voice[:L]; bed = bgm[:L]
env = np.abs(voice)
w = int(0.09 * SR); env = np.convolve(env, np.ones(w) / w, 'same')
mask = np.clip(env / 0.06, 0, 1)
DUCK = 0.55
gain = 1.0 - DUCK * mask
bed *= gain * 0.85
mix = voice + bed
peak = np.abs(mix).max()
if peak > 0.89: mix *= 0.89 / peak

def write_mp3(sig, out, q='2', norm=True):
    wav = "/tmp/_bgmx.wav"
    subprocess.run([FF, '-y', '-v', 'error', '-f', 'f32le', '-ac', '1', '-ar', str(SR),
                    '-i', '-', '-c:a', 'pcm_s16le', wav], input=sig.tobytes(), check=True)
    args = [FF, '-y', '-v', 'error', '-i', wav]
    if norm: args += ['-af', 'loudnorm=I=-16:TP=-1.5:LRA=11']
    args += ['-c:a', 'libmp3lame', '-q:a', q, out]
    subprocess.run(args, check=True)

write_mp3(mix, f"{ROOT}/EP02_WITH_BGM.mp3")
write_mp3(bgm[:L], f"{ROOT}/EP02_BGM_STEM.mp3", q='3', norm=False)
rms = np.sqrt(np.mean(mix ** 2)); print(f"OK EP02_WITH_BGM.mp3 {L/SR/60:.1f} min | mix RMS {20*np.log10(max(rms,1e-9)):.1f} dBFS | stem saved")
