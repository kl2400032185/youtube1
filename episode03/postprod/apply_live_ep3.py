#!/usr/bin/env python3
"""EP3 LIVE ANIMATION PASS: takes EP03_BASE_1080p.mp4 and layers
- golden motes (real-world acts S1-S30, S59-S68)
- rising spark embers + breathing haze (vision S31-S58)
- film grain
in a single timeline-toggled overlay chain. Audio copied untouched.
Output: EP03_FINAL_FILM_1080p.mp4 (the animated master)."""
import subprocess, json, os, imageio_ffmpeg

FF = imageio_ffmpeg.get_ffmpeg_exe()
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sm = json.load(open(os.path.join(ROOT, 'scene_map_ep3.json')))
V0 = sm['scenes'][30]['start']   # S31 vision begins
V1 = sm['scenes'][57]['end']     # S58 vision ends
print(f'vision window {V0:.2f} -> {V1:.2f}', flush=True)

base = os.path.join(ROOT, 'EP03_BASE_1080p.mp4')
ovl = os.path.join(ROOT, 'assets', 'ovl')
out = os.path.join(ROOT, 'EP03_FINAL_FILM_1080p.mp4')

cmd = [FF, '-y', '-v', 'warning', '-i', base,
    '-stream_loop', '-1', '-framerate', '12', '-i', os.path.join(ovl, 'motes_%03d.png'),
    '-stream_loop', '-1', '-framerate', '12', '-i', os.path.join(ovl, 'sparks_%03d.png'),
    '-stream_loop', '-1', '-framerate', '12', '-i', os.path.join(ovl, 'haze_%03d.png'),
    '-filter_complex',
    (f"[1:v]fps=24,scale=1920:1080,split[m1][m2];"
     f"[2:v]fps=24,scale=1920:1080[s];"
     f"[3:v]fps=24,scale=1920:1080[h];"
     f"[0:v][m1]overlay=0:0:enable='lt(t,{V0:.2f})':eof_action=pass[t1];"
     f"[t1][s]overlay=0:0:enable='between(t,{V0:.2f},{V1:.2f})':eof_action=pass[t2];"
     f"[t2][h]overlay=0:0:enable='between(t,{V0:.2f},{V1:.2f})':eof_action=pass[t3];"
     f"[t3][m2]overlay=0:0:enable='gt(t,{V1:.2f})':eof_action=pass[t4];"
     f"[t4]noise=alls=4:allf=t,format=yuv420p[vout]"),
    '-map', '[vout]', '-map', '0:a', '-c:a', 'copy',
    '-r', '24', '-c:v', 'libx264', '-preset', 'fast', '-crf', '20',
    '-tune', 'film', '-pix_fmt', 'yuv420p', '-shortest', out]
r = subprocess.run(cmd, capture_output=True, text=True)
if r.returncode != 0:
    print('FAIL:\n', '\n'.join(r.stderr.splitlines()[-25:])); raise SystemExit(1)
p = subprocess.run([FF, '-i', out, '-hide_banner'], capture_output=True, text=True)
print('WROTE', out, [l for l in p.stderr.splitlines() if 'Duration' in l][0].split('Duration: ')[1].split(',')[0],
      f"{os.path.getsize(out)/1e6:.1f} MB", flush=True)
