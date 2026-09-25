#!/usr/bin/env python3
"""
Extract the narration (blockquote lines) from the Bhrugu script markdown into
TTS-ready part files split at the <!--PART n--> markers.

Rules
-----
* only lines starting with '>' are narration / dialogue
* speaker labels ('— భృగువు: ') are removed
* surrounding quotes and markdown emphasis are stripped
* one narration line per output line (blank-line separated paragraphs)
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SRC = os.path.join(ROOT, "script", "bhrugu", "bhrugu_script_te.md")
OUT = os.path.join(ROOT, "script", "bhrugu", "parts")

SPEAKER = re.compile(r"^\s*—\s*[^:：]{1,30}[:\：]\s*")
QUOTES = "\"'\u201c\u201d\u2018\u2019"
CHARS_PER_SEC = 12.3
MAX_CHARS = 880   # measured from the previous Telugu TTS batch


def clean(line):
    t = line.lstrip(">").strip()
    t = t.replace("**", "").replace("*", "").replace("`", "")
    t = SPEAKER.sub("", t)
    t = t.strip().strip(QUOTES).strip()
    return t


def main():
    text = open(SRC, encoding="utf-8").read()
    os.makedirs(OUT, exist_ok=True)
    for f in os.listdir(OUT):
        if f.endswith(".txt"):
            os.remove(os.path.join(OUT, f))

    lines = []
    for raw in text.split("\n"):
        line = raw.strip()
        if line.startswith(">"):
            t = clean(line)
            if t:
                lines.append(t)

    # auto-split into TTS-safe parts (soft max ~880 chars, never mid-line)
    parts, cur, n = [], [], 0
    for t in lines:
        if cur and n + len(t) > MAX_CHARS:
            parts.append(cur)
            cur, n = [], 0
        cur.append(t)
        n += len(t)
    if cur:
        parts.append(cur)

    total = 0
    bounds = []
    for i, lines in enumerate(parts, 1):
        body = "\n".join(lines)
        path = os.path.join(OUT, f"part{i:02d}.txt")
        open(path, "w", encoding="utf-8").write(body + "\n")
        n = len(body.replace("\n", ""))
        total += n
        est = n / CHARS_PER_SEC
        print(f"part{i:02d}: {len(lines):2d} lines, {n:5d} chars, ~{est:5.1f}s speech")
        print(f"        first: {lines[0][:60]}")
        print(f"        last : {lines[-1][-60:]}")
        bounds.append(lines[0])
    print(f"\nTOTAL: {total} chars, ~{total / CHARS_PER_SEC:.1f}s ({total / CHARS_PER_SEC / 60:.2f} min) speech")
    for i, lines in enumerate(parts, 1):
        body = "\n".join(lines).replace("\n", "")
        if len(body) > 1500:
            sys.exit(f"ERROR: part{i:02d} has {len(body)} chars (>1500)")


if __name__ == "__main__":
    main()
