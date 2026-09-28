#!/usr/bin/env python3
"""Synthesize comedy music bed + cartoon SFX (pure numpy) -> assets/build/"""
import numpy as np, wave, os

SR = 44100
OUT = "/home/user/youtube1/assets/build"
os.makedirs(f"{OUT}/sfx", exist_ok=True)
rng = np.random.default_rng(7)

def save(name, x, gain=1.0):
    x = np.asarray(x, dtype=np.float64) * gain
    peak = np.max(np.abs(x)) or 1.0
    x = x / max(peak, 1e-9) * 0.92
    pcm = (x * 32767).astype(np.int16)
    with wave.open(f"{OUT}/{name}.wav" if not name.startswith("sfx/") else f"{OUT}/{name}.wav", "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes(pcm.tobytes())

def env(n, a=0.005, r=0.1):
    ai, ri = int(a * SR), int(r * SR)
    ai = max(0, min(ai, n // 2))
    ri = max(0, min(ri, n - ai))
    e = np.ones(n)
    e[:ai] = np.linspace(0, 1, ai)
    e[n - ri:] = np.linspace(1, 0, ri)
    return e

# ---------- Karplus-Strong pluck (ukulele-ish) ----------
def pluck(freq, dur, amp=0.5, decay=0.996):
    n = max(2, int(round(SR / freq)))
    buf = rng.uniform(-1, 1, n)
    L = int(SR * dur)
    out = np.empty(L)
    idx = 0
    for i in range(L):
        out[i] = buf[idx]
        buf[idx] = 0.5 * (buf[idx] + buf[(idx + 1) % n]) * decay
        idx = (idx + 1) % n
    return out * amp * env(L, 0.002, min(0.05, dur * 0.3))

NOTE = {"C3":130.81,"E3":164.81,"F3":174.61,"G3":196.00,"A3":220.00,"B3":246.94,
        "C4":261.63,"D4":293.66,"E4":329.63,"F4":349.23,"G4":392.00,"A4":440.00}

def chord_seq(dur=26.0, bpm=104):
    beat = 60.0 / bpm
    prog = [["C4","E4","G4"], ["G3","B3","D4"], ["A3","C4","E4"], ["F3","A3","C4"]]
    arp = [0, 1, 2, 1, 2, 1, 0, 2]  # eighth-note pattern per bar (2 beats/chord)
    t = 0.0
    bars = []
    ci = 0
    while t < dur:
        ch = prog[ci % 4]
        for step in arp:
            if t >= dur: break
            f = NOTE[ch[step]]
            bars.append((t, f, 0.34))
            t += beat / 2
        # strum start of bar
        for k, nm in enumerate(ch):
            bars.append((t - beat * 2, NOTE[nm], 0.22)) if False else None
        ci += 1
    out = np.zeros(int(SR * (dur + 0.5)))
    for (ts, f, a) in bars:
        s = int(ts * SR)
        p = pluck(f, 0.55, amp=a)
        e = min(len(out) - s, len(p))
        out[s:s + e] += p[:e]
    # gentle fullness: duplicate with tiny delay
    delayed = np.zeros_like(out)
    d = int(0.012 * SR)
    delayed[d:] = out[:-d] * 0.35
    return out + delayed

music = chord_seq()
save("music_bed", music, gain=0.9)

# ---------- SFX ----------
def tone(f0, f1, dur, kind="sine", vib=0.0, a=0.005, r=0.08):
    n = int(SR * dur)
    t = np.arange(n) / SR
    f = np.linspace(f0, f1, n) * (1 + vib * np.sin(2 * np.pi * 6 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    if kind == "sine": w = np.sin(ph)
    elif kind == "saw": w = 2 * ((ph / (2 * np.pi)) % 1) - 1
    elif kind == "square": w = np.sign(np.sin(ph))
    else: w = np.sin(ph)
    return w * env(n, a, r)

def noise(dur, a=0.005, r=0.05, smooth=3):
    n = int(SR * dur)
    x = rng.uniform(-1, 1, n)
    k = np.ones(smooth) / smooth
    x = np.convolve(x, k, mode="same")
    return x * env(n, a, r)

save("sfx/ding", np.sin(2*np.pi*1320*np.arange(int(SR*0.5))/SR) * np.exp(-np.arange(int(SR*0.5))/(SR*0.12))
     + 0.5*np.sin(2*np.pi*1760*np.arange(int(SR*0.5))/SR) * np.exp(-np.arange(int(SR*0.5))/(SR*0.09)))
save("sfx/trombone", tone(320, 196, 0.85, "saw", vib=0.02, a=0.01, r=0.15), 0.8)
save("sfx/boing", np.concatenate([tone(220, 780, 0.16, "sine"), tone(780, 260, 0.22, "sine")]) * 0.7)
save("sfx/whoosh", noise(0.32, 0.01, 0.12, smooth=9) * np.linspace(0.2, 1, int(SR*0.32))[::-1].clip(0.2, 1))
save("sfx/alarm", (tone(880, 880, 0.14, "square") * 0.6).tolist() and np.concatenate(
    [tone(880, 880, 0.13, "square")*0.55, np.zeros(int(SR*0.07)),
     tone(880, 880, 0.13, "square")*0.55, np.zeros(int(SR*0.07)),
     tone(880, 880, 0.13, "square")*0.55]))
save("sfx/pop", tone(900, 260, 0.09, "sine"))
save("sfx/chirp", np.concatenate([tone(2600, 3600, 0.09, "sine"), tone(3200, 2400, 0.08, "sine")]) * 0.7)
save("sfx/sting", tone(110, 98, 0.7, "saw", a=0.004, r=0.25) * 0.75 + tone(116, 104, 0.7, "saw", a=0.004, r=0.25) * 0.6)
save("sfx/sadviolin", tone(440, 392, 0.9, "sine", vib=0.012, a=0.06, r=0.25) * 0.8
     + tone(220, 196, 0.9, "sine", vib=0.012, a=0.06, r=0.25) * 0.5)
save("sfx/sniff", np.concatenate([noise(0.09, 0.004, 0.03, 2), np.zeros(int(SR*0.06)), noise(0.11, 0.004, 0.04, 2)]) * 0.9)
save("sfx/snap", np.concatenate([noise(0.03, 0.001, 0.01, 1) * 0.9, tone(1800, 1200, 0.04, "sine") * 0.6]))
print("audio assets written:", sorted(os.listdir(OUT)), sorted(os.listdir(OUT + "/sfx")))
