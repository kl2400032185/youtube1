#!/usr/bin/env python3
"""EP2 motion-preview film: slow Ken-Burns moves over the 69 keyframes, cut on the
scene map, EP02_WITH_BGM.mp3 as the soundtrack. 1280x720/24 fits under repo caps.
Straight cuts (straight-to-story rule) + fades at the two authored black beats:
S06->S07 (cut-to-black) and S69 tail fade."""
import subprocess, json, os
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, W, H = 24, 1280, 720
sm = json.load(open(os.path.join(ROOT, 'scene_map_ep2.json')))
scenes = sm['scenes']

inputs, chains = [], []
for i, s in enumerate(scenes, 1):
    dur = s['end'] - s['start']
    img = os.path.join(ROOT, 'assets', f'EP02_S{i:02d}.jpg')
    inputs += ['-loop', '1', '-framerate', str(FPS), '-t', f"{dur:.3f}", '-i', img]
    frames = max(24, int(round(dur * FPS)))
    rate = 0.11 / frames                     # ~11% push across the scene (calm)
    drift_x = (14 if i % 2 else -14) / frames   # tiny sideways drift, alternating
    drift_y = (8 if i % 3 else -8) / frames
    zoom_in = (i % 2 == 1)
    z = f"1+{rate:.7f}*on" if zoom_in else f"1.115-{rate:.7f}*on"
    xp = (14.0 if i % 2 else 59.0) / 100.0
    yp = (20.0 if i % 3 else 62.0) / 100.0
    x = f"(iw-iw/zoom)*{xp:.2f}+{drift_x:.5f}*on"
    y = f"(ih-ih/zoom)*{yp:.2f}+{drift_y:.5f}*on"
    v = (f"[{i-1}:v]scale=1600:900:force_original_aspect_ratio=increase,"
         f"crop=1600:900,setsar=1,"
         f"zoompan=z='{z}':x='{x}':y='{y}':d=1:fps={FPS}:s={W}x{H}")
    if i == 6:
        v += f",fade=t=out:st={dur-0.5:.3f}:d=0.5"
    if i in (1, 7):
        v += ",fade=t=in:st=0:d=0.5"
    if i == 69:
        v += f",fade=t=out:st={dur-1.4:.3f}:d=1.4"
    chains.append(v + f"[v{i}]")

concat = "".join(f"[v{i}]" for i in range(1, 70))
fc = ";".join(chains) + ";" + f"{concat.concat}" if False else \
     ";".join(chains) + ";" + f"{concat}concat=n=69:v=1:a=0[vout]"

audio = os.path.join(ROOT, 'EP02_WITH_BGM.mp3')
out = os.path.join(ROOT, 'EP02_PREVIEW_FILM_720p.mp4')
cmd = [FF, '-y', '-v', 'warning'] + inputs + [
    '-i', audio,
    '-filter_complex', fc,
    '-map', '[vout]', '-map', '69:a?',
    '-r', str(FPS), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '25',
    '-tune', 'stillimage', '-pix_fmt', 'yuv420p',
    '-c:a', 'aac', '-b:a', '160k', '-shortest', out]
print('filter graph chars:', len(fc), flush=True)
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print('FAIL tail:\n', '\n'.join(r.stderr.splitlines()[-25:])); raise SystemExit(1)
p = subprocess.run([FF, '-i', out, '-hide_banner'], capture_output=True, text=True)
dl = [l for l in p.stderr.splitlines() if 'Duration' in l][0]
print('WROTE', out, dl.split('Duration: ')[1].split(',')[0],
      f"{os.path.getsize(out)/1e6:.1f} MB", flush=True)
