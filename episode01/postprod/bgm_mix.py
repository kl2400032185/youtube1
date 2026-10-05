#!/usr/bin/env python3
"""
EPISODE 1 — BGM post-production mixer
Synthesizes the 5 themes from the plan's BGM Master Plan (raga-faithful scales),
mixes them under the recorded Telugu narration with ducking, honours the motif
rule (Q falls / A rises, fused ONLY in Scene 64), and renders:
  - full 13:58 master  -> episode01/EP01_MASTER_13m58s.mp3
  - per-scene clips    -> episode01/audio_bgm/EP01_Snn.mp3
Run:  /tmp/bgmlab/bin/python bgm_mix.py
"""
import os, subprocess, numpy as np
import imageio_ffmpeg

FF   = imageio_ffmpeg.get_ffmpeg_exe()
SR   = 22050
ROOT = "/home/user/youtube1/episode01"
WORK = "/tmp/bgmwork"; os.makedirs(WORK, exist_ok=True)
OUT_SCENES = os.path.join(ROOT, "audio_final"); os.makedirs(OUT_SCENES, exist_ok=True)

# ---- scenes: (n, start_s, end_s, kind, intensity/10) -------------------------
# kind: T1 Ancient World | T2 Vyasa Greatness | T3 Inner Restlessness
#       T4 Ashrama Life  | T5 Narada Arrival  | specials
SCENES = [
 ( 1,  0, 10,'T1',1),( 2, 10, 20,'T1',2),( 3, 20, 30,'T1',2),( 4, 30, 41,'T1',2),
 ( 5, 41, 53,'T1',3),( 6, 53, 66,'T1',3),
 ( 7, 66, 78,'T2',3),( 8, 78, 90,'T2',3),( 9, 90,103,'T2',4),(10,103,116,'T2',5),
 (11,116,128,'T4',2),(12,128,140,'T2',3),(13,140,153,'T2',3),(14,153,167,'T2_STOP',6),
 (15,167,180,'T3',3),(16,180,192,'T3',3),(17,192,205,'T3',2),(18,205,218,'T3_HB',3),
 (19,218,231,'T3_WARM',2),(20,231,245,'T3_Q',4),(21,245,260,'T3_THIN',2),
 (22,260,272,'T4',3),(23,272,284,'T4_STING',2),(24,284,296,'T4_STING',3),
 (25,296,309,'T4_RIT',3),(26,309,322,'T4',3),(27,322,335,'T4_WORK',2),
 (28,335,348,'T4_BARE',2),(29,348,362,'T14_BLEND',3.5),
 (30,362,375,'T3_QFRAG',3),(31,375,390,'T3_HB',3.5),(32,390,403,'T3',3),
 (33,403,416,'T3_Q',4),(34,416,429,'T3_BARE',2),(35,429,442,'T3_GHOST2',3),
 (36,442,457,'NEAR_NOTHING',1),(37,457,472,'T3_Q_STR',4),
 (38,472,485,'PLAYFUL',3),(39,485,498,'STING_TO_T3',2.5),(40,498,511,'PLAYFUL',3),
 (41,511,525,'T3_RISE',3.5),(42,525,538,'T3_DEEP',2),(43,538,551,'T4_BARE',2),
 (44,551,564,'T3_VOID',3),(45,564,577,'T3_TO_T4',2.5),(46,577,590,'T3_WARM',2.5),
 (47,590,603,'T2_MEM',3),
 (48,603,616,'S48_STOP_Q',2),(49,616,629,'ONE_NOTE',1),(50,629,643,'SUSPENSE',3.5),
 (51,643,655,'SUSPENSE_UP',4),(52,655,667,'SUSPENSE_BELL',5),
 (53,667,679,'T5_CELL',4),(54,679,691,'T5',5.5),(55,691,703,'T5_WALK',6),
 (56,703,715,'QA_ALT',6),(57,715,727,'T5',6),(58,727,739,'T5_CREST',7),
 (59,739,751,'T5_CREST',7),(60,751,763,'T5_FRIEND',6),(61,763,775,'QA_ALT',6),
 (62,775,787,'HELD_CHORD',3),(63,787,797,'SEMI_RESOLVE',2.5),
 (64,797,810,'UNION',7),(65,810,823,'HANG',2),(66,823,838,'ENDCARD',2),
]

# ---- raga scales (semitones from Sa) ----------------------------------------
MOHANAM      = [0,2,4,7,9]           # T1
KALYANI      = [0,2,4,6,7,9,11]      # T2
SHIVARANJANI = [0,2,3,7,8]           # T3  (question colour)
HAMSADHWANI  = [0,2,4,7,11]          # T4
MOHANAKALY   = [0,2,4,7,9,11]        # T5

SA   = 130.81   # C3 tonic
def hz(off, base=SA): return base*2.0**(off/12.0)

# ---- primitive synthesizers --------------------------------------------------
def N(dur): return max(1, int(round(dur*SR)))

def add(buf, t0, sig, gain=1.0):
    i = int(round(t0*SR))
    if i >= len(buf): return
    j = min(len(buf), i+len(sig))
    if j > i: buf[i:j] += gain*sig[:j-i]

def pluck(freq, dur, amp=0.30, bright=0.7, seed=0):
    """veena / tanpura / dotara — additive inharmonic string with pick noise"""
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n)/SR; y = np.zeros(n)
    for k in range(1, 7):
        fk = freq*k*(1.0+0.00035*k*k)
        y += (1.0/k**1.12)*np.sin(2*np.pi*fk*t + 0.35*np.sin(2*np.pi*fk*t*0.502)) \
             * np.exp(-t*(0.8+0.85*k)/(max(dur,0.3)*bright))
    y *= amp
    m = int(0.004*SR); y[:m] *= np.linspace(0,1,m)
    y[:m] += rng.standard_normal(m)*np.exp(-np.arange(m)/(0.0016*SR))*amp*0.35
    return y.astype(np.float32)

