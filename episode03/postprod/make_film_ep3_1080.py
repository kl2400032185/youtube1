#!/usr/bin/env python3
"""EP3 FINAL master BASE (1080p, stronger motion): type-aware Ken-Burns motion over the 68 keyframes,
length-neutral straight cuts on scene_map_ep3 (audio sync preserved exactly).
Fade beats (length-neutral): S01 in, S28 out (into gold wash), S58 out (into return),
S68 tail. Cinematic grade + live grain. S68 sources the baked TEXT end card."""
import subprocess, json, os
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, W, H = 24, 1920, 1080
sm = json.load(open(os.path.join(ROOT, 'scene_map_ep3.json')))
scenes = sm['scenes']
assert len(scenes) == 68, len(scenes)

# ---- EP3 motion grammar ----
CLOSE = {2,9,12,16,19,24,26,27,30,31,36,38,48,49,51,58,60,62,66,67}   # contemplative: very slow push
WIDE  = {1,3,4,5,7,8,13,14,15,20,21,22,23,28,32,33,34,40,41,42,43,44,45,47,52,53,54,56,61,63,64,65,68}
VISION = set(range(31, 58))                                           # dreamy zero-yaw float
EPIC_RISE = {36: 0.11, 57: 0.12, 60: 0.07}                            # Lord emerges / whole mandala / eyes open

def motion(i, frames):
    zoom = EPIC_RISE.get(i, 0.05 if i in VISION else (0.065 if i in CLOSE else 0.10))
    rate = zoom / frames
    if i in VISION:
        drift_x = ((15 if i % 2 else -15)) / frames
        drift_y = ((8 if i % 3 else -8)) / frames
    else:
        drift_x = ((26 if i in WIDE else 13) * (1 if i % 2 else -1)) / frames
        drift_y = ((8 if i in WIDE else 4) * (1 if i % 3 else -1)) / frames
    zoom_in = (i % 2 == 1) or i in EPIC_RISE or (51 <= i <= 57)   # approach the light
    z = f"1+{rate:.7f}*on" if zoom_in else f"{1+zoom+0.01:.4f}-{rate:.7f}*on"
    xp = (12.0 if i % 2 else 60.0) / 100.0
    yp = (18.0 if i % 3 else 58.0) / 100.0
    return (z, f"(iw-iw/zoom)*{xp:.2f}+{drift_x:.5f}*on",
               f"(ih-ih/zoom)*{yp:.2f}+{drift_y:.5f}*on")

inputs, chains = [], []
for i, s in enumerate(scenes, 1):
    dur = s['end'] - s['start']
    img = os.path.join(ROOT, 'assets', f'EP03_S{i:02d}.jpg')
    if i == 68:
        img = os.path.join(ROOT, 'assets', 'EP03_S68_card_1080.jpg')
    inputs += ['-loop', '1', '-framerate', str(FPS), '-t', f"{dur:.3f}", '-i', img]
    frames = max(24, int(round(dur * FPS)))
    z, x, y = motion(i, frames)
    v = (f"[{i-1}:v]scale=2560:1440:force_original_aspect_ratio=increase,crop=2560:1440,"
         f"setsar=1,zoompan=z='{z}':x='{x}':y='{y}':d=1:fps={FPS}:s={W}x{H}")
    if i == 1:
        v += ",fade=t=in:st=0:d=0.5"
    if i == 28:
        v += f",fade=t=out:st={dur-0.5:.3f}:d=0.5"   # melt into gold wash
    if i == 58:
        v += f",fade=t=out:st={dur-0.7:.3f}:d=0.7"   # vision folds into the return
    if i == 68:
        v += f",fade=t=out:st={dur-1.5:.3f}:d=1.5"
    chains.append(v + f"[v{i}]")

concat = "".join(f"[v{i}]" for i in range(1, 69))
fc = (";".join(chains) + ";" + f"{concat}concat=n=68:v=1:a=0,"
      "eq=contrast=1.045:saturation=1.09:gamma=0.99,format=yuv420p[vout]")

audio = os.path.join(ROOT, 'EP03_WITH_BGM.mp3')
out = os.path.join(ROOT, 'EP03_BASE_1080p.mp4')
cmd = [FF, '-y', '-v', 'warning'] + inputs + ['-i', audio,
    '-filter_complex', fc, '-map', '[vout]', '-map', '68:a?',
    '-r', str(FPS), '-c:v', 'libx264', '-preset', 'fast', '-crf', '21',
    '-tune', 'film', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-shortest', out]
print('graph chars:', len(fc), flush=True)
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print('FAIL:\n', '\n'.join(r.stderr.splitlines()[-25:])); raise SystemExit(1)
p = subprocess.run([FF, '-i', out, '-hide_banner'], capture_output=True, text=True)
print('WROTE', out, [l for l in p.stderr.splitlines() if 'Duration' in l][0].split('Duration: ')[1].split(',')[0],
      f"{os.path.getsize(out)/1e6:.1f} MB", flush=True)
