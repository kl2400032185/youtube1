#!/usr/bin/env python3
"""EP2 FINAL motion-grade film (v2): type-aware camera moves over the 69 keyframes,
length-neutral straight cuts on the scene map (audio sync preserved exactly),
authored black beats S06->S07 & S69 tail kept; cinematic grade (contrast/sat) +
subtle live grain. Output 1280x720/24."""
import subprocess, json, os
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, W, H = 24, 1280, 720
sm = json.load(open(os.path.join(ROOT, 'scene_map_ep2.json')))
scenes = sm['scenes']

# ---- per-scene motion grammar (strength as % push across the scene) ----
CLOSE = {2,4,12,13,21,25,26,30,31,32,37,40,44,48,51,56,58,61,68}   # emotional close-ups: very slow push
WIDE  = {1,3,5,7,8,9,11,35,36,38,47,52,54,55,59,62,64,65,66,69}  # epics/journeys: lateral drift emphasis
EPIC_RISE = {60: 0.14}                                            # the rise: strongest (still calm) push
def motion(i, frames):
    zoom = EPIC_RISE.get(i, 0.045 if i in CLOSE else (0.075 if i in WIDE else 0.06))
    rate = zoom / frames
    drift_x = ((20 if i in WIDE else 10) * (1 if i % 2 else -1)) / frames
    drift_y = ((6 if i in WIDE else 3) * (1 if i % 3 else -1)) / frames
    zoom_in = (i % 2 == 1) or i in EPIC_RISE
    z = f"1+{rate:.7f}*on" if zoom_in else f"{1+zoom+0.01:.4f}-{rate:.7f}*on"
    xp = (12.0 if i % 2 else 60.0)/100.0
    yp = (18.0 if i % 3 else 58.0)/100.0
    return (z, f"(iw-iw/zoom)*{xp:.2f}+{drift_x:.5f}*on",
               f"(ih-ih/zoom)*{yp:.2f}+{drift_y:.5f}*on")

inputs, chains = [], []
for i, s in enumerate(scenes, 1):
    dur = s['end'] - s['start']
    img = os.path.join(ROOT, 'assets', f'EP02_S{i:02d}.jpg')
    inputs += ['-loop','1','-framerate',str(FPS),'-t',f"{dur:.3f}",'-i',img]
    frames = max(24, int(round(dur*FPS)))
    z,x,y = motion(i, frames)
    v = (f"[{i-1}:v]scale=1600:900:force_original_aspect_ratio=increase,crop=1600:900,"
         f"setsar=1,zoompan=z='{z}':x='{x}':y='{y}':d=1:fps={FPS}:s={W}x{H}")
    if i == 6:  v += f",fade=t=out:st={dur-0.55:.3f}:d=0.55"
    if i in (1,7): v += ",fade=t=in:st=0:d=0.55"
    if i == 69: v += f",fade=t=out:st={dur-1.5:.3f}:d=1.5"
    chains.append(v + f"[v{i}]")

concat = "".join(f"[v{i}]" for i in range(1,70))
fc = (";".join(chains) + ";" + f"{concat}concat=n=69:v=1:a=0,"
      "eq=contrast=1.045:saturation=1.09:gamma=0.99,"
      "noise=alls=3:allf=t,format=yuv420p[vout]")

audio = os.path.join(ROOT,'EP02_WITH_BGM.mp3')
out = os.path.join(ROOT,'EP02_FINAL_FILM_720p.mp4')
cmd = [FF,'-y','-v','warning'] + inputs + ['-i',audio,
    '-filter_complex',fc,'-map','[vout]','-map','69:a?',
    '-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','25',
    '-tune','film','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest',out]
print('graph chars:',len(fc),flush=True)
r = subprocess.run(cmd,capture_output=True,text=True)
if r.returncode != 0:
    print('FAIL:\n','\n'.join(r.stderr.splitlines()[-25:])); raise SystemExit(1)
p = subprocess.run([FF,'-i',out,'-hide_banner'],capture_output=True,text=True)
print('WROTE',out,[l for l in p.stderr.splitlines() if 'Duration' in l][0].split('Duration: ')[1].split(',')[0],
      f"{os.path.getsize(out)/1e6:.1f} MB",flush=True)
