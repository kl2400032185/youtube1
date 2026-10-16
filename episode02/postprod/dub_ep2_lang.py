#!/usr/bin/env python3
"""EP2 dub finisher (argv: LANG hi|en):
1) split BLK_B*.mp3 blocks into per-scene clips (proportional chars over SPEAKING scenes, snap to silence)
2) assemble 69-slot clean voice (design durations from vo_script JSON; b=None visuals -> silence slots)
3) duck-mix EP02_BGM_STEM.mp3 (duck .80 / bed .38, loudnorm) -> EP02_WITH_BGM_<L>.mp3"""
import sys, os, json, subprocess
import numpy as np, imageio_ffmpeg
LANG=sys.argv[1]; assert LANG in ('hi','en')
FF=imageio_ffmpeg.get_ffmpeg_exe()
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUD=os.path.join(ROOT,f'audio_{LANG}'); SR=44100
print('ROOT:',ROOT,'AUD:',AUD)

def decode(f):
    o=subprocess.run([FF,'-v','error','-i',f,'-f','f32le','-ac','1','-ar',str(SR),'-'],capture_output=True,check=True)
    return np.frombuffer(o.stdout,dtype=np.float32).copy()
def write_mp3(x,out,norm=True,q='2'):
    peak=max(1e-9,np.max(np.abs(x))); (x/peak*0.97).astype(np.float32).tofile('/tmp/_w.wav')
    args=[FF,'-y','-v','error','-f','f32le','-ar',str(SR),'-ac','1','-i','/tmp/_w.wav']
    if norm: args+=['-af','loudnorm=I=-16:TP=-1.5:LRA=11']
    args+=['-ar','44100','-c:a','libmp3lame','-q:a',q,out]
    r=subprocess.run(args,capture_output=True,text=True); assert r.returncode==0, r.stderr[-200:]

TX={s['n']:s for s in json.load(open(f'{ROOT}/vo_script/EP02_scene_texts_{LANG}.json',encoding='utf-8'))['scenes']}
# ---------- 1) split blocks ----------
import glob
def trim(x,thr=0.008,pad=0.25):
    e=np.abs(x); w=2205; sm=np.convolve(e,np.ones(w)/w,'same')
    idx=np.where(sm>thr)[0]
    if len(idx)==0: return x
    p=int(pad*SR); return x[max(0,idx[0]-p):min(len(x),idx[-1]+p)]
def silences(x,thr=0.012,min_gap=0.22):
    w=2205; e=np.convolve(np.abs(x),np.ones(w)/w,'same')
    mask=e<thr; out=[]; st=None
    for i,m in enumerate(mask):
        if m and st is None: st=i
        elif not m and st is not None:
            if (i-st)/SR>=min_gap: out.append((st,i))
            st=None
    return out
for blk in sorted(glob.glob(f'{AUD}/BLK_B*.mp3')):
    name=os.path.basename(blk); rng=name.split('_S')[1].replace('.mp3','')
    s0,s1=int(rng.split('-')[0]),int(rng.split('-')[1])
    speaking=[n for n in range(s0,s1+1) if TX[n]['b']]   # skip visual-only slots
    x=trim(decode(blk)); sil=silences(x)
    mids=[(a+b)//2 for a,b in sil]
    chars=np.array([len(TX[n]['b']) for n in speaking],dtype=float)
    total=len(x); bounds=[0]+list(np.cumsum(chars/chars.sum())[:-1]*total)+[total]
    # snap each inner bound to nearest silence midpoint within +-1.0s
    snapped=[bounds[0]]
    for b in bounds[1:-1]:
        cand=[m for m in mids if abs(m-b)<=SR*1.0]
        snapped.append(min(cand,key=lambda m:abs(m-b)) if cand else int(b))
    snapped.append(int(bounds[-1]))
    # enforce strictly increasing bounds with min 0.6s gaps toward proportional positions
    MIN=int(0.6*SR)
    for i in range(1,len(snapped)):
        if snapped[i] < snapped[i-1]+MIN: snapped[i]=int(max(bounds[i], snapped[i-1]+MIN))
        if snapped[i] > len(x): snapped[i]=len(x)
    for i in range(len(snapped)-2,0,-1):
        if snapped[i] > snapped[i+1]-MIN: snapped[i]=snapped[i+1]-MIN
    n_sc=len(speaking)
    assert len(snapped)==n_sc+1 and all(snapped[i+1]-snapped[i]>=MIN//2 for i in range(n_sc)), f'{name}: bad snap'
    for k,n in enumerate(speaking):
        seg=trim(x[int(snapped[k]):int(snapped[k+1])])
        write_mp3(seg,f'{AUD}/EP02_S{n:02d}.mp3',norm=False,q='3')
    print(f'{name} -> {n_sc} clips ({[round((snapped[k+1]-snapped[k])/SR,1) for k in range(n_sc)]})',flush=True)

# ---------- 2) assemble ----------
master=np.zeros(0,dtype=np.float32); smap=[]; t=0.0
for n in sorted(TX):
    s=TX[n]; f=f'{AUD}/EP02_S{n:02d}.mp3'
    if not s['b']:
        # visual-only slot: design-duration silence keeps timing aligned to the film
        slot=s['d']
        master=np.concatenate([master,np.zeros(int(slot*SR),dtype=np.float32)])
        smap.append({'n':n,'start':round(t,3),'vo_end':None,'end':round(t+slot,3),'vo_dur':0.0,'design':s['d'],'visual_only':True})
        t+=slot
    elif os.path.exists(f):
        vo=trim(decode(f)); slot=max(s['d'],len(vo)/SR+0.45)
        master=np.concatenate([master,vo,np.zeros(int((slot-len(vo)/SR)*SR),dtype=np.float32)])
        smap.append({'n':n,'start':round(t,3),'vo_end':round(t+len(vo)/SR,3),'end':round(t+slot,3),'vo_dur':round(len(vo)/SR,3),'design':s['d']})
        t+=slot
    else: raise FileNotFoundError(f)
write_mp3(master,f'{ROOT}/EP02_CLEAN_VOICE_{LANG.upper()}.mp3')
json.dump({'total':round(t,3),'scenes':smap},open(f'{ROOT}/scene_map_ep2_{LANG}.json','w'),indent=1)
print(f'clean voice {int(t//60)}:{t%60:04.1f}',flush=True)

# ---------- 3) duck-mix bed ----------
bed=decode(f'{ROOT}/EP02_BGM_STEM.mp3')
need=len(master)-len(bed)
if need>0:
    xfade=int(5*SR); loop=bed[xfade:]
    reps=int(np.ceil(need/len(loop)))
    tail=np.concatenate([loop]*reps)[:need]
    seg=np.concatenate([bed,tail]); bed=seg
bed=bed[:len(master)]
env=np.convolve(np.abs(master),np.ones(22050)/22050,'same')
mask=np.clip(env/(np.percentile(env[env>0],75)+1e-9),0,1)
g=1.0-0.80*mask; mix=master+bed*g*0.38
peak=np.max(np.abs(mix))
if peak>0.98: mix=mix/peak*0.98
write_mp3(mix,f'{ROOT}/EP02_WITH_BGM_{LANG.upper()}.mp3')
rms=np.sqrt(np.mean(mix**2))
print(f"OK EP02_WITH_BGM_{LANG.upper()}.mp3 {len(mix)/SR/60:.1f} min | RMS {20*np.log10(max(rms,1e-9)):.1f} dBFS")
