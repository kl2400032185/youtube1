#!/usr/bin/env python3
"""EP5 trilingual films: engaging motion grammar over 40 keyframes (+B-variant sub-cuts
on drama beats) on the Telugu scene map (length-neutral cuts = audio sync preserved).
Renders EP05_FILM_720p.mp4 with Telugu master, then remuxes EN + HI with atempo fit.
Output 1280x720/24."""
import subprocess, json, os, re
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, W, H = 24, 1280, 720
N = 40

def dur_of(f):
    o = subprocess.run([FF,'-i',f], capture_output=True, text=True).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', o)
    return int(m.group(1))*3600 + int(m.group(2))*60 + float(m.group(3))

sm = json.load(open(os.path.join(ROOT, 'scene_map_ep5_te.json')))
scenes = sm['scenes']
assert len(scenes) == N, f'{len(scenes)} scenes'

# ---- motion grammar for Parikshit's Seven Days ----
CLOSE = {1,2,7,8,9,10,13,14,17,21,24,28,29,32,35,36}      # faces, inner beats: very slow push
WIDE  = {4,5,6,11,20,22,23,25,26,27,31,33,34,38,39}      # journeys, gatherings: lateral drift
EPIC  = {16: 0.10, 37: 0.09, 30: 0.085}                  # curse / recitation / divine light: strongest
def motion(i, frames, var=0):
    zoom = EPIC.get(i, 0.045 if i in CLOSE else (0.075 if i in WIDE else 0.06))
    if var: zoom *= 0.8                                     # B-variants move a touch less
    rate = zoom/frames
    drift_x = ((20 if i in WIDE else 10) * (1 if (i+var) % 2 else -1))/frames
    drift_y = ((6 if i in WIDE else 3) * (1 if (i+var) % 3 else -1))/frames
    zoom_in = ((i+var) % 2 == 1) or i in EPIC
    z = f"1+{rate:.7f}*on" if zoom_in else f"{1+zoom+0.01:.4f}-{rate:.7f}*on"
    xp = (12.0 if (i+var) % 2 else 60.0)/100.0
    yp = (18.0 if (i+var) % 3 else 58.0)/100.0
    return (z, f"(iw-iw/zoom)*{xp:.2f}+{drift_x:.5f}*on",
               f"(ih-ih/zoom)*{yp:.2f}+{drift_y:.5f}*on")

# ---- build parts: A-only or A->B sub-cut at 55/45 for drama beats ----
parts = []          # list of (scene_no, var, dur, img)
for i, s in enumerate(scenes, 1):
    dur = s['end'] - s['start']
    a_img = os.path.join(ROOT,'assets',f'EP05_S{i:02d}.jpg')
    b_img = os.path.join(ROOT,'assets',f'EP05_S{i:02d}B.jpg')
    if os.path.exists(b_img) and dur >= 4.0:
        parts += [(i,0,dur*0.55,a_img), (i,1,dur*0.45,b_img)]
    else:
        parts += [(i,0,dur,a_img)]

inputs, chains, labels = [], [], []
for k,(i,var,dur,img) in enumerate(parts):
    inputs += ['-loop','1','-framerate',str(FPS),'-t',f"{dur:.3f}",'-i',img]
    frames = max(12, int(round(dur*FPS)))
    z,x,y = motion(i, frames, var)
    v = (f"[{k}:v]scale=1600:900:force_original_aspect_ratio=increase,crop=1600:900,"
         f"setsar=1,zoompan=z='{z}':x='{x}':y='{y}':d=1:fps={FPS}:s={W}x{H}")
    if k == 0: v += ",fade=t=in:st=0:d=0.55"
    if k == len(parts)-1: v += f",fade=t=out:st={max(0,dur-1.5):.3f}:d=1.5"
    chains.append(v + f"[v{k}]"); labels.append(f"[v{k}]")

V = len(parts)
fc = (";".join(chains) + ";" + "".join(labels) + f"concat=n={V}:v=1:a=0,"
      "eq=contrast=1.05:saturation=1.10:gamma=0.99,"
      "noise=alls=3:allf=t,format=yuv420p[vout]")

audio = os.path.join(ROOT,'EP05_WITH_BGM_TE.mp3')
film  = os.path.join(ROOT,'EP05_FILM_720p.mp4')
cmd = [FF,'-y','-v','warning'] + inputs + ['-i',audio,
    '-filter_complex',fc,'-map','[vout]','-map',f'{V}:a?',
    '-r',str(FPS),'-c:v','libx264','-preset','veryfast','-crf','25',
    '-tune','film','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-shortest',film]
print('parts:',V,'graph chars:',len(fc),flush=True)
r = subprocess.run(cmd,capture_output=True,text=True)
if r.returncode != 0:
    print('FAIL:\n','\n'.join(r.stderr.splitlines()[-25:])); raise SystemExit(1)
vd = dur_of(film)
print(f'FILM ok {vd:.2f}s {os.path.getsize(film)/1e6:.1f}MB',flush=True)
subprocess.run(['cp',film,os.path.join(ROOT,'EP05_DUB_TE_720p.mp4')],check=True)

for lg,suf in (('EN','EN'),('HI','HI')):
    a = os.path.join(ROOT,f'EP05_WITH_BGM_{suf}.mp3')
    o = os.path.join(ROOT,f'EP05_DUB_{lg}_720p.mp4')
    ad = dur_of(a); at = ad/vd
    af = f'atempo={at:.4f}' if abs(at-1) > 0.004 else 'anull'
    r = subprocess.run([FF,'-y','-v','error','-i',film,'-i',a,'-map','0:v:0','-map','1:a:0',
        '-c:v','copy','-af',af,'-c:a','aac','-b:a','160k','-shortest',o],capture_output=True,text=True)
    assert r.returncode == 0, r.stderr[-300:]
    print(f'{lg}: atempo {at:.4f} -> {os.path.getsize(o)/1e6:.1f}MB {dur_of(o):.2f}s',flush=True)
print('ALL DONE')
