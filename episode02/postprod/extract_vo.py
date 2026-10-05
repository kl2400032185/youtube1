#!/usr/bin/env python3
"""Extract spoken text (B + C fields) per scene from EPISODE_02_PRODUCTION_PLAN.md
into EP02_scene_texts.json + EP02_VO_RECORDING_SCRIPT.md.
Single source of truth for what the narrator voice actually speaks.
Usage: python3 extract_vo.py   (run from repo root)"""
import re, json, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
PLAN = ROOT / 'episode02/EPISODE_02_PRODUCTION_PLAN.md'
OUT_J = ROOT / 'episode02/vo_script/EP02_scene_texts.json'
OUT_M = ROOT / 'episode02/vo_script/EP02_VO_RECORDING_SCRIPT.md'

def clean(field: str) -> str:
    if 'none' in field.lower()[:40]:   # check BEFORE quote extraction (directions may contain quotes)
        return ''
    field = field.replace('\\"', '"')
    q = re.findall(r'"([^"]+)"', field)
    if q:
        t = ' '.join(q)
    else:
        t = field
    t = re.sub(r'\([^()]*\)', ' ', t)      # strip stage directions like (pause)
    t = t.replace("'", '').replace('*', '')
    t = re.sub(r'^[A-Z\-]+ ?', '', t)      # drop leftover speaker label
    return re.sub(r'\s+', ' ', t).strip(' :"—-')

def main():
    s = PLAN.read_text(encoding='utf-8')
    blocks = re.split(r'^### SCENE ', s, flags=re.M)[1:]
    assert len(blocks) == 69, f'expected 69 scenes, found {len(blocks)}'
    scenes = []
    for b in blocks:
        n = int(b[:2])
        bm = re.search(r'^\*\*B\.\*\*(.+)$', b, re.M)
        cm = re.search(r'^\*\*C\.\*\*(.+)$', b, re.M)
        bt = clean(bm.group(1)) if bm else ''
        ct = clean(cm.group(1)) if cm else ''
        text = (bt + ' ' + ct).strip() if (bt and ct) else (bt or ct)
        scenes.append({'n': n, 'b': bt, 'c': ct, 'text': text})
    # verbatim mandates / normalization
    for sc in scenes:
        sc['text'] = sc['text'].lstrip('…').strip()
        sc['text'] = sc['text'].replace('అసంతృప్తికి మాత్రం… సమాధానం', 'అసంతృప్తికి మాత్రం సమాధానం')
    empty = [x['n'] for x in scenes if not x['text']]
    assert not empty, f'empty spoken text in scenes {empty}'
    OUT_J.write_text(json.dumps({'scenes': scenes}, ensure_ascii=False, indent=1), encoding='utf-8')
    with OUT_M.open('w', encoding='utf-8') as f:
        f.write('# EPISODE 2 — VOICE-OVER RECORDING SCRIPT (from blueprint §7, B+C fields)\n\n')
        for x in scenes:
            f.write(f"## S{x['n']:02d}\n{x['text']}\n\n")
    total = sum(len(x['text']) for x in scenes)
    print(f'OK: {len(scenes)} scenes, {total} spoken chars, longest {max(len(x["text"]) for x in scenes)}')

if __name__ == '__main__':
    main()
