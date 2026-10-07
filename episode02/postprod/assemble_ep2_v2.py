#!/usr/bin/env python3
"""EP2 v2 assembler — TIGHT FLOW per user note: no dead air, straight to story, runtime > 10 min.
- trims leading/trailing silence from each scene VO clip (TTS pads both ends)
- 0.45s breath-gap between scenes, 0.3s lead-in; no design-slot holds
- peak cap 0.89 -> loudnorm -16 LUFS / TP -1.5 / LRA 11  ->  EP02_CLEAN_VOICE.mp3
- rewrites scene_map_ep2.json (drives BGM engine + picture sync)
"""
import subprocess, json, os, re
import numpy as np, imageio_ffmpeg

FF   = imageio_ffmpeg.get_ffmpeg_exe()
SR   = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # episode02/
GAP  = 0.45        # s between scenes
LEAD = 0.30        # s before S01
TRIM_THR   = 0.012 # envelope threshold (~-38 dBFS)
TRIM_MARGIN= 0.06  # keep this much breath at edges
RAMP       = 0.03  # fade at trimmed edges (anti-click)

def dec(path):
    o = subprocess.run([FF,'-v','error','-i',path,'-f','f32le','-ac','1','-ar',str(SR),'-'],
                       capture_output=True, check=True)
    return np.frombuffer(o.stdout, dtype=np.float32).copy()

def trim(x):
    env = np.abs(x); w = int(0.02*SR)
    env = np.convolve(env, np.ones(w)/w, 'same')
    idx = np.where(env > TRIM_THR)[0]
    if len(idx) == 0: return x
    a = max(0, idx[0] - int(TRIM_MARGIN*SR)); b = min(len(x), idx[-1] + int(TRIM_MARGIN*SR))
    return x[a:b]

def ramp(x):
    n = min(int(RAMP*SR), len(x)//2)
    r = np.linspace(0.,1.,n).astype(np.float32)
    x[:n] *= r; x[-n:] *= r[::-1]
    return x

clips, missing = {}, []
for n in range(1,70):
    p = os.path.join(ROOT, 'audio', f'EP02_S{n:02d}.mp3')
    if not os.path.exists(p): missing.append(n); continue
    clips[n] = dec(p)
assert not missing, f'missing clips: {missing}'

parts = [np.zeros(int(LEAD*SR), dtype=np.float32)]
scene_map = []
t = LEAD
raw_total = trimmed_total = 0.0
for n in range(1,70):
    raw = clips[n]; vo = ramp(trim(raw))
    raw_total += len(raw)/SR; trimmed_total += len(vo)/SR
    start = t; vo_end = start + len(vo)/SR; end = vo_end + (GAP if n < 69 else 0.0)
    parts.append(vo)
    if n < 69: parts.append(np.zeros(int(GAP*SR), dtype=np.float32))
    scene_map.append({'n': n, 'scene': n, 'start': round(start,3), 'vo_end': round(vo_end,3),
                      'end': round(end,3), 'vo_dur': round(len(vo)/SR,3)})
    t = end
mix = np.concatenate(parts)
peak = float(np.abs(mix).max())
if peak > 0.89: mix *= 0.89/peak

subprocess.run([FF,'-y','-v','error','-f','f32le','-ac','1','-ar',str(SR),'-i','-',
               '-c:a','pcm_s16le','/tmp/_ep2_v2.wav'], input=mix.tobytes(), check=True)
subprocess.run([FF,'-y','-v','error','-i','/tmp/_ep2_v2.wav',
               '-af','loudnorm=I=-16:TP=-1.5:LRA=11',
               '-c:a','libmp3lame','-q:a','2', os.path.join(ROOT,'EP02_CLEAN_VOICE.mp3')], check=True)

total = float(t)
json.dump({'total': round(total,3), 'gap': GAP, 'lead': LEAD, 'scenes': scene_map},
          open(os.path.join(ROOT,'scene_map_ep2.json'),'w'), indent=1)
m, s = divmod(total, 60)
print(f"OK tight master {int(m)}:{s:04.1f} | raw VO {raw_total/60:.1f}min -> trimmed {trimmed_total/60:.1f}min | 69 scenes")
print('runtime >= 10:00 ->', 'PASS' if total >= 600 else 'FAIL (would need longer gaps)')
