#!/usr/bin/env python3
"""EP3 BGM engine — 8-theme bed synthesized against the REAL scene map, then
duck-mixed under the voice master (recipe inherited from EP2, user-approved levels).
Motif grammar: Q = 3-rise-then-fall bansuri (the question); A = 4-rise veena (Narada's answer).
Themes (blueprint §8): T1 Remembrance (Shivaranjani S01-06) · T2 Morning gold (Hamsadhwani S07-18)
· T2' ritual stillness (Kalyani thinning S19-26) · T3 Samadhi drone (S27-34) · T4 The Lord
(Mohanakalyani S35-41) · T5 Maya-veil shimmer (Bhairavi S42-46) · T6 Jiva sparks (santoor S47-52)
· T7 Bhakti river (Desh S53-58) · T8 Home/composition (Mohanam S59-68).
Instrument synthesizers: EP1/EP2 proven engines, verbatim.
Inputs : episode03/scene_map_ep3.json, episode03/EP03_CLEAN_VOICE.mp3
Outputs: episode03/EP03_WITH_BGM.mp3, episode03/EP03_BGM_STEM.mp3"""
import subprocess, json, os
import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.abspath(__file__)).replace('/postprod', '')
SR = 44100

sm = json.load(open(f"{ROOT}/scene_map_ep3.json"))
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

def P0(t0, t1, d):  # S01–06 · T1 Remembrance (night after the answer)
    tanpura(bgm, t0, t1, amp=0.032)
    for tt in [t0, t0 + d * 0.4]:
        add(bgm, tt, pad([hz(0), hz(7), hz(-12)], d * 0.6, 0.05, a_t=3.0, r_t=3.0))
    motif_Q(bgm, T(4) + 0.5, amp=0.08)                       # the question, quiet now
    motif_A(bgm, T(2) + 0.4, amp=0.13)                       # echo of Narada's answer (S02)
    add(bgm, T(2) + 2.2, pluck(hz(12, SA), 2.6, 0.09, bright=1.6, seed=2))
    motif_A(bgm, T(3) + 0.3, amp=0.12, kind='flute')        # the rise recalled on bamboo
    add(bgm, T(5) + 0.5, melody(SHIVARANJANI, SA * 2, TE(6) - T(5), R, density=0.2, amp=0.07, kind='flute'))

def P1(t0, t1, d):  # S07–18 · T2 Morning gold (Hamsadhwani)
    tanpura(bgm, t0, t1, amp=0.045)
    add(bgm, t0, pad([hz(0), hz(7), hz(12)], d, 0.055, a_t=2.5, r_t=2.5))
    add(bgm, t0, melody(HAMSADHWANI, SA * 2, d, R, density=0.42, amp=0.10, kind='flute'))
    add(bgm, T(8), melody(MOHANAM, SA * 4, TE(10) - T(8), R, density=0.28, amp=0.045, kind='pluck'))  # santoor on the desk
    gait(bgm, T(13), TE(14), step=1.15, amp=0.11)           # the small procession
    stinger(bgm, T(17) + 1.0, seed=17)                       # ★ humor beat 1 — asana rush
    add(bgm, T(18) + 0.5, pad([hz(0), hz(4)], TE(18) - T(18) + 1.0, 0.05, a_t=1.5, r_t=2.2))  # thinning toward the seat

def P2(t0, t1, d):  # S19–26 · ritual of stillness (T2 condenses)
    tanpura(bgm, t0, T(24), amp=0.04)
    add(bgm, t0, pad([hz(0), hz(7)], T(24) - t0, 0.05, a_t=2.0, r_t=2.0))
    add(bgm, T(19), bell(hz(7, SA * 2), 2.2, 0.08))          # achamana
    add(bgm, T(20), bell(hz(12, SA * 2), 2.2, 0.07))         # water returned
    add(bgm, T(21), melody(KALYANI, SA * 2, TE(24) - T(21), R, density=0.25, amp=0.08, kind='pluck'))
    add(bgm, T(23), flute(hz(0, SA * 2), 2.5, 0.09, seed=23, warm=True))   # the leaf glides
    motif_A(bgm, T(25) + 0.3, amp=0.13)                      # ★ anchor #2 — blessing hand
    add(bgm, T(25), pad([hz(0), hz(5)], TE(25) - T(25), 0.055, a_t=1.5))
    add(bgm, T(26), pad([hz(-12, SA)], TE(26) - T(26) + 2.0, 0.05, a_t=1.0, r_t=3.0))  # eyes close: world falls away
    heartbeat(bgm, [T(26) + 1.2], amp=0.18)