def flute(freq, dur, amp=0.22, seed=0, warm=False):
    """bansuri — vibrato sine + breath, soft slur in/out"""
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n)/SR
    vib = 1.0 + 0.0042*np.sin(2*np.pi*(4.9 if not warm else 4.4)*t + rng.uniform(0,6.28))
    f = np.full(n, freq); m = int(0.11*SR)
    if m > 0: f[:m] = freq*2.0**(np.linspace(-0.45,0,m)/12.0)
    ph = 2*np.pi*np.cumsum(f*vib)/SR
    y = np.sin(ph)*amp
    breath = np.convolve(rng.standard_normal(n), np.ones(48)/48.0, 'same')*amp*0.05
    y += breath
    a = min(int(0.09*SR), max(1, n//4)); r = min(int(0.28*SR), max(1, n-a))
    e = np.ones(n); e[:a] = np.linspace(0,1,a); e[-r:] *= np.linspace(1,0,r)
    e *= (1.0+0.14*np.sin(np.pi*np.minimum(t/max(dur,0.01),1.0)))
    return (y*e).astype(np.float32)

def pad(freqs, dur, amp=0.10, seed=0, a_t=1.8, r_t=2.2):
    """string pad — detuned saw-ish partials, dark lowpass, slow envelope"""
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n)/SR; y = np.zeros(n)
    for f in freqs:
        for det in (-5.0, 6.0):
            fm = f*2.0**(det/1200.0); ph = 2*np.pi*fm*t
            for k in range(1, 5):
                y += np.sin(k*ph + rng.uniform(0,6.28))/(k*1.6)
    y = np.convolve(y, np.ones(9)/9.0, 'same')
    y *= amp/max(1.0, np.abs(y).max())
    a = min(n//2, int(a_t*SR)); r = min(n//2, int(r_t*SR))
    e = np.ones(n); e[:a] = np.linspace(0,1,a)**1.5; e[-r:] *= np.linspace(1,0,r)**1.3
    return (y*e).astype(np.float32)

def thump(amp=0.5, dur=0.3, seed=0):
    """mridangam heartbeat / gait stroke"""
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n)/SR
    f = 95.0 + 75.0*np.exp(-t/0.02)
    y = np.sin(2*np.pi*np.cumsum(f)/SR)*np.exp(-t/0.075)*amp
    c = int(0.007*SR)
    y[:c] += rng.standard_normal(c)*np.exp(-np.arange(c)/18.0)*amp*0.5
    return y.astype(np.float32)

def tick(amp=0.12, dur=0.05, seed=0):
    rng = np.random.default_rng(seed)
    n = N(dur); nz = rng.standard_normal(n)
    hp = np.concatenate([[0], np.diff(nz)])
    return (hp*np.exp(-np.arange(n)/(0.008*SR))*amp).astype(np.float32)

def bell(freq, dur=2.2, amp=0.13, seed=0):
    """temple chime — inharmonic partials"""
    n = N(dur); t = np.arange(n)/SR; y = np.zeros(n)
    for p, a, tau in [(1.0,1.0,2.6),(2.44,0.5,1.8),(4.10,0.28,1.2),(5.43,0.16,0.8)]:
        y += a*np.sin(2*np.pi*freq*p*t)*np.exp(-t/tau)
    y *= amp
    m = int(0.003*SR); y[:m] *= np.linspace(0,1,m)
    return y.astype(np.float32)

def tanpura(buf, t_from, t_to, amp=0.045, base=SA):
    """tanpura drone cycle  Pa  Sa  Sa  SA(low)"""
    pat = [7, 12, 12, -12]; step = 1.15
    t = t_from
    while t < t_to - 1.0:
        for i, off in enumerate(pat):
            add(buf, t + i*step, pluck(hz(off, base), 1.8,
                amp*(1.15 if off == -12 else 1.0), bright=1.4, seed=int(t*10+i)))
        t += step*4

def melody(scale, base, dur, rng, density=0.5, amp=0.2, kind='flute', reg=0,
           tmin=0.9, tmargin=1.4):
    """random-walk raga phrases with rests"""
    notes = []
    t = tmin + rng.uniform(0, 1.6)
    deg = 0 if rng.random() < 0.5 else int(rng.integers(0, len(scale)))
    while t < dur - tmargin:
        nd = float(rng.choice([0.7, 0.9, 1.1, 1.4, 1.8]))*(0.72 if density > 0.6 else 1.05)
        deg = int(np.clip(deg + int(rng.integers(-2, 3)), 0, len(scale)+2))
        o, idx = divmod(deg, len(scale))
        off = scale[idx] + 12*(o+reg)
        notes.append((t, nd, off))
        t += nd + float(rng.choice([0.05, 0.15, 0.3, 0.55]))*(1.8-1.2*density)
    out = np.zeros(N(dur), dtype=np.float32)
    for t0, nd, off in notes:
        f = hz(off, base)
        sig = flute(f, nd*1.12, amp, seed=int(t0*97)) if kind == 'flute' \
              else pluck(f, nd*2.0, amp, seed=int(t0*97))
        add(out, t0, sig)
    return out

# ============================ SFX LAYER (item E) =============================
def _lp(x, k):
    k = max(3, int(k) | 1)
    return np.convolve(x, np.hanning(k)/np.hanning(k).sum(), 'same')

def _hp(x):
    return np.concatenate([[0.0], np.diff(x)])

def fwind(dur, amp=0.05, gust=0.35, seed=0):
    """wind bed — brown noise shaped by slow random gusts"""
    rng = np.random.default_rng(seed)
    n = N(dur)
    br = np.cumsum(rng.standard_normal(n)); br /= max(1e-9, np.abs(br).max())
    br = _hp(br)
    g = _lp(rng.standard_normal(n), SR//2)
    g = 0.65 + gust*(g/max(1e-9, np.abs(g).max()))
    hiss = _hp(rng.standard_normal(n))*0.35*g
    return ((br*g*0.9 + hiss)*amp).astype(np.float32)

def friver(dur, amp=0.05, seed=0):
    """river — mid-band rushing water, no pitch"""
    rng = np.random.default_rng(seed)
    n = N(dur); x = rng.standard_normal(n)
    mid = _lp(x, 31) - _lp(x, 501)
    g = 1.0 + 0.18*np.sin(2*np.pi*0.37*np.arange(n)/SR + seed)
    return (mid*g*amp/max(1e-9, np.abs(mid).max())*0.9).astype(np.float32)

def fcrickets(dur, amp=0.02, seed=0):
    rng = np.random.default_rng(seed)
    n = N(dur); t = np.arange(n)/SR
    train = (np.sin(2*np.pi*4230*t)*(0.5+0.5*np.sign(np.sin(2*np.pi*14*t)))) * \
            (0.6+0.4*np.sin(2*np.pi*0.9*t+1))
    train = _lp(train, 9)
    return (train*amp/(1e-9+np.abs(train).max())*0.8).astype(np.float32)

def ffire(dur, amp=0.045, seed=0, density=3.0):
    """fire — low rumble + random crackle pops"""
    rng = np.random.default_rng(seed)
    n = N(dur)
    br = np.cumsum(rng.standard_normal(n)); br = _hp(br); br /= max(1e-9, np.abs(br).max())
    y = br*0.5
    pops = int(dur*density)
    for _ in range(pops):
        p = int(rng.integers(0, max(1, n-800)))
        L = int(rng.integers(120, 700))
        y[p:p+L] += rng.standard_normal(min(L, len(y)-p))*np.exp(-np.arange(min(L, len(y)-p))/60.0)*rng.uniform(0.3, 1.0)
    return (y*amp/(1e-9+np.abs(y).max())).astype(np.float32)

def _gliss(f0, f1, d, amp, seed=0, vib=0.0, rough=0.0):
    rng = np.random.default_rng(seed)
    n = N(d); t = np.arange(n)/SR
    f = np.linspace(f0, f1, n)
    if vib: f = f*(1+vib*np.sin(2*np.pi*9*t))
    ph = 2*np.pi*np.cumsum(f)/SR
    y = np.sin(ph)
    if rough: y += rough*np.sign(np.sin(ph))
    e = np.ones(n); a = min(int(0.02*SR), max(2, n//4)); r = min(int(0.09*SR), max(2, n-a))
    e[:a] = np.linspace(0, 1, a); e[-r:] *= np.linspace(1, 0, r)
    return (y*e*amp).astype(np.float32)

def koel(dur, amp=0.05, times=(2.0,), seed=0):
    out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        add(out, t0,       _gliss(880, 1180, 0.30, amp, seed+i))
        add(out, t0+0.34,  _gliss(1180, 950, 0.42, amp*1.1, seed+i+9))
    return out

def mynah(dur, amp=0.04, times=(1.0,), seed=0):
    out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        for k in range(3):
            add(out, t0+k*0.16, _gliss(1900, 1250, 0.10, amp*rng01(seed+i+k), seed+i*7+k))
    return out

def rng01(s):
    return float(np.random.default_rng(int(s*7919) % 2**31).uniform(0.75, 1.05))

def peacock_call(dur, amp=0.045, t0=2.0, seed=0):
    out = np.zeros(N(dur), dtype=np.float32)
    add(out, t0, _gliss(1900, 950, 0.75, amp, seed, vib=0.02))
    add(out, t0+0.95, _gliss(1750, 900, 0.65, amp*0.85, seed+3, vib=0.02))
    return out

def crow(dur, amp=0.07, times=(2.0,), seed=0):
    out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        add(out, t0, _gliss(760, 430, 0.16, amp, seed+i, rough=0.9))
    return out

def owl(dur, amp=0.04, times=(2.0,), seed=0):
    out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        add(out, t0, _gliss(338, 330, 0.55, amp, seed+i))
        add(out, t0+0.75, _gliss(335, 322, 0.85, amp, seed+i+4))
    return out

def nightjar(dur, amp=0.03, t0=3.0, seed=0):
    n = N(min(1.6, dur-t0)); t = np.arange(n)/SR
    y = np.sin(2*np.pi*1750*t)*(np.sign(np.sin(2*np.pi*31*t))*0.5+0.5)
    out = np.zeros(N(dur), dtype=np.float32); add(out, t0, (y*amp).astype(np.float32))
    return out

def cuckoo(dur, amp=0.04, times=(3.0,), seed=0):
    out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        add(out, t0, _gliss(660, 650, 0.28, amp, seed+i))
        add(out, t0+0.38, _gliss(540, 525, 0.34, amp, seed+i+2))
    return out

def bee(dur, amp=0.05, t0=1.6, seed=0):
    rng = np.random.default_rng(seed); nn = N(min(2.6, dur-t0))
    t = np.arange(nn)/SR
    y = np.sign(np.sin(2*np.pi*196*t)) + 0.6*np.sin(2*np.pi*196*t)
    y = _lp(y, 61)
    wob = 0.55 + 0.45*np.sin(2*np.pi*23*t)
    drift = 0.5 + 0.5*np.sin(2*np.pi*0.7*t+1.2)
    out = np.zeros(N(dur), dtype=np.float32)
    add(out, t0, (y*wob*drift*amp*0.25).astype(np.float32))
    return out

def wingburst(dur, amp=0.13, t0=0.6, seed=0):
    rng = np.random.default_rng(seed); out = np.zeros(N(dur), dtype=np.float32)
    t = t0
    for i in range(9):
        L = int(0.12*SR); p = int(t*SR)
        fl = rng.standard_normal(L)*np.exp(-np.arange(L)/(0.028*SR))
        fl = _lp(fl, 121)
        add(out, t, (fl*amp).astype(np.float32))
        t += 0.23 - i*0.012
    return out

def drop_ripple(dur, amp=0.10, t0=2.0, seed=0):
    out = np.zeros(N(dur), dtype=np.float32)
    add(out, t0, _gliss(920, 430, 0.09, amp, seed))
    add(out, t0+0.42, _gliss(830, 460, 0.06, amp*0.35, seed+1))
    rng = np.random.default_rng(seed)
    for k in range(4):
        add(out, t0+0.75+0.4*k, _gliss(1200+200*k, 1150, 0.05, amp*0.12, seed+10+k))
    return out

def leaves(dur, amp=0.03, seed=0):
    rng = np.random.default_rng(seed); n = N(dur)
    x = _hp(rng.standard_normal(n))
    g = _lp(rng.standard_normal(n), int(0.4*SR))
    g = 0.5+0.5*(g/max(1e-9, np.abs(g).max()))
    return (x*g*amp).astype(np.float32)

def steps(dur, amp=0.09, times=(0.5, 1.2, 1.9), seed=0, stone=False):
    rng = np.random.default_rng(seed); out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        th = thump(amp=amp*(0.8 if not stone else 0.55), dur=0.16, seed=seed+i)
        tk = tick(amp=amp*(0.35 if stone else 0.15), dur=0.05, seed=seed+i+50)
        out2 = np.zeros(len(th), dtype=np.float32)
        out2[:len(th)] += th; out2[:len(tk)] += tk
        add(out, t0, out2)
    return out

def swish(dur, amp=0.06, t0=1.0, seed=0, dd=0.35):
    rng = np.random.default_rng(seed); out = np.zeros(N(dur), dtype=np.float32)
    n = N(dd); x = _lp(rng.standard_normal(n), 25)
    e = np.sin(np.pi*np.arange(n)/n)**1.5
    add(out, t0, (x*e*amp).astype(np.float32))
    return out

def stylus(dur, amp=0.05, times=(1.0, 3.2, 5.5), seed=0):
    rng = np.random.default_rng(seed); out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        n = N(0.5); x = _hp(rng.standard_normal(n))
        e = np.sin(np.pi*np.arange(n)/n)**2
        add(out, t0, (x*e*amp).astype(np.float32))
    return out

def woodknock(dur, amp=0.10, times=(1.0,), seed=0):
    out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        add(out, t0, pluck(196+((seed+i) % 3)*24, 0.22, amp, bright=0.35, seed=seed+i))
    return out

def chantbed(dur, amp=0.05, seed=0):
    n = N(dur); t = np.arange(n)/SR
    y = np.zeros(n)
    for k, a in [(1, 1.0), (2, 0.35), (3, 0.14)]:
        y += a*np.sin(2*np.pi*(130.81*0.75)*k*t + 0.1*np.sin(2*np.pi*0.5*t))
    breath = _lp(np.random.default_rng(seed).standard_normal(n), 301)*0.25
    e = np.ones(n); a = int(1.2*SR); e[:a] = np.linspace(0, 1, a); e[-a:] *= np.linspace(1, 0, a)
    return ((y+breath)*e*amp).astype(np.float32)

def whoosh(dur, amp=0.07, t0=1.0, dd=1.8, seed=0):
    rng = np.random.default_rng(seed); out = np.zeros(N(dur), dtype=np.float32)
    n = N(dd); x = rng.standard_normal(n)
    sweep = np.linspace(3, 401, n); x = x - _lp(x, sweep.astype(int).clip(3).tolist()) if False else x  # keep simple
    base = _hp(x)*0.5 + _lp(x, 501)*0.5
    e = np.sin(np.pi*np.arange(n)/n)**1.3
    add(out, t0, (base*e*amp).astype(np.float32))
    return out

def breathpuff(dur, amp=0.05, t0=2.0, seed=0):
    rng = np.random.default_rng(seed); out = np.zeros(N(dur), dtype=np.float32)
    n = N(0.55); x = _hp(rng.standard_normal(n)); e = np.sin(np.pi*np.arange(n)/n)
    add(out, t0, (x*e*amp).astype(np.float32))
    return out

def chimespark(dur, amp=0.05, times=(2.0,), seed=0, base_f=2500):
    out = np.zeros(N(dur), dtype=np.float32)
    for i, t0 in enumerate(times):
        add(out, t0, bell(base_f*(1+0.11*(i % 3)), 1.3, amp, seed+i))
    return out

def rumble(dur, amp=0.06, seed=0):
    n = N(dur); t = np.arange(n)/SR
    y = np.sin(2*np.pi*42*t)*(0.7+0.3*np.sin(2*np.pi*0.4*t))
    return (y*amp).astype(np.float32)

def sfx_scene(n, dur, seed0=7):
    """per-scene SFX recipe (plan item E)"""
    rng = np.random.default_rng(4000+n)
    buf = np.zeros(N(dur), dtype=np.float32)
    s = lambda x, g=1.0: buf.__iadd__((x*g).astype(np.float32))

    if n == 1: s(fwind(dur, 0.055, 0.5, seed0+1)); buf = np.add(buf, koel(dur, 0.02, (6.0,), 2))
    elif n == 2: s(fwind(dur, 0.06, 0.55, seed0+2)); add(buf, 5.0, _gliss(2300, 1500, 1.1, 0.035, 3))
    elif n == 3: s(leaves(dur, 0.035, 4)); add(buf, 0, koel(dur, 0.045, (1.5, 6.5), 5)); add(buf, 0, mynah(dur, 0.03, (3.5, 8.5), 6))
    elif n == 4: s(friver(dur, 0.05, 7)); add(buf, 0, peacock_call(dur, 0.03, 5.0, 8))
    elif n == 5: s(fwind(dur, 0.03, 0.3, 9)); add(buf, 0, peacock_call(dur, 0.025, 7.5, 10)); add(buf, 2.0, bell(640, 0.7, 0.015, 11)); add(buf, 6.0, bell(660, 0.7, 0.013, 12))
    elif n == 6: s(fwind(dur, 0.035, 0.4, 13)); s(leaves(dur, 0.025, 14)); add(buf, 3.0, bell(1320, 1.6, 0.03, 15))
    elif n == 7: s(steps(dur, 0.07, tuple(0.8+i*0.75 for i in range(6)), 16)); add(buf, 0, swish(dur, 0.04, 2.2, 17))
    elif n == 8: s(leaves(dur, 0.02, 18)); add(buf, 0, swish(dur, 0.03, 4.0, 19)); add(buf, 0, kotick(dur) if False else swish(dur, 0.025, 8.0, 20))
    elif n == 9: s(stylus(dur, 0.045, (1.2, 4.0, 7.0, 10.0), 21)); s(ffire(dur, 0.02, 22, 1.5))
    elif n == 10: add(buf, 0, whoosh(dur, 0.05, 3.0, 2.2, 23)); add(buf, 0, rumble(dur, 0.03, 24))
    elif n == 11: s(friver(dur, 0.04, 25)); add(buf, 0, owl(dur, 0.03, (4.0,), 26)); s(ffire(dur, 0.015, 27, 1.0))
    elif n == 12: add(buf, 0, chantbed(dur, 0.05, 28)); add(buf, 0, tickbed(dur) if False else chimespark(dur, 0.008, tuple(1.0+i*0.7 for i in range(14)), 29, 3200))
    elif n == 13: add(buf, 0, woodknock(dur, 0.05, (1.5, 4.5, 8.0), 30)); s(steps(dur, 0.05, (2.0, 3.2, 5.6, 7.4), 31)); add(buf, 0.6, bell(880, 1.4, 0.03, 32))
    elif n == 14: s(ffire(dur, 0.035, 33, 2.0)); s(_lp(np.random.default_rng(34).standard_normal(N(dur)), 901)*0.012); add(buf, 4.0, breathpuff(dur, 0.02, 4.0, 35))
    elif n == 15: s(fwind(dur, 0.04, 0.35, 36)); s(ffire(dur, 0.012, 37, 0.8))
    elif n == 16: s(fwind(dur, 0.028, 0.3, 38)); add(buf, 2.0, bell(2000, 2.0, 0.015, 39))
    elif n == 17: s(ffire(dur, 0.03, 40, 1.2)); add(buf, 0, fcrickets(dur, 0.014, 41))
    elif n == 18: s(ffire(dur, 0.04, 42, 2.5)); add(buf, 0, breathpuff(dur, 0.03, 6.0, 43))
    elif n == 19: s(friver(dur, 0.055, 44)); add(buf, 0, nightjar(dur, 0.022, 4.0, 45)); s(leaves(dur, 0.015, 46))
    elif n == 20: s(friver(dur, 0.045, 47)); add(buf, 0, drop_ripple(dur, 0.10, 8.6, 48))
    elif n == 21: s(friver(dur, 0.035, 49)); s(fwind(dur, 0.025, 0.3, 50))
    elif n == 22: s(leaves(dur, 0.028, 51)); add(buf, 0, koel(dur, 0.04, (2.0, 8.0), 52)); s(steps(dur, 0.04, (3.0, 4.0, 7.0), 53))
    elif n == 23: s(friver(dur, 0.03, 54)); add(buf, 3.2, swish(dur, 0.05, 3.2, 55, 0.5)); add(buf, 3.9, bell(520, 0.5, 0.03, 56))
    elif n == 24: add(buf, 0, bee(dur, 0.05, 2.0, 57)); add(buf, 8.0, swish(dur, 0.04, 8.0, 58))
    elif n == 25: add(buf, 2.0, whoosh(dur, 0.06, 2.0, 1.2, 59)); s(ffire(dur, 0.035, 60, 2.2)); add(buf, 10.0, bell(1560, 1.2, 0.03, 61))
    elif n == 26: add(buf, 0, peacock_call(dur, 0.035, 2.5, 62)); add(buf, 6.0, bell(640, 0.6, 0.018, 63)); add(buf, 9.5, bell(655, 0.6, 0.015, 64))
    elif n == 27: add(buf, 0, swish(dur, 0.035, 1.5, 65, 0.6)); add(buf, 0, swish(dur, 0.03, 5.5, 66, 0.6)); s(friver(dur, 0.02, 67))
    elif n == 28: s(leaves(dur, 0.03, 68)); add(buf, 7.0, swish(dur, 0.04, 7.0, 69))
    elif n == 29: s(ffire(dur, 0.02, 70, 1.5)); add(buf, 1.5, bell(1180, 1.8, 0.03, 71)); add(buf, 5.0, bell(1320, 1.8, 0.03, 72)); add(buf, 9.5, bell(1100, 2.2, 0.028, 73))
    elif n == 30: add(buf, 0, fcrickets(dur, 0.018, 74)); add(buf, 2.5, bell(2600, 1.0, 0.012, 75)); add(buf, 7.0, bell(2450, 1.0, 0.010, 76))
    elif n == 31: s(ffire(dur, 0.028, 77, 1.4)); add(buf, 0, fcrickets(dur, 0.010, 78))
    elif n == 32: s(fwind(dur, 0.018, 0.25, 79)); add(buf, 5.5, drop_ripple(dur, 0.06, 5.5, 80)); add(buf, 3.0, swish(dur, 0.02, 3.0, 81, 0.3))
    elif n == 33: s(friver(dur, 0.06, 82))
    elif n == 34: s(friver(dur, 0.04, 83)); add(buf, 0, breathpuff(dur, 0.035, 9.0, 84))
    elif n == 35: s(_lp(np.random.default_rng(85).standard_normal(N(dur)), 601)*0.02); add(buf, 4.5, whoosh(dur, 0.045, 4.5, 2.4, 86))
    elif n == 36: s(friver(dur, 0.045, 87)); add(buf, 0, breathpuff(dur, 0.03, 4.0, 88)); add(buf, 0, breathpuff(dur, 0.025, 10.5, 89))
    elif n == 37: s(fwind(dur, 0.05, 0.5, 90)); add(buf, 0, crow(dur, 0.05, (3.0, 3.5), 91))
    elif n == 38: add(buf, 1.8, swish(dur, 0.05, 1.8, 92, 0.15)); add(buf, 2.2, swish(dur, 0.04, 2.2, 93, 0.12)); add(buf, 5.0, swish(dur, 0.045, 5.0, 94, 0.2))
    elif n == 39: s(fwind(dur, 0.02, 0.25, 95)); add(buf, 6.0, swish(dur, 0.03, 6.0, 96))
    elif n == 40: add(buf, 0, _gliss(520, 430, 0.09, 0.03, 97, rough=0.4)); add(buf, 2.0, _gliss(540, 420, 0.08, 0.028, 98, rough=0.4)); add(buf, 9.0, breathpuff(dur, 0.04, 9.0, 99))
    elif n == 41: s(fwind(dur, 0.04, 0.55, 100)); s(steps(dur, 0.05, tuple(1.0+i*0.9 for i in range(4)), 101))
    elif n == 42: s(leaves(dur, 0.04, 102)); s(steps(dur, 0.045, (1.4, 3.0, 4.8, 6.6), 103))
    elif n == 43: s(leaves(dur, 0.02, 104)); add(buf, 0, cuckoo(dur, 0.032, (4.0,), 105))
    elif n == 44: s(rumble(dur, 0.045, 106)); add(buf, 3.0, drop_ripple(dur, 0.05, 3.0, 107)); add(buf, 8.5, drop_ripple(dur, 0.04, 8.5, 108))
    elif n == 45: s(friver(dur, 0.05, 109)); add(buf, 0, woodknock(dur, 0.04, (6.0, 10.0), 110))
    elif n == 46: add(buf, 2.0, swish(dur, 0.035, 2.0, 111, 0.5)); s(leaves(dur, 0.02, 112))
    elif n == 47: s(stylus(dur, 0.04, (1.5, 5.5, 9.5), 113)); s(fwind(dur, 0.02, 0.4, 114))
    elif n == 48: s(fwind(dur, 0.05, 0.5, 115)); add(buf, 1.2, whoosh(dur, 0.05, 1.2, 1.4, 116)); add(buf, 11.0, swish(dur, 0.02, 11.0, 117, 0.3))
    elif n == 49: s(fwind(dur, 0.035, 0.35, 118)); add(buf, 5.0, pluck(70, 0.9, 0.03, 0.3, 119))
    elif n == 50: s(fwind(dur, 0.055, 0.6, 120)); add(buf, 3.5, bell(2400, 1.0, 0.012, 121)); add(buf, 8.0, bell(2550, 0.9, 0.010, 122))
    elif n == 51: add(buf, 0, wingburst(dur, 0.13, 1.0, 123)); add(buf, 0, mynah(dur, 0.045, (2.6, 3.4, 5.0), 124))
    elif n == 52: s(leaves(dur, 0.03, 125)); add(buf, 1.5, bell(760, 2.6, 0.06, 126)); add(buf, 6.0, bell(760, 2.2, 0.04, 127))
    elif n == 53: s(fwind(dur, 0.018, 0.2, 128))
    elif n == 54: s(fwind(dur, 0.03, 0.3, 129)); s(steps(dur, 0.04, (2.0, 3.1, 4.2), 130))
    elif n == 55: add(buf, 1.0, bell(950, 1.6, 0.025, 131)); add(buf, 4.5, bell(1010, 1.4, 0.02, 132)); add(buf, 7.5, swish(dur, 0.03, 7.5, 133))
    elif n == 56: s(steps(dur, 0.06, tuple(1.0+i*1.1 for i in range(5)), 134, stone=True)); add(buf, 10.5, bell(880, 2.2, 0.035, 135))
    elif n == 57: s(steps(dur, 0.05, (2.5, 3.6, 4.7), 136, stone=True)); add(buf, 6.0, bell(2300, 1.2, 0.012, 137))
    elif n == 58: add(buf, 9.8, pluck(523.25, 2.5, 0.09, 1.6, 138)); s(_lp(np.random.default_rng(139).standard_normal(N(dur)), 801)*0.010)
    elif n == 59: add(buf, 0.8, bell(1568, 2.0, 0.045, 140)); add(buf, 0, koel(dur, 0.035, (5.0,), 141)); add(buf, 0, mynah(dur, 0.03, (8.5,), 142))
    elif n == 60: add(buf, 2.0, swish(dur, 0.03, 2.0, 143)); add(buf, 6.5, bell(2800, 0.9, 0.012, 144))
    elif n == 61: s(steps(dur, 0.055, tuple(1.2+i*1.0 for i in range(5)), 145, stone=True)); s(friver(dur, 0.015, 146))
    elif n == 62: add(buf, 4.0, swish(dur, 0.025, 4.0, 147, 0.8)); s(fwind(dur, 0.012, 0.2, 148))
    elif n == 63: add(buf, 0, cuckoo(dur, 0.022, (3.0,), 149)); add(buf, 6.5, bell(1760, 2.0, 0.015, 150))
    elif n == 64: add(buf, 1.2, bell(660, 2.6, 0.03, 151))
    elif n == 65: s(fwind(dur, 0.03, 0.25, 152))
    elif n == 66: add(buf, 2.0, whoosh(dur, 0.05, 2.0, 1.6, 153)); add(buf, 11.5, bell(1320, 1.6, 0.03, 154))
    return buf

def q_motif(dur, base, amp=0.26, ached=True):
    """QUESTION: 3 rising notes that FALL on the 4th — Shivaranjani"""
    offs = [0, 2, 3, -4 if ached else -4]; durs = [0.8, 0.8, 0.8, 1.8]
    out = np.zeros(N(dur), dtype=np.float32); t = 0.0
    for i, (o, d) in enumerate(zip(offs, durs)):
        w = flute if i < 3 else pluck          # last note lands on veena — the ache
        add(out, t, w(hz(o, base), d*1.25, amp*(0.8 if i == 3 else 1.0), seed=i+11))
        t += d
    return out

def a_motif(dur, base, amp=0.30):
    """ANSWER: 4 bright RISING notes — Mohana-Kalyani veena"""
    offs = [0, 4, 7, 11, 12]; durs = [0.55, 0.55, 0.55, 0.7, 1.7]
    out = np.zeros(N(dur), dtype=np.float32); t = 0.0
    for o, d in zip(offs, durs):
        add(out, t, pluck(hz(o, base), d*1.6, amp, bright=1.0, seed=int(o*7+d*13)))
        t += d
    return out

def stinger(buf, dur, rng, playful=True):
    """humour: dotara pluck cluster + bansuri trill"""
    offs = [0, 4, 7, 4, 7, 12] if playful else [0, 3, 7, 3, 7, 12]
    t = 1.1
    for o in offs:
        add(buf, t, pluck(hz(o, SA*2), 0.5, 0.16, bright=1.6, seed=int(t*31)))
        t += 0.13
    tr = [7, 9, 7, 9]
    for i, o in enumerate(tr):
        add(buf, t+0.15+0.12*i, flute(hz(o, SA*2), 0.16, 0.12, seed=i+5))

# ---- per-scene BGM builders --------------------------------------------------
def build_scene(n, start, end, kind, inten, rng):
    dur = float(end - start)
    buf = np.zeros(N(dur), dtype=np.float32)
    g   = 0.12 + inten*0.022                    # overall bed gain
    den = min(1.0, 0.25 + inten*0.09)           # melodic density

    def base_drone(a=0.045):
        tanpura(buf, 0.1, dur, amp=a)

    if kind in ('T1',):
        base_drone(0.05)
        buf += pad([hz(-12), hz(-5)], dur, amp=g*0.5, seed=n)          # soft strings
        buf += melody(MOHANAM, SA*2, dur, rng, den, amp=g*1.4, kind='flute')
        if n >= 4:
            buf += melody(MOHANAM, SA, dur, rng, den*0.6, amp=g*1.1, kind='veena', tmin=3.0)
        for tb in np.arange(4.0, dur-2.0, 6.5):                          # santoor shimmer
            add(buf, tb, bell(hz(24+int(rng.integers(0,3)*2)), 1.4, 0.035))

    elif kind in ('T2', 'T2_STOP', 'T2_MEM'):
        slow = (kind == 'T2_MEM'); gg = g*(0.7 if slow else 1.0)
        base_drone(0.05)
        buf += pad([hz(-12), hz(-5), hz(4-12)], dur, amp=gg*0.7, seed=n)
        buf += melody(KALYANI, SA*2, dur, rng, den*(0.6 if slow else 1.0),
                      amp=gg*1.5, kind='veena')
        if inten >= 4 and not slow:                                      # mridangam heartbeat
            for tb in np.arange(1.0, dur-(1.5 if kind == 'T2_STOP' else 0.5), 1.5):
                add(buf, tb, thump(amp=gg*1.3*0.5/(1+tb*0.05), seed=int(tb*7)))
        for tb in np.arange(2.5, dur-2.0, 5.0):                          # chime accents
            add(buf, tb, bell(hz(24), 1.6, gg*0.28))
        if kind == 'T2_STOP':                                            # crest then HARD ending
            add(buf, 0.0, pad([hz(0), hz(7), hz(16)], min(4.0, dur), amp=gg*0.8, seed=88, a_t=1.2, r_t=2.0))
            k = int((dur-2.0)*SR); buf[k:] *= np.linspace(1, 0, len(buf)-k)**2

    elif kind in ('T4', 'T4_BARE', 'T4_STING', 'T4_RIT', 'T4_WORK', 'T4',
                  'T14_BLEND', 'PLAYFUL'):
        base_drone(0.045 if kind != 'T4_BARE' else 0.035)
        warm = pad([hz(-12), hz(7-12)], dur, amp=g*0.55, seed=n)
        if kind == 'T14_BLEND': warm += pad([hz(-5)], dur, amp=g*0.4, seed=n+40)
        buf += warm
        if kind != 'T4_BARE':
            buf += melody(HAMSADHWANI, SA*2, dur, rng, den*0.9, amp=g*1.35, kind='veena')
            if inten >= 3:
                buf += melody(HAMSADHWANI, SA*4, dur, rng, den*0.5, amp=g*0.9,
                              kind='flute', tmin=4.0)
        if kind in ('T4_STING', 'PLAYFUL'):
            stinger(buf, dur, rng, playful=True)
        if kind == 'PLAYFUL' and n == 40:                                 # council bed loop
            for tb in np.arange(3.0, dur-2.0, 2.2):
                add(buf, tb, pluck(hz([0, 4, 7, 4][int(tb) % 4], SA*2), 0.5, 0.10, seed=int(tb)))
        if kind == 'T4_RIT':                                             # 1-2-3 rest pulse
            tb = 1.0
            while tb < dur-1.0:
                add(buf, tb, thump(amp=g*1.6, seed=int(tb)))
                add(buf, tb+0.6, tick(amp=0.10, seed=int(tb)))
                add(buf, tb+1.2, tick(amp=0.08, seed=int(tb+1)))
                tb += 2.4
        if kind == 'T4_WORK':
            for tb in np.arange(0.5, dur-0.5, 0.8):
                add(buf, tb, tick(amp=0.07, seed=int(tb*3)))
        add(buf, 0.6, bell(hz(24), 2.0, 0.05))                            # hand-bell chime

    elif kind.startswith('T3') or kind in ('ONE_NOTE',):
        cold = pad([hz(-24), hz(-12)], dur, amp=g*0.75, seed=n, a_t=2.4)
        buf += cold
        tanpura(buf, 0.5, dur, amp=0.028, base=SA/2)
        if kind not in ('T3_VOID', 'T3_BARE', 'ONE_NOTE', 'T3_HB'):
            buf += melody(SHIVARANJANI, SA*2, dur, rng, den*0.55, amp=g*1.2,
                          kind='flute', tmin=1.6, tmargin=2.0)
        if kind in ('T3_HB', 'T3_VOID'):
            step = 3.0 if kind == 'T3_HB' else 4.5
            for tb in np.arange(1.5, dur-1.0, step):
                add(buf, tb, thump(amp=g*2.2, seed=int(tb*5)))
        if kind == 'T3_WARM':
            buf += pad([hz(-5)], dur, amp=g*0.4, seed=n+9)
        if kind == 'T3_RISE':
            buf += pad([hz(-12), hz(0)], dur, amp=g*0.5, seed=n+3, a_t=3.0)
        if kind == 'T3_TO_T4':
            buf += melody(HAMSADHWANI, SA*2, dur, rng, 0.3, amp=g*0.9, kind='veena', tmin=dur/2)
        if kind in ('T3_Q', 'T3_Q_STR', 'T3_QFRAG'):
            q = q_motif(dur, SA*2, amp=g*1.5)
            if kind == 'T3_QFRAG': q[int(2.4*SR):] = 0                    # fragment only
            tq = dur*0.45 - 1.5
            add(buf, max(0.5, tq), q)
            if kind == 'T3_Q_STR':
                buf += pad([hz(3-12)], dur, amp=g*0.4, seed=n)            # dissonant colour
        if kind == 'T3_GHOST2':
            add(buf, 1.2, melody(KALYANI, SA*2, min(6.0, dur-2), rng, 0.25, amp=g*0.8, kind='veena'))
        if kind == 'T3_THIN':                                            # last 2 s → near silence
            buf += melody(SHIVARANJANI, SA*2, dur, rng, 0.2, amp=g*0.9, kind='flute')
            k = int((dur-3.5)*SR); buf[k:] *= np.linspace(1, 0.06, len(buf)-k)
        add(buf, 2.0, pluck(hz(12, SA*2), 2.4, g*0.8, bright=1.6))        # veena harmonic ring
        if kind == 'ONE_NOTE':
            buf[:] = pad([hz(-12)], dur, amp=0.07, seed=n, a_t=1.5)

    elif kind == 'NEAR_NOTHING':
        buf += pad([hz(-24)], dur, amp=0.05, seed=n, a_t=3.0)
        add(buf, 1.5, pluck(hz(-5), 2.0, 0.09, bright=0.5, seed=1))       # one cello-ish stroke
        tanpura(buf, 2.0, dur, amp=0.02, base=SA/2)

    elif kind == 'S48_STOP_Q':
        buf[:int(1.4*SR)] = 0                                             # FULL STOP opening
        buf += pad([hz(-12)], dur, amp=0.06, seed=n, a_t=2.2)
        add(buf, dur-4.6, q_motif(dur-(dur-4.6), SA*2, amp=0.16))         # Q motif over the string

    elif kind in ('SUSPENSE', 'SUSPENSE_UP', 'SUSPENSE_BELL'):
        accel = {'SUSPENSE': 2.2, 'SUSPENSE_UP': 1.4, 'SUSPENSE_BELL': 1.1}[kind]
        buf += pad([hz(-24), hz(-12), hz(-13)], dur, amp=g*0.7, seed=n, a_t=2.0)
        trem = np.sin(2*np.pi*hz(24)*np.arange(N(dur))/SR) \
             * (0.5+0.5*np.sin(2*np.pi*6*np.arange(N(dur))/SR))*g*0.10    # high tremolo
        buf += trem.astype(np.float32)
        tb = 1.0
        while tb < dur-0.5:
            add(buf, tb, thump(amp=g*2.4, seed=int(tb*11)))
            tb += max(0.55, accel - tb*0.05)                              # accelerando
        if kind == 'SUSPENSE_BELL':
            for tb in np.arange(1.5, dur-1.0, 2.6):
                add(buf, tb, bell(hz(19+int(rng.integers(0, 4))), 1.8, 0.06))

    elif kind in ('T5_CELL', 'T5', 'T5_WALK', 'T5_CREST', 'T5_FRIEND', 'QA_ALT'):
        buf += pad([hz(-12), hz(0), hz(7-12)], dur, amp=g*0.8, seed=n)    # warm floor
        tanpura(buf, 0.2, dur, amp=0.03)
        if kind == 'T5_CELL':
            add(buf, 1.5, pluck(hz(24), 3.0, 0.22, bright=1.8, seed=53))  # first pure veena harmonic
            add(buf, 6.0, pluck(hz(24), 3.0, 0.18, bright=1.8, seed=54))
            am = a_motif(6.0, SA*2, amp=g*1.4)
            add(buf, dur-6.5, am)
        else:
            add(buf, 1.0 + (n % 3)*0.8, a_motif(6.0, SA*2, amp=g*(1.5 if kind != 'T5_FRIEND' else 1.2)))
            if kind in ('T5_WALK', 'T5_CREST', 'T5'):
                tb = 0.8
                while tb < dur-0.5:
                    add(buf, tb, thump(amp=g*1.2, seed=int(tb*13)))
                    add(buf, tb+0.3, tick(amp=0.08, seed=int(tb*17)))
                    tb += 0.62
            if kind == 'T5_CREST':
                buf += pad([hz(0), hz(7), hz(16), hz(24)], dur, amp=g*0.5, seed=n+7, a_t=2.5)
                buf += melody(MOHANAKALY, SA*4, dur, rng, den, amp=g*0.8, kind='flute', tmin=2.0)
            if kind == 'T5_FRIEND':
                buf += melody(HAMSADHWANI, SA*4, dur, rng, den*0.7, amp=g*0.85, kind='flute')
            for tb in np.arange(3.0, dur-2.0, 4.6):
                add(buf, tb, bell(hz(24), 1.6, g*0.3))
        if kind == 'QA_ALT':
            add(buf, 1.2, q_motif(5.0, SA*2, amp=g*1.1))
            add(buf, dur-5.8, a_motif(5.5, SA*2, amp=g*1.3))

    elif kind == 'HELD_CHORD':
        buf[:] = pad([hz(-12), hz(0), hz(7), hz(16)], dur, amp=0.09, seed=n, a_t=1.6, r_t=3.5)

    elif kind == 'SEMI_RESOLVE':
        buf += pad([hz(-12), hz(0), hz(4), hz(7)], dur, amp=0.08, seed=n, a_t=2.0)
        add(buf, dur-4.0, pluck(hz(16), 3.2, 0.12, bright=1.6, seed=63))  # veena breath

    elif kind == 'UNION':
        bar = 3.2                                                          # 4 bars, motifs interlocked
        add(buf, 0.3, q_motif(bar+0.4, SA*2, amp=g*1.2))                   # bar 1: question
        add(buf, bar+0.15, a_motif(4.2, SA*2, amp=g*1.3))                  # bar 2: answer
        for i in range(2):                                                 # bars 3-4: interlocked
            add(buf, 2*bar+0.1+i*bar*0.5, q_motif(bar, SA*2, amp=g*0.95))
            add(buf, 2*bar+1.7+i*bar*0.5, a_motif(bar*0.8, SA*4, amp=g*0.9))
        buf += pad([hz(0), hz(7), hz(16)], dur, amp=g*0.6, seed=n, a_t=2.0)# resolving bloom
        add(buf, 4*bar-0.8, bell(hz(24), 2.0, 0.12))
        k = int((4*bar)*SR*1.02)                                           # sudden full stop on cut
        if k < len(buf): buf[k:] = 0
        buf[int((4*bar-0.15)*SR):k] = 0

    elif kind == 'HANG':
        buf += pad([hz(-24)], dur, amp=0.045, seed=n, a_t=2.5)
        add(buf, 1.0, q_motif(4.0, SA*2, amp=0.10))                        # unresolved question hangs
        add(buf, dur-3.4, pluck(hz(24), 3.0, 0.10, bright=1.8, seed=65))   # far veena answers, unresolved

    elif kind == 'ENDCARD':
        tanpura(buf, 0.2, dur-2.0, amp=0.028)
        add(buf, 1.2, pluck(hz(24), 3.4, 0.16, bright=1.9, seed=66))       # single veena harmonic
        add(buf, 6.5, a_motif(5.0, SA*2, amp=0.10))                        # one last gentle answer
        add(buf, dur-2.2, bell(hz(12), 2.0, 0.09))
        add(buf, dur-1.9, thump(amp=0.34, seed=66))                        # final thump
        k = int((dur-1.55)*SR); buf[k:] = 0                                # clean silence tail

    return buf

# ---- render master -----------------------------------------------------------
TOTAL = SCENES[-1][2]
bgm = np.zeros(N(TOTAL), dtype=np.float32)
sfx = np.zeros(N(TOTAL), dtype=np.float32)
vob = np.zeros(N(TOTAL), dtype=np.float32)

print("synthesizing BGM…")
for idx, (n, s, e, kind, inten) in enumerate(SCENES):
    rng = np.random.default_rng(1000+n)
    segb = build_scene(n, s, e, kind, inten, rng)
    pkind  = SCENES[idx-1][3] if idx > 0 else None
    nkind  = SCENES[idx+1][3] if idx < len(SCENES)-1 else None
    same_p = pkind and pkind[0] == kind[0]
    same_n = nkind and nkind[0] == kind[0]
    fi = int((0.08 if same_p else 0.9)*SR); fo = int((0.08 if same_n else 0.9)*SR)
    if kind in ('T2_STOP', 'S48_STOP_Q', 'UNION', 'ENDCARD'): fo = int(0.05*SR)
    if kind in ('NEAR_NOTHING', 'HANG'): fo = int(1.6*SR)
    if fi < len(segb): segb[:fi]  *= np.linspace(0, 1, fi)
    if fo > 0:         segb[-fo:] *= np.linspace(1, 0, fo)
    add(bgm, s, segb)

print("synthesizing SFX layer…")
for (n, s, e, kind, inten) in SCENES:
    d = float(e - s)
    segx = sfx_scene(n, d)
    m = int(0.4*SR)
    segx[:m] *= np.linspace(0, 1, m); segx[-m:] *= np.linspace(1, 0, m)
    add(sfx, s, segx)

def compress_pauses(vo, sr, max_pause=0.62, floor=0.012):
    """silence-compress: cap over-long TTS pauses at max_pause sec —
    keeps every spoken word at natural speed, breathing room intact."""
    fl = int(0.02*sr)
    nf = len(vo)//fl
    if nf == 0: return vo
    rms = np.sqrt(np.mean(vo[:nf*fl].reshape(nf, fl)**2, axis=1))
    thr = max(floor, rms.max()*0.06)
    speech = rms > thr
    out = []
    i = 0
    while i < nf:
        j = i
        if speech[i]:
            while j < nf and speech[j]: j += 1
            out.append(vo[i*fl:j*fl])
        else:
            while j < nf and not speech[j]: j += 1
            run = (j-i)*fl/sr
            keep = min(run, max_pause)
            seg = vo[i*fl:(i+int(max(1, keep*sr/fl))*fl)]
            out.append(seg[:int(keep*sr)])
        i = j
    if not out: return vo
    res = np.concatenate(out).astype(np.float32)
    m = int(0.015*sr)                                                     # 15 ms edge fades
    if len(res) > 2*m:
        res[:m] *= np.linspace(0, 1, m); res[-m:] *= np.linspace(1, 0, m)
    return res

print("placing narration…")
fits = 0
for n, s, e, kind, inten in SCENES:
    mp3 = os.path.join(ROOT, 'audio', f'EP01_S{n:02d}.mp3')
    out = subprocess.run([FF, '-v', 'error', '-i', mp3, '-f', 'f32le', '-ac', '1',
                          '-ar', str(SR), '-'], capture_output=True)
    vo = np.frombuffer(out.stdout, dtype=np.float32).copy()
    raw = len(vo)/SR
    vo = compress_pauses(vo, SR)
    win = (e - s) - 0.45
    if len(vo)/SR > win:                                                  # only if still long: ≤5 % fit
        ratio = max(0.95, win/(len(vo)/SR))
        x = np.linspace(0, len(vo)-1, int(len(vo)*ratio))
        vo = np.interp(x, np.arange(len(vo)), vo).astype(np.float32)
        fits += 1
        print(f"  S{n:02d}: {raw:.1f}s → {len(vo)/SR:.1f}s (fit ×{ratio:.3f})")
    add(vob, s + (0.35 if kind not in ('S48_STOP_Q',) else 1.6), vo*0.98)
print(f"  speed-fitted scenes: {fits}/66 (rest = natural pace, pauses capped at 0.62s)")

# ---- duck music under speech -------------------------------------------------
print("ducking + mastering…")
env  = np.abs(vob)
k    = np.ones(int(0.30*SR))/int(0.30*SR)
mask = np.clip(np.convolve((env > 0.010).astype(np.float32), k, 'same')*2.2, 0, 1)
bgm *= (1.0 - 0.66*mask)                                                  # ≈ −9.4 dB under speech
sfx *= (1.0 - 0.50*mask)                                                  # ≈ −6.0 dB under speech

mix = vob*1.0 + bgm*0.92 + sfx*0.85
mix /= max(1e-9, np.abs(mix).max()); mix *= 0.94
wav = os.path.join(WORK, 'master.wav')
from wave import open as wopen
with wopen(wav, 'wb') as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1)*32767).astype('<i2').tobytes())

norm = os.path.join(WORK, 'master_norm.wav')
subprocess.run([FF, '-y', '-v', 'error', '-i', wav,
                '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11', '-ar', '44100', '-ac', '2', norm], check=True)

master_mp3 = os.path.join(ROOT, 'EP01_MASTER_13m58s.mp3')
subprocess.run([FF, '-y', '-v', 'error', '-i', norm, '-b:a', '192k', master_mp3], check=True)
print("master →", master_mp3)

# ---- per-scene clips ---------------------------------------------------------
print("rendering 66 scene clips…")
for n, s, e, kind, inten in SCENES:
    d = e - s
    outp = os.path.join(OUT_SCENES, f'EP01_S{n:02d}.mp3')
    subprocess.run([FF, '-y', '-v', 'error', '-ss', f'{s:.2f}', '-t', f'{d:.2f}', '-i', norm,
                    '-af', f'afade=t=in:st=0:d=0.06,afade=t=out:st={d-0.10:.2f}:d=0.10',
                    '-b:a', '160k', outp], check=True)
print("done. 66 clips →", OUT_SCENES)
