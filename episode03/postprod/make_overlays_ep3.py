#!/usr/bin/env python3
"""Live-animation overlay loops for EP3 (RGBA PNG sequences @480x270, 12fps):
motes  - golden dust drifting up (real-world scenes)
sparks - dense warm embers rising+pulsing (vision scenes S19+ / S31-S58)
haze   - full-frame breathing golden haze (vision glow)"""
import numpy as np, os
from PIL import Image

W, H = 480, 270
rng = np.random.default_rng(11)

def blobs(frames, n, base_a, speed_up, size_lo, size_hi, warm=1.0, blink=6):
    """n soft gaussian dots rising slowly with sinusoidal alpha pulse."""
    os.makedirs('/tmp/ovl', exist_ok=True)
    x0 = rng.uniform(0, W, n); y0 = rng.uniform(0, H, n)
    r = rng.uniform(size_lo, size_hi, n)
    ph = rng.uniform(0, 2*np.pi, n)
    spd = rng.uniform(0.4, 1.0, n) * speed_up
    yy_full = np.linspace(0, 1, H)[:, None] * H
    xx_full = np.arange(W)[None, :]
    for f in range(frames):
        t = f / 12.0
        img = np.zeros((H, W, 3), dtype=np.float32)
        for i in range(n):
            x = (x0[i] + 6*np.sin(t*0.6 + ph[i]*0.7)) % W
            y = (y0[i] - spd[i]*t*14) % H
            pulse = 0.55 + 0.45*np.sin(t*2.2 + ph[i])
            a = base_a * pulse
            xi, yi = int(x), int(y)
            rad = r[i]
            xlo, xhi = max(0, xi-int(2.2*rad)), min(W, xi+int(2.2*rad))
            ylo, yhi = max(0, yi-int(2.2*rad)), min(H, yi+int(2.2*rad))
            if xhi <= xlo or yhi <= ylo: continue
            gx = xx_full[0, xlo:xhi][None, :] - x
            gy = yy_full[ylo:yhi, 0][:, None] - y
            g = np.exp(-(gx*gx + gy*gy)/(2*rad*rad)) * a
            img[ylo:yhi, xlo:xhi, 0] += g * 1.00
            img[ylo:yhi, xlo:xhi, 1] += g * 0.82 * warm
            img[ylo:yhi, xlo:xhi, 2] += g * 0.42 * warm
        rgb = (np.clip(img, 0, 1) * 255).astype(np.uint8)
        alpha = (np.clip(img.max(axis=2) * 1.15, 0, 0.9) * 255).astype(np.uint8)
        Image.fromarray(np.dstack([rgb, rgb.max(axis=2, keepdims=True)*0+alpha[..., None]]), 'RGBA').save(f'/tmp/ovl/{name}_{f:03d}.png')
    print(name, frames, 'frames OK', flush=True)

def haze(frames=24):
    name = 'haze'
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    cx, cy = W/2, H*0.44
    d = np.sqrt(((xx-cx)/(W*0.62))**2 + ((yy-cy)/(H*0.72))**2)
    for f in range(frames):
        t = f / frames * 2*np.pi
        amp = 0.10 + 0.07*(0.5+0.5*np.sin(t))
        g = np.clip(1 - d, 0, 1)**1.6 * amp
        rgb = np.dstack([g*1.0, g*0.86, g*0.52])
        rgba = np.dstack([(rgb*255).astype(np.uint8), (np.clip(g*1.2,0,1)*255).astype(np.uint8)])
        Image.fromarray(rgba, 'RGBA').save(f'/tmp/ovl/{name}_{f:03d}.png')
    print(name, frames, 'OK', flush=True)

name = 'motes';  blobs(frames=48, n=26, base_a=0.34, speed_up=1.0, size_lo=2.2, size_hi=5.5, warm=1.0)
name = 'sparks'; blobs(frames=48, n=48, base_a=0.42, speed_up=1.9, size_lo=1.4, size_hi=3.6, warm=0.72)
haze(24)
