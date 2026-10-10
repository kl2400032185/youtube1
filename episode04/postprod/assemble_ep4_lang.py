import sys
LANG = sys.argv[1]
assert LANG in ('hi','en')
#!/usr/bin/env python3
"""EP4 multilingual assembly (argv: LANG = hi|en): 56 slots from vo_script JSON designs (HARD <10:00 target 7.0-7.9).
slot = max(design, trimmed_VO + 0.45) for speaking scenes; design for visual-only.
S38 'శుకా… శుకా…' gets a forest echo (aecho) baked into its clip.
Outputs: episode04/EP04_CLEAN_VOICE.mp3 + episode04/scene_map_ep4.json"""
import subprocess, os, json
import numpy as np, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUD = os.path.join(ROOT, 'audio_' + LANG)
SR = 44100

def decode(f):
    o = subprocess.run([FF, '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-'],
                       capture_output=True, check=True)
    return np.frombuffer(o.stdout, dtype=np.float32).copy()

def trim(x, thr=0.009, pad=T_pad if False else None):
    pass
T_pad = 0.30
def trimm(x, thr=0.009, pad=T_pad):
    e = np.abs(x)
    w = 2205
    sm = np.convolve(e, np.ones(w)/w, 'same')
    idx = np.where(sm > thr)[0]
    if len(idx) == 0: return x
    s, t = idx[0], idx[-1]
    p = int(pad * SR)
    return x[max(0, s-p):min(len(x), t+p)]

def echo(x, D=0.42, FB=0.55, N=4):
    y = np.zeros(len(x) + int(SR * D * N * 1.6), dtype=np.float32)
    y[:len(x)] = x
    for k in range(1, N+1):
        g = FB ** k
        st = int(D * k * SR)
        y[st:st+len(x)] += x * g
    return y * (1.0/1.25)

def write_mp3(sig, out, tag=None):
    sig = sig.astype(np.float32)
    p = subprocess.run([FF, '-y', '-f', 'f32le', '-ac', '1', '-ar', str(SR), '-i', '-',
                        '-c:a', 'pcm_s16le', '/tmp/_ep4.wav'], input=sig.tobytes(), capture_output=True)
    assert p.returncode == 0, p.stderr[-300:]
    args = [FF, '-y', '-v', 'error', '-i', '/tmp/_ep4.wav']
    if tag: args += ['-af', f'loudnorm={tag}']
    args += ['-ar', '44100', '-c:a', 'libmp3lame', '-q:a', '2', out]
    r = subprocess.run(args, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-300:]

d = json.load(open(os.path.join(ROOT, 'vo_script', 'EP04_scene_texts_' + LANG + '.json'), encoding='utf-8'))
scenes = d['scenes']
assert len(scenes) == 56
master = np.zeros(0, dtype=np.float32)
smap = []
t = 0.0
for s in scenes:
    n, dur, b = s['n'], s['d'], s['b']
    f = os.path.join(AUD, f'EP04_S{n:02d}.mp3')
    if b and os.path.exists(f):
        vo = trimm(decode(f))
        if n == 38:
            vo = echo(vo)
        slot = max(dur, len(vo)/SR + 0.45)
        beg = len(master)
        master = np.concatenate([master, vo, np.zeros(int((slot - len(vo)/SR) * SR), dtype=np.float32)])
        smap.append({'n': n, 'start': t, 'vo_end': t + len(vo)/SR, 'end': t + slot, 'vo_dur': len(vo)/SR, 'design': dur})
        t += slot
    else:
        master = np.concatenate([master, np.zeros(int(dur * SR), dtype=np.float32)])
        smap.append({'n': n, 'start': t, 'vo_end': t, 'end': t + dur, 'vo_dur': 0.0, 'design': dur})
        t += dur
    print(f"S{n:02d} slot={smap[-1]['end']-smap[-1]['start']:5.2f}s (design {dur:4.1f}) total {t:7.2f}", flush=True)

write_mp3(master, os.path.join(ROOT, 'EP04_CLEAN_VOICE_' + LANG.upper() + '.mp3'), tag='I=-16:TP=-1.5:LRA=11')
sm = {'total': t, 'scenes': [{k: (round(v, 3) if isinstance(v, float) else v) for k, v in s.items()} for s in smap]}
json.dump(sm, open(os.path.join(ROOT, 'scene_map_ep4_' + LANG + '.json'), 'w'), indent=1)
print(f"OK master {int(t//60)}:{t%60:04.1f} | runtime {'PASS' if 420 <= t <= 560 else 'WARN'} (target 7:00-9:20, must be <10:00)")