def P3(t0, t1, d):  # S27–34 · T3 SAMADHI (drone, heartbeat slows to silence)
    add(bgm, t0, pad([hz(-12, SA), hz(7, SA), hz(0)], TE(31) - t0, 0.065, a_t=4.0, r_t=3.0, wide=1.6))
    tanpura(bgm, t0, T(29), amp=0.028)
    hb = []; tt = T(27) + 1.0; st = 60 / 50.0                # 50 bpm
    while tt < T(29) + 3.0:
        hb.append(tt); st += 0.02; tt += st                  # decelerating toward 38 bpm — then GONE
    heartbeat(bgm, hb, amp=0.20)
    add(bgm, T(30), bell(hz(12, SA * 4), 3.0, 0.04))         # the tilak doorway
    add(bgm, T(32), pad([hz(0, SA * 2), hz(7, SA * 2)], TE(33) - T(32), 0.05, a_t=2.0))  # shimmer grows
    for k in range(3):
        add(bgm, T(32) + 1.2 + k * 1.5, bell(hz([0, 4, 12][k], SA * 4), 2.2, 0.035))
    add(bgm, T(34) - 0.5, pad([hz(0, SA * 2), hz(4, SA * 2), hz(7, SA * 2)],
        TE(34) - T(34) + 2.0, 0.075, a_t=1.8, r_t=2.5, wide=1.6))  # ★ river melts into ocean — warm bloom

def P4(t0, t1, d):  # S35–41 · T4 THE LORD (Mohanakalyani)
    tanpura(bgm, t0, t1, amp=0.04)
    add(bgm, t0, pad([hz(0, SA * 2), hz(7, SA * 2), hz(12, SA * 2)], d, 0.055, a_t=3.0, r_t=3.0, wide=1.8))
    add(bgm, t0, melody(MOHANAKALY, SA * 2, d, R, density=0.4, amp=0.11, kind='pluck'))  # veena arpeggio pad
    motif_A(bgm, T(36) + 0.2, amp=0.18)                      # ★ full resolve AS HE EMERGES
    add(bgm, T(37), pad([hz(4, SA * 2), hz(11, SA * 2)], TE(37) - T(37), 0.045, a_t=1.5, wide=2.2))  # face swell (choir-ish)
    motif_Q(bgm, T(38) + 0.4, amp=0.09)                      # anchor #3 — Q asks once more…
    motif_A(bgm, T(38) + 2.6, amp=0.16)                      # …and the Answer carries it
    for k in range(4):                                       # S39 rays — octave bells to all directions
        add(bgm, T(39) + 0.6 + k * 0.9, bell(hz(12 * k, SA * 2), 2.0, 0.05))
    add(bgm, T(40), pad([hz(0), hz(7)], TE(40) - T(40), 0.045, a_t=1.2))    # the tiny light offers itself — hush
    add(bgm, T(41), melody(MOHANAM, SA * 4, TE(41) - T(41), R, density=0.45, amp=0.05, kind='pluck'))  # petal cascade santoor

def P5(t0, t1, d):  # S42–46 · T5 MAYA-VEIL (Bhairavi shimmer)
    add(bgm, t0, melody(BHAIRAVI, SA * 2, d, R, density=0.22, amp=0.07, kind='flute'))
    add(bgm, t0, pad([hz(0), hz(1), hz(7)], d, 0.04, a_t=3.0, r_t=3.0))      # the shimmering minor-second veil
    for k in range(6):                                                         # reversed plucks = her backwards arrival
        add(bgm, T(42) + 1.0 + k * 1.6, rpluck(hz([0, 1, 7, 12, 1, 7][k], SA * 2), 1.1, 0.08, seed=42 + k))
    for k in range(3):                                                         # glass chimes
        add(bgm, T(44) + 0.8 + k * 1.4, bell(hz([12, 17, 19][k], SA * 2), 2.4, 0.035))
    # S43 swallow-then-open: the shimmer dips, then a clear bell passes through
    add(bgm, T(43), pad([hz(1, SA), hz(8, SA)], TE(43) - T(43) * 0.55 - T(43) * 0.45, 0.05, a_t=1.0))
    add(bgm, TE(43) - 1.2, bell(hz(0, SA * 2), 2.6, 0.10))
    add(bgm, T(46), pad([hz(0), hz(4), hz(7)], TE(46) - T(46) + 1.5, 0.06, a_t=1.5, r_t=2.5))  # wraps UP into warmth

