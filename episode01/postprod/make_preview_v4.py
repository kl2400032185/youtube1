#!/usr/bin/env python3
"""v4 preview: scene windows expanded to natural narration pace, clean voice."""
import os, json, subprocess, concurrent.futures as cf
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = "/home/user/youtube1/episode01"; TMP = "/tmp/vid4"; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1280, 720, 24

data = json.load(open('/tmp/scenes_v4.json'))
SC = [(s['n'], s['dur']) for s in data['scenes']]

def seg_cmd(n, dur):
    F = int(round(dur*FPS)); F1 = max(1, F-1)
    zin = n % 2 == 1
    z = "min(1.0+0.00062*on,1.24)" if zin else "max(1.24-0.00062*on,1.001)"
    dirx = 1 if (n % 4 in (1, 2)) else -1
    x = f"iw/2-(iw/zoom/2)+(on/{F1}-0.5)*0.085*{dirx}*iw/zoom"
    img = os.path.join(ROOT, "assets", f"EP01_S{n:02d}.png")
    out = os.path.join(TMP, f"s{n:02d}.mp4")
    fd = min(0.33, dur*0.10)
    vf = (f"scale=2752:1536,zoompan=z='{z}':d={F}:x='{x}':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS},"
          f"fade=t=in:st=0:d={fd:.2f},fade=t=out:st={dur-fd:.2f}:d={fd:.2f}")
    return [FF, "-y", "-v", "error", "-i", img, "-vf", vf, "-frames:v", str(F),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
            "-pix_fmt", "yuv420p", "-an", out], out

def work(job):
    cmd, out = job
    if os.path.exists(out) and os.path.getsize(out) > 10000: return out, True
    r = subprocess.run(cmd, capture_output=True)
    return out, r.returncode == 0

ok = 0
with cf.ThreadPoolExecutor(4) as ex:
    for out, good in ex.map(work, [seg_cmd(n, d) for n, d in SC]): ok += good
print(f"segments ok: {ok}/66")

lst = os.path.join(TMP, "list.txt")
with open(lst, "w") as f:
    for n, d in SC: f.write(f"file '{os.path.join(TMP, f's{n:02d}.mp4')}'\n")
subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                "-c", "copy", os.path.join(TMP, "concat.mp4")], check=True)
final = os.path.join(ROOT, "EP01_PREVIEW_CUT.mp4")
subprocess.run([FF, "-y", "-v", "error", "-i", os.path.join(TMP, "concat.mp4"),
                "-i", os.path.join(ROOT, "EP01_CLEAN_VOICE.mp3"),
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", "-shortest", final], check=True)
print("v4 preview →", final, f"{os.path.getsize(final)/1e6:.1f} MB")
