#!/usr/bin/env python3
"""EP2 YouTube Short: confession hook (S30 confession -> S31 received -> S32 knowing smile -> S33 tease),
vertical 720x1280 from the same keyframes, English CTA end-card (DejaVuSerif-Bold).
Straight cuts, original WITH_BGM audio segment underneath, runtime ~46s."""
import subprocess, json, os
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FPS, VW, VH = 24, 720, 1280
SC = [30,31,32,33]
sm = json.load(open(os.path.join(ROOT,'scene_map_ep2.json')))
segs = [(sm['scenes'][n-1]['start'], sm['scenes'][n-1]['end'], n) for n in SC]

CARD_SEC = 1.6
# --- CTA end card via PIL (Latin text only) ---
card = Image.new('RGB',(VW,VH),(8,8,14))
d = ImageDraw.Draw(card)
fb = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf',58)
fs = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',34)
lines=[('THE WORD THAT',fb,(255,205,60)),('STARTED THE',fb,(255,205,60)),('BHAGAVATAM',fb,(255,180,40)),
       ('',fs,(255,255,255)),('FULL STORY - EPISODE 2',fs,(235,235,235)),
       ('link in description',fs,(170,170,180)),('',fs,(255,255,255)),
       ('CREATIONS DIARY 0.25',fb,(255,255,255))]
yy=200
for t,f,c in lines:
    w = d.textlength(t,font=f); d.text(((VW-w)/2,yy),t,font=f,fill=c); yy += f.size+26
card_path='/tmp/ep2_short_card.jpg'; card.save(card_path,quality=92)

# --- scene clips: vertical center-crop with gentle push ---
inputs, chains = [], []
for start,end,n in segs:
    dur = end-start
    img = os.path.join(ROOT,'assets',f'EP02_S{n:02d}.jpg')
    inputs += ['-loop','1','-framerate',str(FPS),'-t',f"{dur:.3f}",'-i',img]
    frames = int(round(dur*FPS))
    rate = 0.06/frames
    zoom_in = (n%2==0)
    z = f"1+{rate:.7f}*on" if zoom_in else f"1.065-{rate:.7f}*on"
    chains.append(f"[{len(inputs)//8-1}:v]scale=1600:900:force_original_aspect_ratio=increase,crop=1600:900,setsar=1,"
                  f"zoompan=z='{z}':x='(iw-iw/zoom)/2':y='(ih-ih/zoom)/2':d=1:fps={FPS}:s=1800x1012,"
                  f"crop=570:1012,scale={VW}:{VH},setsar=1[v{n}]")
# CTA card trailing segment
inputs += ['-loop','1','-framerate',str(FPS),'-t',f"{CARD_SEC:.3f}",'-i',card_path]
chains.append(f"[{len(inputs)//8-1}:v]scale={VW}:{VH},setsar=1,format=yuv420p[vcard]")
cat = "".join(f"[v{n}]" for *_ ,n in segs) + "[vcard]"
fc = ";".join(chains) + ";" + f"{cat}concat=n={len(segs)+1}:v=1:a=0,"\
     "eq=contrast=1.05:saturation=1.1,format=yuv420p[vout]"

t0, t1 = segs[0][0], segs[-1][1]
audio_seg='/tmp/ep2_short_seg.wav'
subprocess.run([FF,'-y','-v','error','-ss',f"{t0-0.4:.3f}",'-t',f"{(t1-t0)+0.4:.3f}",
                '-i',os.path.join(ROOT,'EP02_WITH_BGM.mp3'),
                '-af','afade=t=in:st=0:d=0.35','-c:a','pcm_s16le',audio_seg],check=True)
out = os.path.join(ROOT,'shorts','EP02_YT_SHORT_CONFESSION.mp4')
os.makedirs(os.path.dirname(out),exist_ok=True)
cmd=[FF,'-y','-v','warning']+inputs+['-i',audio_seg,'-filter_complex',fc,
     '-map','[vout]','-map',f'{len(inputs)//8}:a?','-r',str(FPS),
     '-c:v','libx264','-preset','veryfast','-crf','22','-pix_fmt','yuv420p',
     '-c:a','aac','-b:a','160k','-shortest',out]
r=subprocess.run(cmd,capture_output=True,text=True)
if r.returncode!=0:
    print('FAIL:\n','\n'.join(r.stderr.splitlines()[-20:])); raise SystemExit(1)
p=subprocess.run([FF,'-i',out,'-hide_banner'],capture_output=True,text=True)
print('WROTE',out,[l for l in p.stderr.splitlines() if 'Duration' in l][0].split('Duration: ')[1].split(',')[0],
      f"{os.path.getsize(out)/1e6:.1f} MB")
