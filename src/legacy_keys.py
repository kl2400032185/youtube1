#!/usr/bin/env python3
"""Answer-key parsers for the legacy uploads.

2014 (Set-1/2/3): two-column text table  'GA 1 B 1' / 'CS 24 C 1' ...
2015 (Set-1/2/3): scanned pages where the correct option is printed green with a
                  tick; NAT answers are still in the text layer ('Correct Answer: N').
Output: data/keys_legacy.json  ->  {paper_prefix: [65 x {type, section, key, marks}]}
"""
import fitz, re, json, pathlib
import numpy as np

SRC = pathlib.Path("/tmp/STUDY-need")
OUT = pathlib.Path("/home/user/youtube1/data")
OUT.mkdir(exist_ok=True)

ORDER_PREFIX = "GATE_2016_CS_Set-1"  # not used; kept for clarity


# --------------------------------------------------------------------------- 2014
def parse_2014(path):
    """Rows are delimited by a section token ('GA'/'CS') followed by the question
    number; the last token of a row is the mark (1/2)."""
    doc = fitz.open(str(path))
    text = "\n".join(p.get_text() for p in doc)
    doc.close()
    lines = [l.strip().replace("\xa0", " ") for l in text.split("\n") if l.strip()]
    starts = [i for i in range(len(lines) - 1)
              if lines[i] in ("GA", "CS") and lines[i + 1].isdigit() and 1 <= int(lines[i + 1]) <= 65]
    rows = []
    for n, st in enumerate(starts):
        end_i = starts[n + 1] if n + 1 < len(starts) else len(lines)
        chunk = lines[st:end_i]
        chunk = [c for c in chunk if not re.search(r"GATE 2014|Answer Keys|Section Q|SESSION|Key / Range|^Marks$", c)]
        if len(chunk) < 4:
            continue
        sec, qno = chunk[0], int(chunk[1])
        marks = chunk[-1]
        if marks not in ("1", "2"):
            continue
        key = " ".join(chunk[2:-1]).strip()
        rows.append((sec, qno, key, marks))
    seen, clean = set(), []
    for sec, qno, key, marks in rows:
        if (sec, qno) in seen:
            continue
        seen.add((sec, qno))
        clean.append((sec, qno, key, marks))
    ga = sorted([r for r in clean if r[0] == "GA"], key=lambda r: r[1])
    cs = sorted([r for r in clean if r[0] == "CS"], key=lambda r: r[1])
    assert len(ga) == 10 and len(cs) == 55, (path.name, len(ga), len(cs), ga, cs[:3])
    out = []
    for sec, qno, key, marks in ga + cs:
        typ = "NAT" if ("to" in key or re.fullmatch(r"-?\d+(\.\d+)?", key)) else "MCQ"
        out.append({"type": typ, "section": sec, "key": key.replace("‐", "-"), "marks": marks})
    return out


# --------------------------------------------------------------------------- 2015
def _page_scan(doc, pno, cache, ocr):
    """OCR + green-ink detection for one key page. Cached: OCR is the slow part.
    Returns (lines, clusters) where a cluster is the y-centre of a green tick."""
    key = f"{doc.name}:{pno}"
    if key in cache:
        return cache[key]["lines"], cache[key]["clusters"]
    pix = doc[pno].get_pixmap(dpi=200)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
    res, _ = ocr(img)
    r, g, b = img[:, :, 0].astype(int), img[:, :, 1].astype(int), img[:, :, 2].astype(int)
    green = (g > 90) & (g - r > 40) & (g - b > 40)
    lines = []
    for box, txt, conf in (res or []):
        xs = [pt[0] for pt in box]; ys = [pt[1] for pt in box]
        lines.append([txt.strip(), int(min(xs)), int(min(ys)), int(max(ys))])
    lines.sort(key=lambda l: (l[2], l[1]))

    # green tick clusters: only take columns x < 40% of page width (the tick gutter)
    rs, cs = np.nonzero(green[:, : int(img.shape[1] * 0.42)])
    clusters = []
    if len(rs):
        ys = np.sort(rs)
        start = prev = ys[0]
        for y in ys[1:]:
            if y - prev > 25:
                if prev - start >= 4:
                    clusters.append(int((start + prev) / 2))
                start = y
            prev = y
        if prev - start >= 4:
            clusters.append(int((start + prev) / 2))
    cache[key] = {"lines": lines, "clusters": clusters}
    return lines, clusters