def P6(t0, t1, d):  # S47–52 · T6 JIVA-SPARKS (santoor sky)
    add(bgm, t0, pad([hz(0, SA * 2), hz(7, SA * 2)], d, 0.045, a_t=3.0, r_t=3.0))
    add(bgm, t0, melody(HAMSADHWANI, SA * 4, d, R, density=0.35, amp=0.04, kind='pluck'))  # santoor glissandi
    for k in range(8):                                                          # rising sparks — staggered small bells
        add(bgm, T(47) + 0.7 + k * 0.8, bell(hz([0, 2, 4, 7, 9, 11, 12, 16][k], SA * 2), 1.8, 0.05))
    for k in range(4):                                                          # S48 threads tracing
        add(bgm, T(48) + 0.5 + k * 1.2, flute(hz([0, 4, 7, 9][k], SA * 2), 1.0, 0.06, seed=48 + k))
    add(bgm, T(50), pad([hz(0), hz(5)], TE(50) - T(50), 0.05, a_t=1.2))        # lives inside the sparks — tenderness
    motif_A(bgm, T(51) + 1.0, amp=0.10, kind='flute')                          # the threads gather, answered softly
    add(bgm, T(52), pad([hz(0, SA * 2), hz(4, SA * 2), hz(7, SA * 2), hz(12, SA * 2)],
        TE(52) - T(52) + 1.0, 0.07, a_t=1.2, r_t=2.2, wide=2.0))               # ★ lotus constellation bloom

def P7(t0, t1, d):  # S53–58 · T7 BHAKTI RIVER (Desh)
    tanpura(bgm, t0, t1, amp=0.042)
    motif_A(bgm, t0 + 0.3, amp=0.15, kind='flute')            # the foundation made melody
    add(bgm, t0, melody(DESH, SA * 2, d, R, density=0.42, amp=0.115, kind='flute'))
    for k in range(5):                                              # S54 names like bells — grid rhythm
        add(bgm, T(54) + 0.6 + k * 0.9, bell(hz([0, 2, 4, 7, 12][k], SA * 2), 1.8, 0.10))
    add(bgm, T(55), melody(KALYANI, SA * 2, TE(55) - T(55), R, density=0.5, amp=0.13, kind='pluck'))  # ★ S55 real veena solo
    motif_A(bgm, T(55) + 1.2, amp=0.16)
    gait(bgm, T(56), TE(56), step=0.9, amp=0.12, double=True)       # joy quickens
    motif_A(bgm, T(56) + 0.4, amp=0.15)
    # S57 THE WHOLE MANDALA — all voices stacked, then taper:
    add(bgm, T(57), pad([hz(0, SA * 2), hz(4, SA * 2), hz(7, SA * 2), hz(12, SA * 2)],
        TE(57) - T(57), 0.08, a_t=1.2, r_t=2.6, wide=2.0))
    motif_A(bgm, T(57) + 0.5, amp=0.17)
    for k in range(3):
        add(bgm, T(57) + 2.0 + k * 1.6, bell(hz([0, 7, 12][k], SA * 4), 2.4, 0.05))
    add(bgm, T(58) + 1.0, pluck(hz(12, SA), 3.2, 0.10, bright=1.7, seed=58))   # everything condenses into ink

