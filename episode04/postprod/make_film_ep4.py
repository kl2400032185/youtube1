#!/usr/bin/env python3
"""EP4 trilingual films: pan/zoom grammar over the 56 keyframes on the Telugu scene map
(length-neutral straight cuts = audio sync preserved). Renders EP04_FILM_720p.mp4 with the
original (Telugu) master, then remuxes EN + HI dubs with atempo fit. Output 1280x720/24."""
import subprocess, json, os, re
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, W, H = 24, 1280, 720
N = 56

def dur_of(f):
    o = subprocess.run([FF,'-i',f], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', o)
    return int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))

sm = json.load(open(os.path.join(ROOT, 'scene_map_ep4.json')))
scenes = sm['scenes']
assert len(scenes) == N, f'{len(scenes)} scenes'

# ---- per-scene motion grammar ----
CLOSE = {4,6,13,18,20,22,24,29,32,36,40,44,46,48,50,51,54}        # emotional beats: very slow push
WIDE  = {1,2,3,5,7,8,9,11,12,15,17,21,23,26,28,31,33,35,38,42,52,55,56}  # epics/journeys: lateral drift
def motion(i, frames):
    zoom = 0.045 if i in CLOSE else (0.075 if i in WIDE else 0.06)
    rate = zoom / frames
    drift_x = ((20 if i in WIDE else 10) * (1 if i % 2 else -1)) / frames
    drift_y = ((6 if i in WIDE else 3) * (1 if i % 3 else -1)) / frames
    zoom_in = (i % 2 == 1)
    z = f"1+{rate:.7f}*on" if zoom_in else f"{1+zoom+0.01:.4f}-{rate:.7f}*on"
    xp = (12.0 if i % 2 else 60.0)/100.0
    yp = (18.0 if i % 3 else 58.0)/100.0
    return (z, f"(iw-iw/zoom)*{xp:.2f}+{drift_x:.5f}*on",
               f"(ih-ih/zoom)*{yp:.2f}+{drift_y:.5f}*on")

inputs, chains = [], []
for i, s in enumerate(scenes, 1):
    dur = s['end'] - s['start']
    img = os.path.join(ROOT, 'assets', f'EP04_S{i:02d}.jpg')
    inputs += ['-loop','1','-framerate',str(FPS),'-t',f"{dur:.3f}",'-i',img]
    frames = max(24, int(round(dur*FPS)))
    z,x,y = motion(i, frames)
    v = (f"[{i-1}:v]scale=1600:900:force_original_aspect_ratio=increase,crop=1600:900,"
         f"setsar=1,zoompan=z='{z}':x='{x}':y='{y}':d=1:fps={FPS}:s={W}x{H}")
    if i == 1:  v += ",fade=t=in:st=0:d=0.55"
    if i == N:  v += f",fade=t=out:st={max(0,dur-1.5):.3f}:d=1.5"
    chains.append(v + f"[v{i}]")

concat = "".join(f"[v{i}]" for i in range(1,N+1))
fc = (";".join(chains) + ";" + f"{concat}concat=n={N}:v=1:a=0,"
      "eq=contrast=1.045:saturation=1.09:gamma=0.99,"
      "noise=alls=3:allf=t,format=yuv420p[vout]")

audio = os.path.join(ROOT,'EP04_WITH_BGM.mp3')   # Telugu master = film timing base
film  = os.path.join(ROOT,'EP04_FILM_720p.mp4')
cmd = [FF,'-y','-v','warning'] + inputs + ['-i',audio,
    '-filter_complex',fc,'-map','[vout]','-map',f'{N}:a?',
    '-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','25',
    '-tune','film','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest',film]
print('graph chars:',len(fc),flush=True)
r = subprocess.run(cmd,capture_output=True,text=True)
if r.returncode != 0:
    print('FAIL:\n','\n'.join(r.stderr.splitlines()[-25:])); raise SystemExit(1)
vd = dur_of(film)
print(f'FILM ok {film} {vd:.2f}s {os.path.getsize(film)/1e6:.1f}MB',flush=True)

# Telugu dub == film (already muxed with TE master)
subprocess.run(['cp',film,os.path.join(ROOT,'EP04_DUB_TE_720p.mp4')],check=True)

# ---- remux EN / HI dubs with atempo fit ----
for lg in ('EN','HI'):
    a = os.path.join(ROOT,f'EP04_WITH_BGM_{lg}.mp3')
    o = os.path.join(ROOT,f'EP04_DUB_{lg}_720p.mp4')
    ad = dur_of(a); at = ad/vd
    af = f'atempo={at:.4f}' if abs(at-1) > 0.004 else 'anull'
    r = subprocess.run([FF,'-y','-v','error','-i',film,'-i',a,'-map','0:v:0','-map','1:a:0',
        '-c:v','copy','-af',af,'-c:a','aac','-b:a','160k','-shortest',o],capture_output=True,text=True)
    assert r.returncode == 0, r.stderr[-300:]
    print(f'{lg}: atempo {at:.4f} -> {o} {os.path.getsize(o)/1e6:.1f}MB {dur_of(o):.2f}s',flush=True)
print('ALL DONE')
