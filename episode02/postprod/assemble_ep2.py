#!/usr/bin/env python3
"""Assemble Episode 2 audio masters from the 69 per-scene VO clips.
Recipe inherits EP1-v4: natural pace, scene slot = max(design, vo + 0.9s gap).
Outputs:
  episode02/EP02_CLEAN_VOICE.mp3   — narration-only master (PRIMARY)
  episode02/scene_map_ep2.json     — per-scene start/end in the master (drives BGM + picture fit)
Requires: all 69 clips in episode02/audio/EP02_S01..S69.mp3
"""
import subprocess, json, re, sys, os
import numpy as np
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.abspath(__file__)).replace('/postprod', '')
AUDIO = f"{ROOT}/audio"
PLAN = f"{ROOT}/EPISODE_02_PRODUCTION_PLAN.md"
SR = 44100

# ---- design durations from the blueprint (single source of truth) ----
ts = re.findall(r'\*\*Timecode:\*\* \d+:\d+–\d+:\d+ · \*\*Duration:\*\* (\d+) sec',
                open(PLAN, encoding='utf-8').read())
assert len(ts) == 69, f"expected 69 design durations, found {len(ts)}"
design = [int(x) for x in ts]

def decode(f):
    out = subprocess.run([FF, '-v', 'error', '-i', f, '-f', 'f32le', '-ac', '1',
                          '-ar', str(SR), '-'], capture_output=True, check=True)
    x = np.frombuffer(out.stdout, dtype=np.float32)
    assert len(x) > SR * 0.5, f"suspicious empty decode: {f}"
    return x

missing = [n for n in range(1, 70) if not os.path.exists(f"{AUDIO}/EP02_S{n:02d}.mp3")]
if missing:
    print("MISSING clips:", missing); sys.exit(1)

GAP = 0.9
slots, scene_map, voice = [], [], []
t = 0.0
for n in range(1, 70):
    x = decode(f"{AUDIO}/EP02_S{n:02d}.mp3")
    vo = len(x) / SR
    slot = max(design[n-1], vo + GAP)
    scene_map.append(dict(n=n, start=round(t, 2), vo_end=round(t + vo, 2),
                          end=round(t + slot, 2), vo_dur=round(vo, 2), design=design[n-1]))
    voice.append(x)
    pad_s = slot - vo
    if pad_s > 0: voice.append(np.zeros(int(pad_s * SR), dtype=np.float32))
    t += slot
    assert len(x) and not np.isnan(x).any()

master = np.concatenate(voice)
# gentle master bus: soft limiter -> loudness via ffmpeg loudnorm below
peak = np.abs(master).max()
if peak > 0.89: master = master * (0.89 / peak)
wpath = "/tmp/ep02_voice_raw.wav"
subprocess.run([FF, '-y', '-v', 'error', '-f', 'f32le', '-ac', '1', '-ar', str(SR),
                '-i', '-', '-c:a', 'pcm_s16le', wpath], input=master.tobytes(), check=True)
subprocess.run([FF, '-y', '-v', 'error', '-i', wpath,
                '-af', 'loudnorm=I=-16:TP=-1.5:LRA=11',
                '-c:a', 'libmp3lame', '-q:a', '2', f"{ROOT}/EP02_CLEAN_VOICE.mp3"], check=True)

# save in float32 for the BGM mixer (pre-loudnorm, pre-encode)
np.save("/tmp/ep02_voice_master.npy", master)
json.dump(dict(total=round(t, 2), scenes=scene_map),
          open(f"{ROOT}/scene_map_ep2.json", 'w'), indent=1)

mm = int(t // 60); ss = t % 60
print(f"OK master {mm}:{ss:04.1f} | slots>design: {sum(1 for s in scene_map if s['vo_dur'] + GAP > s['design'])}/69 scenes grew")
print(f"wrote EP02_CLEAN_VOICE.mp3 + scene_map_ep2.json")