def P8(t0, t1, d):  # S59–68 · T8 HOME / COMPOSITION (Mohanam)
    tanpura(bgm, t0, T(67), amp=0.042)
    add(bgm, t0, pad([hz(0), hz(7)], T(63) - t0, 0.05, a_t=2.0))
    add(bgm, t0, melody(MOHANAM, SA * 2, T(64) - t0, R, density=0.35, amp=0.09, kind='flute'))
    motif_A(bgm, T(60) + 0.3, amp=0.16)                          # ★ eyes open — full cadence
    add(bgm, T(63) + 0.8, pluck(hz(9, SA * 2), 0.9, 0.10, bright=1.6, seed=63))     # humor #2, soft two-note
    add(bgm, T(63) + 1.7, pluck(hz(12, SA * 2), 0.9, 0.10, bright=1.6, seed=64))
    gait(bgm, T(64), TE(64), step=1.15, amp=0.10)                # the walk back with purpose
    tt = T(66) + 0.5                                             # S66 stylus ticks between the strokes
    while tt < TE(66) - 0.5:
        add(bgm, tt, tick(0.09, 0.05, seed=int(tt * 7))); tt += 1.15
    motif_A(bgm, T(67) + 0.4, amp=0.15)                          # veena cadenza prepares…
    add(bgm, TE(67) - 1.0, bell(hz(0, SA * 2), 2.4, 0.12))       # …temple bell pair
    add(bgm, TE(67) + 0.8, bell(hz(7, SA * 2), 2.4, 0.10))
    # S68 END CARD — heartbeat + two open notes under the definitive text:
    heartbeat(bgm, [T(68) + 0.6], amp=0.24)
    add(bgm, T(68) + 2.0, flute(hz(0, SA * 2), 1.6, 0.10, seed=681, warm=True))
    add(bgm, T(68) + 3.8, flute(hz(2, SA * 2), 2.6, 0.10, seed=682, warm=True))
    add(bgm, T(68), pad([hz(0, SA * 2)], TE(68) - T(68) + 1.0, 0.045, a_t=1.0))

for n0, n1, fn in [(1, 6, P0), (7, 18, P1), (19, 26, P2), (27, 34, P3),
                   (35, 41, P4), (42, 46, P5), (47, 52, P6), (53, 58, P7), (59, 68, P8)]:
    segment(n0, n1, fn)

f = int(2.0 * SR); bgm[:f] *= np.linspace(0, 1, f); bgm[-f:] *= np.linspace(1, 0, f)
bgm *= 0.9 / max(1e-6, np.abs(bgm).max())

def decode(fpath):
    out = subprocess.run([FF, '-v', 'error', '-i', fpath, '-f', 'f32le', '-ac', '1',
                          '-ar', str(SR), '-'], capture_output=True, check=True)
    return np.frombuffer(out.stdout, dtype=np.float32)

voice = decode(f"{ROOT}/EP03_CLEAN_VOICE.mp3")
L = min(len(voice), len(bgm)); voice = voice[:L]; bed = bgm[:L]
env = np.abs(voice)
w = int(0.09 * SR); env = np.convolve(env, np.ones(w) / w, 'same')
mask = np.clip(env / 0.06, 0, 1)
DUCK = 0.72
gain = 1.0 - DUCK * mask
bed = bed * (gain * 0.45)
mix = voice + bed
peak = np.abs(mix).max()
if peak > 0.89: mix *= 0.89 / peak

def write_mp3(sig, out, q='2', norm=True):
    wav = "/tmp/_bgmx3.wav"
    subprocess.run([FF, '-y', '-v', 'error', '-f', 'f32le', '-ac', '1', '-ar', str(SR),
                    '-i', '-', '-c:a', 'pcm_s16le', wav], input=sig.tobytes(), check=True)
    args = [FF, '-y', '-v', 'error', '-i', wav]
    if norm: args += ['-af', 'loudnorm=I=-16:TP=-1.5:LRA=11']
    args += ['-c:a', 'libmp3lame', '-q:a', q, out]
    subprocess.run(args, check=True)

write_mp3(mix, f"{ROOT}/EP03_WITH_BGM.mp3")
write_mp3(bgm[:L], f"{ROOT}/EP03_BGM_STEM.mp3", q='3', norm=False)
rms = np.sqrt(np.mean(mix ** 2)); print(f"OK EP03_WITH_BGM.mp3 {L/SR/60:.1f} min | mix RMS {20*np.log10(max(rms,1e-9)):.1f} dBFS | stem saved")
