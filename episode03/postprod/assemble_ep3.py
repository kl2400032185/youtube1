#!/usr/bin/env python3
"""EP3 assembler — tight-flow master with VISION-HOLD FLOORS (locked recipe, see tracker):
- every scene: silence-trimmed VO (40ms edges + 60ms breath margin), 0.45s gaps
- scenes 19..58 (ritual -> samadhi -> vision): slot = max(blueprint design, VO+0.45)
  -> vision vistas/music breathe; narration itself never lags (user rule).
- peak cap 0.89 -> loudnorm -16 LUFS / TP -1.5 / LRA 11  ->  EP03_CLEAN_VOICE.mp3
- writes scene_map_ep3.json (design floor included per scene)"""
import subprocess, json, os, re
import numpy as np, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe(); SR = 44100
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAP, LEAD = 0.45, 0.30
TRIM_THR, TRIM_MARGIN, RAMP = 0.012, 0.06, 0.03
VISION_FLOOR = set(range(19, 59))   # S19..S58 hold to design slot if longer

def dec(p):
    o = subprocess.run([FF,'-v','error','-i',p,'-f','f32le','-ac','1','-ar',str(SR),'-'],
                       capture_output=True, check=True)
    return np.frombuffer(o.stdout, dtype=np.float32).copy()

def trim(x):
    env = np.abs(x); w = int(0.02*SR); env = np.convolve(env, np.ones(w)/w,'same')
    idx = np.where(env > TRIM_THR)[0]
    if len(idx)==0: return x
    a = max(0, idx[0]-int(TRIM_MARGIN*SR)); b = min(len(x), idx[-1]+int(TRIM_MARGIN*SR))
    return x[a:b]

def ramp(x):
    n = min(int(RAMP*SR), len(x)//2); r = np.linspace(0.,1.,n).astype(np.float32)
    x[:n]*=r; x[-n:]*=r[::-1]; return x

# design durations from plan: '### SCENE NN ... **E.** Design KKs'
plan = open(os.path.join(ROOT,'EPISODE_03_PRODUCTION_PLAN.md'),encoding='utf-8').read()
design = {int(n): int(d) for n,d in re.findall(r'### SCENE (\d+).*?\*\*E\.\*\* Design (\d+)s', plan, re.S)}
assert len(design)==68, f'design parse got {len(design)}'

clips, missing = {}, []
for n in range(1,69):
    p = os.path.join(ROOT,'audio',f'EP03_S{n:02d}.mp3')
    if not os.path.exists(p): missing.append(n); continue
    clips[n] = dec(p)
assert not missing, f'missing clips: {missing}'

parts=[np.zeros(int(LEAD*SR),dtype=np.float32)]; scene_map=[]; t=LEAD
raw_total=trimmed_total=hold_added=0.0
for n in range(1,69):
    raw=clips[n]; vo=ramp(trim(raw)); raw_total+=len(raw)/SR; trimmed_total+=len(vo)/SR
    vo_dur=len(vo)/SR
    slot = vo_dur + (GAP if n<69 else 0.0)
    if n in VISION_FLOOR and float(design[n]) > slot:
        hold_added += float(design[n]) - slot
        slot = float(design[n])
    start=t; vo_end=start+vo_dur; end=start+slot
    parts.append(vo); tail=slot-vo_dur
    if tail>0: parts.append(np.zeros(int(tail*SR),dtype=np.float32))
    scene_map.append({'n':n,'scene':n,'start':round(start,3),'vo_end':round(vo_end,3),
                      'end':round(end,3),'vo_dur':round(vo_dur,3),'design':design[n]})
    t=end
mix=np.concatenate(parts)
peak=float(np.abs(mix).max())
if peak>0.89: mix*=0.89/peak
subprocess.run([FF,'-y','-v','error','-f','f32le','-ac','1','-ar',str(SR),'-i','-',
               '-c:a','pcm_s16le','/tmp/_ep3.wav'],input=mix.tobytes(),check=True)
subprocess.run([FF,'-y','-v','error','-i','/tmp/_ep3.wav','-af','loudnorm=I=-16:TP=-1.5:LRA=11',
               '-c:a','libmp3lame','-q:a','2',os.path.join(ROOT,'EP03_CLEAN_VOICE.mp3')],check=True)
json.dump({'total':round(t,3),'gap':GAP,'lead':LEAD,'vision_floor':'S19..S58 slot=max(design,VO+gap)','scenes':scene_map},
          open(os.path.join(ROOT,'scene_map_ep3.json'),'w'),indent=1)
m,s=divmod(t,60)
print(f"OK master {int(m)}:{s:04.1f} | raw {raw_total/60:.1f}m -> trimmed {trimmed_total/60:.1f}m | vision-hold +{hold_added:.0f}s")
print('runtime >= 10:00 ->', 'PASS' if t>=600 else 'FAIL')
