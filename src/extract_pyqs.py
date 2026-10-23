#!/usr/bin/env python3
"""Extract every question from the 17 GATE CS papers (2016-2026), OCR fallback + cache."""
import fitz, re, json, pathlib, time
import numpy as np

SRC = pathlib.Path("/tmp/STUDY-need")
OUT = pathlib.Path("/home/user/youtube1/data")
OUT.mkdir(parents=True, exist_ok=True)
OCR_CACHE = OUT / "ocr_cache.json"
cache = json.loads(OCR_CACHE.read_text()) if OCR_CACHE.exists() else {}

BOILER = [r'Computer Science and Information Technology \(CS.*?\)',
          r'Computer Science & Information Technology \(CS.*?\)',
          r'Organizing Institute:.*', r'Organising Institute.*',
          r'Page \d+ of \d+', r'Copyright © GATE \d+', r'GATE \d+.*?IISc.*',
          r'General Aptitude.*?GA Set.*', r'^\s*\d+/\d+\s*$',
          r'CS, Set-\d+ - Copyright.*', r'^\s*GATE\s*$',
          r'^Graduate Aptitude Test in Engineering.*', r'^Correct\s*:', r'^Wrong\s*:',
          r'^Marks\s*:', r'^\d+\s*$']
BOILER_RE = [re.compile(b) for b in BOILER]

ENGINE = None
def get_engine():
    global ENGINE
    if ENGINE is None:
        from rapidocr_onnxruntime import RapidOCR
        ENGINE = RapidOCR()
    return ENGINE

def ocr_page(doc, pno, dpi=150):
    key = f"{doc.name}:{pno}"
    if key in cache: return cache[key]
    page = doc[pno]
    pix = page.get_pixmap(dpi=dpi)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
    res, _ = get_engine()(img)
    items = sorted(res, key=lambda r: (r[0][0][1], r[0][0][0])) if res else []
    lines = [it[1].strip() for it in items if it[1].strip()]
    cache[key] = lines
    return lines

P1 = re.compile(r'^Q\s*[.,]?\s*(\d{1,2})\s*[.):\-–]?\s*(.*)$')
P2 = re.compile(r'^Question\s*Number\s*:?\s*(\d{1,2})', re.I)
P3 = re.compile(r'^Q\s*[.,]?\s*No\s*[.,:]?\s*(\d{1,2})', re.I)
SECTION_HDR = re.compile(r'Q\.?\s*\d{1,2}\s*[-–]\s*Q\.?\s*\d{1,2}\s+[Cc]arry', re.I)
SECTION_HDR2 = re.compile(r'carry (one|two) mark', re.I)

def is_qstart(ln):
    if SECTION_HDR.search(ln) or SECTION_HDR2.search(ln): return None
    for pat in (P2, P3):
        m = pat.match(ln)
        if m: return int(m.group(1)), ""
    m = P1.match(ln)
    if m:
        # avoid matching things like "Q.1 to Q.5" and stray "Q. No."
        return int(m.group(1)), m.group(2).strip()
    return None

def split_blocks(pages_lines):
    blocks, cur = [], None
    for pno, lines in pages_lines:
        for ln in lines:
            r = is_qstart(ln)
            if r:
                if cur: blocks.append(cur)
                cur = {"qno": r[0], "lines": ([r[1]] if r[1] else []), "page": pno}
                continue
            if cur is not None:
                if any(b.search(ln) for b in BOILER_RE): continue
                cur["lines"].append(ln)
    if cur: blocks.append(cur)
    return blocks

def parse_options(txt):
    for m in re.finditer(r'\(A\)', txt):
        tail = txt[m.start():]
        if re.search(r'\(B\)', tail) and re.search(r'\(C\)', tail):
            stmt = txt[:m.start()].strip()
            parts = re.split(r'\(([A-D])\)', tail)
            opts = {}
            for j in range(1, len(parts) - 1, 2):
                opts[parts[j]] = re.sub(r'\s+', ' ', parts[j + 1]).strip()
            return stmt, opts
    return txt.strip(), {}

def lines_by_pos(page):
    words = page.get_text("words")
    rows = {}
    for w in words:
        y = round(w[1] / 3.0) * 3
        rows.setdefault(y, []).append((w[0], w[4]))
    return [" ".join(t for _, t in sorted(rows[y])) for y in sorted(rows)]

def extract(pdf):
    doc = fitz.open(str(pdf)); pl = []; ocr_pages = []
    for pno in range(len(doc)):
        page = doc[pno]
        words = page.get_text("words")
        lines = lines_by_pos(page) if len(words) >= 25 else [l.strip() for l in page.get_text().split("\n") if l.strip()]
        prefer_ocr = ("2017" in pdf.name) or ("2020" in pdf.name)
        q_idx = [i for i, l in enumerate(lines) if is_qstart(l)]
        thin_tail = (not q_idx) or (len(" ".join(lines[q_idx[-1]:])) < 45)
        if page.get_images() and (prefer_ocr or not q_idx or thin_tail):
            lines = ocr_page(doc, pno)
            ocr_pages.append(pno + 1)
        lines = [l.strip() for l in lines if l.strip()]
        lines = [l for l in lines if not any(b.search(l) for b in BOILER_RE)]
        pl.append((pno + 1, lines))
    doc.close()
    blocks = split_blocks(pl)
    # drop exact duplicate consecutive blocks (OCR page overlap)
    out = []
    for b in blocks:
        t = re.sub(r'\s+', ' ', " ".join(b["lines"])).strip()
        if len(t) < 8: continue
        if out and out[-1]["qno"] == b["qno"] and t[:80] == out[-1]["text"][:80]:
            continue
        out.append({"qno": b["qno"], "text": t, "page": b["page"]})
    return out, ocr_pages

def main():
    papers = sorted(SRC.glob("*Question_Paper.pdf"))
    keys = {}
    pat = re.compile(r'(?<![\d.])(\d{1,2})\s+(?:(\d)\s+)?(MCQ|MSQ|NAT)\s+(GA|CS(?:-\d)?)\s+(.+?)\s+([12])(?=\s|$)')
    for kp in sorted(SRC.glob("*Answer_Key.pdf")):
        doc = fitz.open(str(kp)); full = "\n".join(p.get_text() for p in doc); doc.close()
        ms = list(pat.finditer(re.sub(r'\s+', ' ', full)))[:65]
        keys[kp.name.replace("_Answer_Key.pdf", "")] = [
            {"type": m.group(3), "section": m.group(4), "key": m.group(5).strip(), "marks": m.group(6)} for m in ms]
    (OUT / "keys.json").write_text(json.dumps(keys, indent=1))

    result = {}
    for pdf in papers:
        prefix = pdf.name.replace("_Question_Paper.pdf", "")
        t0 = time.time()
        qs, ocr_pages = extract(pdf)
        for i, q in enumerate(qs):
            q["pos"] = i + 1
            q["stmt"], q["options"] = parse_options(q["text"])
        result[prefix] = {"file": pdf.name, "questions": qs, "ocr_pages": ocr_pages}
        OCR_CACHE.write_text(json.dumps(cache))
        (OUT / "questions.json").write_text(json.dumps(result, indent=1))
        print(f"{prefix}: {len(qs)} blocks, ocr={len(ocr_pages)}p, {time.time()-t0:.0f}s", flush=True)

if __name__ == "__main__":
    main()
