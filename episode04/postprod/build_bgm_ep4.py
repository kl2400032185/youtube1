#!/usr/bin/env python3
"""Emits episode04/postprod/make_bgm_ep4.py = EP3 engine primitives + EP4's 10-cue map
(+ NEW ambient primitives: river bed + dawn birds)."""
src = open('episode03/postprod/make_bgm_ep3.py').read()
head = src[:src.index('def P0')]
tail = src[src.index('\nf = int(2.0 * SR)'):]

for a, b in [('scene_map_ep3', 'scene_map_ep4'),
             ('EP03_CLEAN_VOICE', 'EP04_CLEAN_VOICE'),
             ('EP03_WITH_BGM', 'EP04_WITH_BGM'),
             ('EP03_BGM_STEM', 'EP04_BGM_STEM'),
             ('8-theme', '10-cue')]:
    head = head.replace(a, b)

MID = r'''
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
'''

out = head + MID + tail
open('episode04/postprod/make_bgm_ep4.py', 'w').write(out)
print('make_bgm_ep4.py emitted:', len(out), 'chars')
