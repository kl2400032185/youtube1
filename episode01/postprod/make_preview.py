#!/usr/bin/env python3
"""EP1 preview cut: 66 scene images -> Ken Burns segments -> concat + master audio."""
import os, subprocess, concurrent.futures as cf
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = "/home/user/youtube1/episode01"
TMP  = "/tmp/vid"; os.makedirs(TMP, exist_ok=True)
W, H, FPS = 1280, 720, 24

SCENES = [(1,0,10),(2,10,20),(3,20,30),(4,30,41),(5,41,53),(6,53,66),(7,66,78),(8,78,90),
 (9,90,103),(10,103,116),(11,116,128),(12,128,140),(13,140,153),(14,153,167),(15,167,180),
 (16,180,192),(17,192,205),(18,205,218),(19,218,231),(20,231,245),(21,245,260),(22,260,272),
 (23,272,284),(24,284,296),(25,296,309),(26,309,322),(27,322,335),(28,335,348),(29,348,362),
 (30,362,375),(31,375,390),(32,390,403),(33,403,416),(34,416,429),(35,429,442),(36,442,457),
 (37,457,472),(38,472,485),(39,485,498),(40,498,511),(41,511,525),(42,525,538),(43,538,551),
 (44,551,564),(45,564,577),(46,577,590),(47,590,603),(48,603,616),(49,616,629),(50,629,643),
 (51,643,655),(52,655,667),(53,667,679),(54,679,691),(55,691,703),(56,703,715),(57,715,727),
 (58,727,739),(59,739,751),(60,751,763),(61,763,775),(62,775,787),(63,787,797),(64,797,810),
 (65,810,823),(66,823,838)]

def seg_cmd(n, s, e):
    dur = float(e - s); F = int(round(dur*FPS)); F1 = max(1, F-1)
    zin  = n % 2 == 1
    z = "min(1.0+0.00078*on,1.24)" if zin else "max(1.24-0.00078*on,1.001)"
    dirx = 1 if (n % 4 in (1, 2)) else -1
    x = f"iw/2-(iw/zoom/2)+(on/{F1}-0.5)*0.085*{dirx}*iw/zoom"
    y = "ih/2-(ih/zoom/2)"
    img = os.path.join(ROOT, "assets", f"EP01_S{n:02d}.png")
    out = os.path.join(TMP, f"s{n:02d}.mp4")
    vf = (f"scale=2752:1536,zoompan=z='{z}':d={F}:x='{x}':y='{y}':s={W}x{H}:fps={FPS},"
          f"fade=t=in:st=0:d=0.33,fade=t=out:st={dur-0.34:.2f}:d=0.33")
    return [FF, "-y", "-v", "error", "-i", img, "-vf", vf, "-frames:v", str(F),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "28",
            "-pix_fmt", "yuv420p", "-an", out], out

def work(job):
    cmd, out = job
    if os.path.exists(out) and os.path.getsize(out) > 10000: return out, True
    r = subprocess.run(cmd, capture_output=True)
    return out, r.returncode == 0

jobs = [seg_cmd(n, s, e) for n, s, e in SCENES]
done_ok = 0
with cf.ThreadPoolExecutor(4) as ex:
    for out, ok in ex.map(work, jobs):
        done_ok += ok
print(f"segments ok: {done_ok}/66")

lst = os.path.join(TMP, "list.txt")
with open(lst, "w") as f:
    for n, s, e in SCENES:
        f.write(f"file '{os.path.join(TMP, f's{n:02d}.mp4')}'\n")
subprocess.run([FF, "-y", "-v", "error", "-f", "concat", "-safe", "0", "-i", lst,
                "-c", "copy", os.path.join(TMP, "concat.mp4")], check=True)
final = os.path.join(ROOT, "EP01_PREVIEW_CUT.mp4")
subprocess.run([FF, "-y", "-v", "error", "-i", os.path.join(TMP, "concat.mp4"),
                "-i", os.path.join(ROOT, "EP01_MASTER_13m58s.mp3"),
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
                "-movflags", "+faststart", "-shortest", final], check=True)
print("preview cut →", final, f"{os.path.getsize(final)/1e6:.1f} MB")