def parse_2015(path):
    """MCQ: the correct choice is printed green with a tick in the left gutter, so we
    find the green rows and match them to the numbered option lines (1..4 = A..D).
    NAT: 'Correct Answer: value' is in the text layer, in question order."""
    from rapidocr_onnxruntime import RapidOCR
    cache_path = OUT / "ocr_keys_cache2.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    ocr = RapidOCR()
    doc = fitz.open(str(path))

    text = "\n".join(p.get_text() for p in doc)
    headers = [(int(n), t) for n, t in
               re.findall(r"Question\s*Number\s*:?\s*(\d{1,2})\s*Question\s*Type\s*:?\s*(\w+)", text)]
    types = {n: t for n, t in headers}
    nat_qs = [n for n, t in headers if t == "NAT"]
    nat_vals = re.findall(r"Correct\s*Answer\s*:\s*\n?\s*([-\d.]+)", text)

    answers, last_q = {}, 0
    for pno in range(len(doc)):
        lines, clusters = _page_scan(doc, pno, cache, ocr)
        opts = []
        for t, x0, y0, y1 in lines:
            norm = re.sub(r"\s+", "", t)
            mh = re.search(r"QuestionNumber:?(\d{1,2})", norm, re.I)
            if mh:
                last_q = int(mh.group(1))
                continue
            m = re.match(r"^([1-4])\s*[.)]", t)
            if m:
                opts.append({"idx": int(m.group(1)), "y": (y0 + y1) // 2, "t": t, "q": last_q})
        # group option lines into blocks: a new block starts when the numbering restarts
        blocks, cur = [], []
        for o in opts:
            if cur and o["idx"] <= cur[-1]["idx"]:
                blocks.append(cur); cur = []
            cur.append(o)
        if cur:
            blocks.append(cur)
        for blk in blocks:
            if len(blk) < 2:
                continue
            # fit y = a*idx + b so a missing line (usually '1.') can still be located
            n = len(blk)
            mx = sum(o["idx"] for o in blk) / n
            my = sum(o["y"] for o in blk) / n
            den = sum((o["idx"] - mx) ** 2 for o in blk)
            if den == 0:
                continue
            a_ = sum((o["idx"] - mx) * (o["y"] - my) for o in blk) / den
            b_ = my - a_ * mx
            if abs(a_) < 10:
                continue
            lo, hi = b_ + a_ * 0.4, b_ + a_ * 4.6
            inside = [c for c in clusters if lo <= c <= hi]
            if not inside:
                continue
            cy = inside[0]
            idx = int(round((cy - b_) / a_))
            idx = max(1, min(4, idx))
            q = blk[0]["q"]
            if q and q not in answers:
                answers[q] = ("ABCD"[idx - 1], 1.0)
    doc.close()
    cache_path.write_text(json.dumps(cache))

    for q, v in zip(nat_qs, nat_vals):
        answers[q] = (v, 1.0)

    out = []
    for i in range(1, 66):
        typ = types.get(i, "MCQ")
        section = "GA" if i <= 10 else "CS"
        marks = "1" if (i <= 5 or 11 <= i <= 35) else "2"
        ans = answers.get(i)
        out.append({"type": typ, "section": section, "key": ans[0] if ans else "", "marks": marks})
    blanks = [i for i, e in enumerate(out, 1) if not e["key"]]
    print(f"  missing={len(blanks)} {blanks}")
    return out


def main():
    result = {}
    for p in sorted(SRC.glob("GATE_2014_CS_Set-*_Answer_Key.pdf")):
        prefix = p.name.replace("_Answer_Key.pdf", "")
        result[prefix] = parse_2014(p)
        got = sum(1 for e in result[prefix] if e["key"])
        result[prefix] = [{k: v for k, v in e.items() if k != "confidence"} for e in result[prefix]]
        print(f"{prefix}: {got}/65 keys")
    for p in sorted(SRC.glob("GATE_2015_CS_Set-*_Answer_Key.pdf")):
        prefix = p.name.replace("_Answer_Key.pdf", "")
        result[prefix] = parse_2015(p)
        got = sum(1 for e in result[prefix] if e["key"])
        result[prefix] = [{k: v for k, v in e.items() if k != "confidence"} for e in result[prefix]]
        mcq = sum(1 for e in result[prefix] if e["type"] == "MCQ" and e["key"])
        nat = sum(1 for e in result[prefix] if e["type"] == "NAT" and e["key"])
        print(f"{prefix}: {got}/65 keys (MCQ {mcq}, NAT {nat})")
    (OUT / "keys_legacy.json").write_text(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
