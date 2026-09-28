"""
render.py -- hand-written study-notes page renderer.

Everything is drawn with Pillow: ruled-paper background, ink-blue handwriting
(Google's Kalam), marker highlights, sketchy boxes/arrows, syntax-coloured code
blocks and hand-drawn array / matrix doodles.

A page is an object you push content blocks onto; call .save(path) at the end.
"""
from __future__ import annotations

import math
import os
import random
import re

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

# ---------------------------------------------------------------- page setup
PAGE_W = 1600
GROW_H = 6000
INIT_H = 8000
PAD_L = 158
PAD_R = 82
MARGIN_LINE_X = 118
CONTENT_W = PAGE_W - PAD_L - PAD_R
RULE_H = 34

PAPER = (250, 245, 230)
RULE = (198, 215, 233)
MARGIN_RED = (226, 158, 150)

INK = (26, 46, 92)
INK_SOFT = (72, 96, 140)
GRAY = (120, 122, 128)
RED = (186, 50, 42)
GREEN = (22, 116, 70)
PURPLE = (112, 54, 146)
ORANGE = (203, 108, 18)
TEAL = (16, 116, 130)
BROWN = (140, 92, 48)

HL_YELLOW = (255, 226, 116)
HL_PINK = (255, 176, 192)
HL_GREEN = (188, 234, 186)
HL_BLUE = (180, 214, 246)
HL_PEACH = (255, 210, 168)

BOX_FILL = (252, 249, 236)
CODE_FILL = (253, 250, 238)

FONT_FILES = {
    "hand": "Kalam-Regular.ttf",
    "handb": "Kalam-Bold.ttf",
    "title": "Caveat[wght].ttf",
    "patrick": "PatrickHand-Regular.ttf",
    "arch": "ArchitectsDaughter-Regular.ttf",
    "shadow": "ShadowsIntoLight.ttf",
    "gloria": "GloriaHallelujah.ttf",
    "mono": "CutiveMono-Regular.ttf",
    "monob": "SpaceMono-Bold.ttf",
}

_font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(key: str, size: int) -> ImageFont.FreeTypeFont:
    ck = (key, size)
    if ck not in _font_cache:
        _font_cache[ck] = ImageFont.truetype(os.path.join(ASSETS, FONT_FILES[key]), size)
    return _font_cache[ck]


def fh(f: ImageFont.FreeTypeFont) -> tuple[int, int]:
    return f.getmetrics()  # (ascent, descent)


def tw(f: ImageFont.FreeTypeFont, s: str) -> float:
    return f.getlength(s)


# ------------------------------------------------------------------ sketching
def _wobble(rng, n, amp):
    return [rng.uniform(-amp, amp) for _ in range(n)]


def sketch_line(d: ImageDraw.ImageDraw, x1, y1, x2, y2, color, width=3, rng=None, bow=2.0):
    """A slightly hand-wobbly straight line."""
    rng = rng or random.Random(0)
    n = max(4, int(math.hypot(x2 - x1, y2 - y1) / 26))
    pts = []
    for i in range(n + 1):
        t = i / n
        x = x1 + (x2 - x1) * t
        y = y1 + (y2 - y1) * t
        # perpendicular bow
        dx, dy = x2 - x1, y2 - y1
        L = math.hypot(dx, dy) or 1
        px, py = -dy / L, dx / L
        off = math.sin(t * math.pi) * rng.uniform(-bow, bow)
        pts.append((x + px * off, y + py * off))
    d.line(pts, fill=color, width=width, joint="curve")
    # tiny overshoot at the ends -- pen strokes rarely stop exactly
    d.line([(pts[0][0] - (x2 - x1) / L * 3, pts[0][1] - (y2 - y1) / L * 3), pts[0]],
           fill=color, width=width)


def sketch_rect(d, box, color, width=3, rng=None, fill=None, rough=1.8, passes=1):
    x1, y1, x2, y2 = box
    if fill is not None:
        d.rounded_rectangle(box, radius=10, fill=fill)
    rng = rng or random.Random(1)
    for _ in range(passes):
        sketch_line(d, x1, y1, x2, y1, color, width, rng, rough)
        sketch_line(d, x2, y1, x2, y2, color, width, rng, rough)
        sketch_line(d, x2, y2, x1, y2, color, width, rng, rough)
        sketch_line(d, x1, y2, x1, y1, color, width, rng, rough)


def sketch_circle(d, cx, cy, rx, ry, color, width=3, rng=None, turns=1.0):
    rng = rng or random.Random(2)
    pts = []
    N = 70
    for i in range(int(N * turns) + 1):
        a = -math.pi / 2 + 2 * math.pi * i / N
        r = 1 + rng.uniform(-0.018, 0.018)
        pts.append((cx + rx * math.cos(a) * r, cy + ry * math.sin(a) * r))
    d.line(pts, fill=color, width=width, joint="curve")


def arrow(d, p1, p2, color, width=4, rng=None, curve=0.18, head=17):
    rng = rng or random.Random(3)
    x1, y1 = p1
    x2, y2 = p2
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    cx, cy = mx - dy / L * L * curve, my + dx / L * L * curve
    pts = []
    for i in range(31):
        t = i / 30
        bx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * cx + t * t * x2
        by = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * cy + t * t * y2
        pts.append((bx + rng.uniform(-0.7, 0.7), by + rng.uniform(-0.7, 0.7)))
    d.line(pts, fill=color, width=width, joint="curve")
    ang = math.atan2(y2 - pts[-3][1], x2 - pts[-3][0])
    for da in (math.radians(152), -math.radians(152)):
        d.line([(x2, y2),
                (x2 + head * math.cos(ang + da), y2 + head * math.sin(ang + da))],
               fill=color, width=width)


def star(d, cx, cy, r, color, width=3, rng=None, points=5):
    rng = rng or random.Random(4)
    pts = []
    for i in range(points * 2 + 1):
        a = -math.pi / 2 + math.pi * i / points
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a) + rng.uniform(-1, 1),
                    cy + rr * math.sin(a) + rng.uniform(-1, 1)))
    d.polygon(pts, outline=color, fill=color)


def marker_fill(d, box, color, rng, strength=0.5, streaks=3):
    """Highlighter-pen rectangle with soft, uneven edges."""
    x1, y1, x2, y2 = box
    def blend(c, a):
        return tuple(int(PAPER[i] * (1 - a) + c[i] * a) for i in range(3))
    base = blend(color, strength)
    d.rounded_rectangle([x1, y1 + 1, x2, y2 - 1], radius=5, fill=base)
    for _ in range(streaks):
        yy1 = rng.uniform(y1, y2 - 4)
        d.rounded_rectangle([x1 + rng.uniform(-3, 4), yy1,
                             x2 + rng.uniform(-4, 3), yy1 + rng.uniform(2, 6)],
                            radius=3, fill=blend(color, strength * 0.55))


# --------------------------------------------------------------- text layout
TOKEN = re.compile(r"(\*\*.+?\*\*|`[^`]+`|==[^=]+==|!![^!]+!!|\+\+[^+]+\+\+)")


def parse_inline(text: str, base: dict) -> list[tuple[str, dict]]:
    """Parse **bold**, `code`, ==yellow==, !!pink==, ++green++ markers."""
    out = []
    for part in TOKEN.split(text):
        if not part:
            continue
        st = dict(base)
        if part.startswith("**") and part.endswith("**"):
            st["font"] = "handb"
            out.append((part[2:-2], st))
        elif part.startswith("`") and part.endswith("`"):
            st.update(font="mono", color=RED, size=st.get("msize", st["size"]))
            out.append((part[1:-1], st))
        elif part.startswith("==") and part.endswith("=="):
            st.update(hl=HL_YELLOW)
            out.append((part[2:-2], st))
        elif part.startswith("!!") and part.endswith("!!"):
            st.update(hl=HL_PINK)
            out.append((part[2:-2], st))
        elif part.startswith("++") and part.endswith("++"):
            st.update(hl=HL_GREEN)
            out.append((part[2:-2], st))
        else:
            out.append((part, st))
    return out


def _tokens(text: str) -> list[str]:
    return re.findall(r"\S+\s*|\s+", text)


def layout(segs: list[tuple[str, dict]], max_w: int):
    """Greedy word wrap of styled segments -> list of lines (list of (txt,st))."""
    lines, cur, curw = [], [], 0.0
    for text, st in segs:
        f = font(st["font"], st["size"])
        for tok in _tokens(text):
            w = tw(f, tok.rstrip())
            sp = w != tw(f, tok)
            if cur and curw + w > max_w:
                lines.append(cur)
                cur, curw = [], 0.0
                tok = tok.lstrip()
                w = tw(f, tok.rstrip())
                if not tok:
                    continue
            cur.append((tok.rstrip(), st))
            curw += w + (tw(f, " ") if sp else 0)
            if sp:
                cur.append((" ", st))
    if cur:
        lines.append(cur)
    return lines


def _merge(line):
    out = []
    for t, st in line:
        if out and out[-1][1] == st:
            out[-1] = (out[-1][0] + t, st)
        else:
            out.append((t, st))
    return out


def _blend(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))


class Page:
    def __init__(self, seed=7):
        self.rng = random.Random(seed)
        self.img = Image.new("RGB", (PAGE_W, INIT_H), PAPER)
        self.d = ImageDraw.Draw(self.img)
        self.y = 62
        self.num = ""

    # -- canvas helpers -----------------------------------------------------
    def need(self, h):
        if self.y + h > self.img.height - 40:
            nh = self.img.height + GROW_H
            ni = Image.new("RGB", (PAGE_W, nh), PAPER)
            ni.paste(self.img, (0, 0))
            self.img = ni
            self.d = ImageDraw.Draw(self.img)

    def gap(self, h=14):
        self.y += h

    # -- text ---------------------------------------------------------------
    def text_line(self, x, y, line, jitter=True, shadow=False):
        """Draw one laid-out line, rotated a hair for a hand-written feel."""
        line = _merge(line)
        if not line:
            return 0
        sizes = [st["size"] for _, st in line]
        asc, desc = fh(font(line[0][1]["font"], max(sizes)))
        h = asc + desc + 8
        w = 0.0
        for t, st in line:
            w += tw(font(st["font"], st["size"]), t)
        w = int(math.ceil(w)) + 10
        strip = Image.new("RGBA", (w + 6, h + 10), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strip)
        cx = 4
        for t, st in line:
            f = font(st["font"], st["size"])
            col = st.get("color", INK)
            if st.get("hl"):
                a, dd = fh(f)
                pad = 3
                marker_fill(sd, [cx - pad, dd + 2, cx + tw(f, t) + pad, h + 1],
                            st["hl"], self.rng, strength=0.55, streaks=2)
            sd.text((cx, 4), t, font=f, fill=col)
            if st.get("ul"):
                a2, d2 = fh(f)
                sketch_line(sd, cx, a2 + d2 + 3, cx + tw(f, t), a2 + d2 + 3,
                            col, 2, self.rng, 1.0)
            cx += tw(f, t)
        ang = self.rng.uniform(-0.45, 0.45) if jitter else 0.0
        if abs(ang) > 0.02:
            strip = strip.rotate(ang, expand=True, resample=Image.BICUBIC)
        jx = int(round(self.rng.uniform(-1.4, 1.4))) if jitter else 0
        self.img.paste(strip, (int(x) - 4 + jx, int(y) - 4), strip)
        return w

    def text_block(self, text, size=25, color=INK, fkey="hand", max_w=None,
                   indent=0, lh=1.42, bullet=None, bullet_color=None, x=None):
        """Wrapped paragraph; returns height used."""
        base = {"font": fkey, "size": size, "color": color, "msize": max(15, size - 4)}
        segs = parse_inline(text, base)
        mw = max_w or (CONTENT_W - indent)
        lines = layout(segs, mw)
        x0 = PAD_L + indent if x is None else x
        lhpx = int(size * lh)
        for i, ln in enumerate(lines):
            self.need(lhpx + 6)
            xx = x0
            if bullet is not None and i == 0:
                if bullet == "dot":
                    r = 5
                    self.d.ellipse([x0 - 26, self.y + size * 0.42 - r,
                                    x0 - 26 + 2 * r, self.y + size * 0.42 + r],
                                   fill=bullet_color or color)
                else:
                    bf = font("handb", size)
                    self.d.text((x0 - tw(bf, bullet) - 8, self.y), bullet,
                                font=bf, fill=bullet_color or color)
            self.text_line(xx, self.y, ln)
            self.y += lhpx
        return self.y

    # -- structural blocks --------------------------------------------------
    def header(self, num, title, meta, tag=None, tag_color=RED):
        self.num = num
        d = self.d
        # number badge
        cx, cy = PAD_L + 2, self.y + 34
        sketch_circle(d, cx, cy, 40, 38, tag_color, 4, self.rng, 1.08)
        sketch_circle(d, cx, cy, 40, 38, tag_color, 2, self.rng, 1.05)
        bf = font("title", 52)
        s = str(num)
        d.text((cx - tw(bf, s) / 2, cy - fh(bf)[0] / 2 - 4), s, font=bf, fill=tag_color)
        # title
        tf = font("handb", 44)
        tx = PAD_L + 62
        lines = layout([(title, {"font": "handb", "size": 44, "color": INK, "msize": 30})],
                       CONTENT_W - 62)
        for ln in lines:
            self.text_line(tx, self.y + 2, ln, jitter=False)
            self.y += 50
        # double wavy underline
        w = max(tw(tf, ln[0][0]) if ln else 0 for ln in lines)
        sketch_line(d, tx, self.y - 4, tx + min(w, CONTENT_W - 70), self.y - 4,
                    tag_color, 5, self.rng, 2.4)
        sketch_line(d, tx + 6, self.y + 4, tx + min(w, CONTENT_W - 70) - 14, self.y + 4,
                    tag_color, 3, self.rng, 2.0)
        self.y += 22
        # meta line
        mf = font("arch", 22)
        d.text((PAD_L, self.y), meta, font=mf, fill=GRAY)
        self.y += 30
        # tag in the corner
        if tag:
            f2 = font("handb", 24)
            w2 = tw(f2, tag) + 30
            box = [PAGE_W - PAD_R - w2, 12, PAGE_W - PAD_R, 56]
            strip = Image.new("RGBA", (int(w2) + 12, 60), (0, 0, 0, 0))
            sd = ImageDraw.Draw(strip)
            marker_fill(sd, [6, 8, w2 + 6, 52], tag_color, self.rng, strength=0.35)
            sd.text((21, 12), tag, font=f2, fill=(255, 255, 255) if False else INK)
            strip = strip.rotate(-3.5, expand=True, resample=Image.BICUBIC)
            self.img.paste(strip, (int(box[0]) - 6, int(box[1]) - 4), strip)
            self.d = ImageDraw.Draw(self.img)
        self.gap(16)
        # divider
        sketch_line(d, PAD_L - 20, self.y, PAGE_W - PAD_R, self.y, INK_SOFT, 2, self.rng, 1.5)
        self.gap(16)

    def h2(self, text, color=None):
        color = color or RED
        self.gap(18)
        self.need(60)
        f = font("handb", 34)
        w = tw(f, text)
        marker_fill(self.d, [PAD_L - 12, self.y - 2, PAD_L - 12 + w + 18, self.y + 40],
                    HL_YELLOW, self.rng, strength=0.42)
        self.text_line(PAD_L, self.y, [(text, {"font": "handb", "size": 34, "color": color,
                                              "msize": 22})], jitter=False)
        self.y += 44
        star(self.d, PAGE_W - PAD_R - 16, self.y - 28, 13, color, rng=self.rng)
        self.gap(6)

    def h3(self, text, color=INK):
        self.gap(10)
        self.need(46)
        f = font("handb", 27)
        self.d.polygon([(PAD_L, self.y + 5), (PAD_L, self.y + 23),
                        (PAD_L + 15, self.y + 14)], fill=RED)
        self.text_line(PAD_L + 26, self.y,
                       [(text, {"font": "handb", "size": 27, "color": color, "msize": 20})])
        self.y += 36

    def p(self, text, size=25, color=INK, indent=0, fkey="hand", lh=1.42):
        self.need(44)
        self.text_block(text, size=size, color=color, indent=indent, fkey=fkey, lh=lh)
        self.gap(4)

    def bullets(self, items, size=24, color=INK, indent=26, marker="dot", mc=None):
        for i, it in enumerate(items):
            self.need(40)
            self.text_block(it, size=size, color=color, indent=indent,
                            bullet=marker, bullet_color=mc or RED)
            self.gap(2)
        self.gap(6)

    def numbered(self, items, size=24, color=INK, indent=34, start=1):
        for i, it in enumerate(items):
            self.need(40)
            self.text_block(it, size=size, color=color, indent=indent,
                            bullet=f"{i + start})", bullet_color=RED)
            self.gap(2)
        self.gap(6)

    def quote(self, text, who="Striver"):
        self.gap(8)
        self.need(90)
        f = font("arch", 25)
        lines = layout([(text, {"font": "arch", "size": 25, "color": PURPLE, "msize": 20})],
                       CONTENT_W - 120)
        x0 = PAD_L + 46
        y0 = self.y
        h = len(lines) * 34 + 26
        # big quote glyph
        qf = font("title", 78)
        self.d.text((PAD_L - 6, y0 - 26), "“", font=qf, fill=HL_PEACH)
        for i, ln in enumerate(lines):
            self.text_line(x0, y0 + i * 34, ln)
        wf = font("hand", 20)
        self.d.text((x0 + 12, y0 + len(lines) * 34 - 2), f"— {who}", font=wf, fill=GRAY)
        sketch_line(self.d, x0 - 18, y0 - 6, x0 - 18, y0 + len(lines) * 34 + 6,
                    PURPLE, 4, self.rng, 2.0)
        self.y = y0 + h + 8

    def callout(self, kind, title, text, size=23):
        kinds = {
            "idea": (HL_YELLOW, "IDEA", RED),
            "trick": (HL_GREEN, "TRICK", GREEN),
            "gotcha": (HL_PINK, "GOTCHA!", RED),
            "note": (HL_BLUE, "NOTE", TEAL),
            "formula": (HL_PEACH, "FORMULA", ORANGE),
            "interview": (HL_PINK, "IN INTERVIEW", PURPLE),
        }
        tint, label, col = kinds.get(kind, (HL_BLUE, "NOTE", TEAL))
        self.gap(10)
        base = {"font": "hand", "size": size, "color": INK, "msize": size - 6}
        lines = layout(parse_inline(text, base), CONTENT_W - 96)
        h = max(58, len(lines) * int(size * 1.4) + 30)
        self.need(h + 12)
        y1, y2 = self.y, self.y + h
        self.d.rounded_rectangle([PAD_L, y1, PAGE_W - PAD_R, y2], radius=12,
                                 fill=_blend(PAPER, tint, 0.42))
        sketch_rect(self.d, [PAD_L, y1, PAGE_W - PAD_R, y2], col, 3, self.rng, rough=2.0)
        self.d.rounded_rectangle([PAD_L, y1, PAD_L + 9, y2], radius=4, fill=col)
        lf = font("handb", 22)
        self.d.text((PAD_L + 24, y1 + 8), label, font=lf, fill=col)
        yy = y1 + 34
        for ln in lines:
            self.text_line(PAD_L + 26, yy, ln)
            yy += int(size * 1.4)
        if title:
            tf = font("handb", 22)
            self.d.text((PAD_L + 24 + tw(lf, label) + 18, y1 + 9), title,
                        font=tf, fill=INK)
        self.y = y2 + 6

    def chips(self, items, colors=None):
        self.gap(6)
        self.need(52)
        x = PAD_L
        y = self.y
        for i, it in enumerate(items):
            col = (colors or [RED, TEAL, GREEN, PURPLE, ORANGE])[i % 5]
            f = font("handb", 23)
            w = tw(f, it) + 34
            if x + w > PAGE_W - PAD_R:
                x = PAD_L
                y += 50
                self.need(52)
            marker_fill(self.d, [x, y + 2, x + w, y + 40], col, self.rng, strength=0.33)
            sketch_rect(self.d, [x, y + 2, x + w, y + 40], col, 2, self.rng, rough=1.4)
            self.d.text((x + 17, y + 7), it, font=f, fill=col)
            x += w + 16
        self.y = y + 50

    # -- code ---------------------------------------------------------------
    KW = {
        "cpp": ("int long void return if else for while bool vector auto const new class struct "
                "using namespace std push_back size begin end swap sort true false NULL pair "
                "make_pair first second reverse unordered_map map set include").split(),
        "java": ("int long void return if else for while boolean new class public static "
                 "private List ArrayList Arrays Collections sort add get size true false null "
                 "HashMap HashSet String this").split(),
        "py": ("def return if elif else for while in not and or len range list set dict "
               "append sort sorted print True False None import as lambda max min abs "
               "float str enumerate zip reverse").split(),
        "pseudo": ("if else for while return end do then to").split(),
    }

    def code(self, lang, src, caption=None, note=None, size=20):
        lines = src.strip("\n").split("\n")
        self.gap(10)
        lh = int(size * 1.5)
        pad_top, pad_bot = 40, 18
        h = pad_top + len(lines) * lh + pad_bot
        self.need(h + 16)
        y1 = self.y
        y2 = y1 + h
        x1, x2 = PAD_L, PAGE_W - PAD_R
        strip = Image.new("RGBA", (x2 - x1 + 24, int(h) + 24), (0, 0, 0, 0))
        sd = ImageDraw.Draw(strip)
        ox, oy = 12, 12
        sd.rounded_rectangle([ox, oy, ox + (x2 - x1), oy + h], radius=10, fill=CODE_FILL)
        sketch_rect(sd, [ox, oy, ox + (x2 - x1), oy + h], INK_SOFT, 3, self.rng, rough=1.6)
        # tab
        lf = font("monob", 18)
        lab = lang.upper()
        twl = tw(lf, lab) + 26
        sd.rounded_rectangle([ox, oy - 2, ox + twl, oy + 30], radius=6, fill=INK_SOFT)
        sd.text((ox + 13, oy + 4), lab, font=lf, fill=(252, 249, 236))
        if caption:
            cf = font("arch", 21)
            sd.text((ox + twl + 16, oy + 6), caption, font=cf, fill=GRAY)
        kws = self.KW.get(lang, [])
        cf = font("mono", size)
        gf = font("mono", max(13, size - 5))
        for i, ln in enumerate(lines):
            yy = oy + pad_top + i * lh
            if i % 2 == 1:
                sd.rectangle([ox + 4, yy - 3, ox + (x2 - x1) - 4, yy + lh - 6],
                             fill=(247, 242, 226))
            num = str(i + 1)
            sd.text((ox + 10, yy), num, font=gf, fill=(186, 182, 168))
            xx = ox + 46
            for tok, col in self._lex(ln, kws, size):
                sd.text((xx, yy), tok, font=cf, fill=col)
                xx += tw(cf, tok)
        if note:
            nf = font("arch", 20)
            sd.text((ox + 14, oy + h - 24), note, font=nf, fill=GRAY)
        ang = self.rng.uniform(-0.3, 0.3)
        strip = strip.rotate(ang, expand=True, resample=Image.BICUBIC)
        self.img.paste(strip, (x1 - 12, y1 - 12), strip)
        self.d = ImageDraw.Draw(self.img)
        self.y = y2 + 8

    def _lex(self, line, kws, size):
        out = []
        i = 0
        while i < len(line):
            c = line[i]
            if c in "#/" and (c == "#" or line[i:i + 2] == "//"):
                out.append((line[i:], (96, 138, 96)))
                break
            if c in "\"'":
                j = i + 1
                while j < len(line) and line[j] != c:
                    j += 1
                out.append((line[i:j + 1], (150, 66, 120)))
                i = j + 1
                continue
            if c.isdigit():
                j = i
                while j < len(line) and (line[j].isdigit() or line[j] == "."):
                    j += 1
                out.append((line[i:j], (150, 74, 150)))
                i = j
                continue
            if c.isalpha() or c == "_":
                j = i
                while j < len(line) and (line[j].isalnum() or line[j] == "_"):
                    j += 1
                w = line[i:j]
                col = (28, 60, 150) if w in kws else INK
                out.append((w, col))
                i = j
                continue
            out.append((c, INK_SOFT))
            i += 1
        return out

    # -- tables -------------------------------------------------------------
    def table(self, headers, rows, fracs=None, size=21, title=None, hcolor=None):
        hcolor = hcolor or TEAL
        self.gap(10)
        if title:
            tf = font("handb", 24)
            self.d.text((PAD_L, self.y), title, font=tf, fill=hcolor)
            self.y += 32
        n = len(headers)
        fracs = fracs or [1 / n] * n
        widths = [int((CONTENT_W - 4) * f) for f in fracs]
        widths[-1] = CONTENT_W - sum(widths[:-1])
        xs = [PAD_L]
        for w in widths:
            xs.append(xs[-1] + w)
        hf = font("handb", size)
        cf = font("hand", size)
        # row heights
        cell_lines = []
        rh = []
        for r in [headers] + rows:
            lines = [layout(parse_inline(str(c), {"font": "hand", "size": size,
                                                  "color": INK, "msize": size - 5}),
                            widths[i] - 16) for i, c in enumerate(r)]
            cell_lines.append(lines)
            rh.append(max(len(l) for l in lines) * int(size * 1.32) + 12)
        total = sum(rh)
        self.need(total + 10)
        y = self.y
        ys = [y]
        for h in rh:
            ys.append(ys[-1] + h)
        # header marker
        marker_fill(self.d, [PAD_L - 4, y + 2, PAGE_W - PAD_R + 2, ys[1] - 2],
                    hcolor, self.rng, strength=0.30)
        for ri, row in enumerate(cell_lines):
            for ci, lines in enumerate(row):
                yy = ys[ri] + 6
                col = INK if ri else hcolor
                fk = "hand" if ri else "handb"
                for ln in lines:
                    ln = [(t, dict(st, font=fk, color=col)) for t, st in ln]
                    self.text_line(xs[ci] + 8, yy, ln)
                    yy += int(size * 1.32)
        for yy in ys:
            sketch_line(self.d, PAD_L - 6, yy, PAGE_W - PAD_R + 4, yy, INK_SOFT, 2,
                        self.rng, 1.6)
        for xx in xs:
            sketch_line(self.d, xx, y - 4, xx, ys[-1] + 2, INK_SOFT, 2, self.rng, 1.6)
        self.y = ys[-1] + 10

    # -- diagrams -----------------------------------------------------------
    def arr(self, values, marks=None, mark_color=RED, idx0=0, label=None,
            bw=68, bh=62, captions=None, cap_color=PURPLE):
        """Hand-drawn 1-D array. marks = {index: colour} to circle cells."""
        self.gap(14)
        n = len(values)
        total = n * (bw + 6)
        x0 = PAD_L + max(0, (CONTENT_W - total) // 2)
        y = self.y
        if label:
            lf = font("handb", 24)
            self.d.text((PAD_L, y - 4), label, font=lf, fill=INK_SOFT)
            y += 30
        self.need(bh + 70)
        vf = font("handb", 26)
        fnt = font("mono", 18)
        for i, v in enumerate(values):
            x = x0 + i * (bw + 6)
            self.d.rounded_rectangle([x, y, x + bw, y + bh], radius=6, fill=BOX_FILL)
            sketch_rect(self.d, [x, y, x + bw, y + bh], INK, 3, self.rng, rough=1.3)
            s = str(v)
            self.d.text((x + bw / 2 - tw(vf, s) / 2, y + bh / 2 - 17), s, font=vf, fill=INK)
            idx = str(i + idx0)
            if captions and i in captions:
                cf = font("hand", 19)
                self.d.text((x + bw / 2 - tw(cf, captions[i]) / 2, y + bh + 8),
                            captions[i], font=cf, fill=cap_color)
            else:
                self.d.text((x + bw / 2 - tw(fnt, idx) / 2, y + bh + 6), idx, font=fnt, fill=GRAY)
            if marks and i in marks:
                mc = marks[i] if isinstance(marks[i], tuple) else mark_color
                sketch_circle(self.d, x + bw / 2, y + bh / 2, bw / 2 + 9, bh / 2 + 9,
                              mc, 3, self.rng, 1.05)
        self.y = y + bh + (56 if captions else 34)

    def matrix(self, grid, marks=None, mark_color=RED, bw=62, bh=54, label=None,
               zero_color=RED):
        """Hand-drawn 2-D grid. marks = set of (r,c) to circle."""
        self.gap(14)
        rows, cols = len(grid), len(grid[0])
        total_w = cols * (bw + 6)
        x0 = PAD_L + max(0, (CONTENT_W - total_w) // 2)
        y = self.y
        if label:
            lf = font("handb", 24)
            self.d.text((PAD_L, y - 4), label, font=lf, fill=INK_SOFT)
            y += 30
        self.need(rows * (bh + 6) + 20)
        vf = font("handb", 23)
        for r in range(rows):
            for c in range(cols):
                x = x0 + c * (bw + 6)
                yy = y + r * (bh + 6)
                self.d.rounded_rectangle([x, yy, x + bw, yy + bh], radius=6, fill=BOX_FILL)
                sketch_rect(self.d, [x, yy, x + bw, yy + bh], INK, 3, self.rng, rough=1.2)
                s = str(grid[r][c])
                col = zero_color if s == "0" else INK
                self.d.text((x + bw / 2 - tw(vf, s) / 2, yy + bh / 2 - 15), s,
                            font=vf, fill=col)
                if marks and (r, c) in marks:
                    sketch_circle(self.d, x + bw / 2, yy + bh / 2, bw / 2 + 7, bh / 2 + 7,
                                  mark_color, 3, self.rng, 1.05)
        self.y = y + rows * (bh + 6) + 14

    def flow(self, items, colors=None, size=21):
        """boxes -> arrow -> boxes, single row (wraps to next row)."""
        self.gap(14)
        self.need(70)
        x = PAD_L
        y = self.y
        for i, it in enumerate(items):
            col = (colors or [TEAL, ORANGE, GREEN, PURPLE, RED])[i % 5]
            f = font("handb", size)
            lines = layout([(it, {"font": "handb", "size": size, "color": col,
                                  "msize": size - 4})], 210)
            w = max((sum(tw(font(s["font"], s["size"]), t) for t, s in ln) for ln in lines),
                    default=40) + 34
            h = len(lines) * 27 + 22
            if x + w > PAGE_W - PAD_R - 40:
                x = PAD_L
                y += h + 34
                self.need(70)
            self.d.rounded_rectangle([x, y, x + w, y + h], radius=10, fill=BOX_FILL)
            sketch_rect(self.d, [x, y, x + w, y + h], col, 3, self.rng, rough=1.4)
            yy = y + 10
            for ln in lines:
                self.text_line(x + 17, yy, ln)
                yy += 27
            if i < len(items) - 1:
                arrow(self.d, (x + w + 2, y + h / 2), (x + w + 34, y + h / 2), col, 3,
                      self.rng, curve=0.02, head=12)
            x += w + 40
        self.y = y + 64

    def dryrun(self, title, headers, rows, note=None):
        self.h3(title, color=PURPLE)
        self.table(headers, rows, size=20, hcolor=PURPLE)
        if note:
            self.p(note, size=21, color=GRAY, indent=6, fkey="arch")

    def divider(self):
        self.gap(10)
        self.need(20)
        x = PAD_L + 40
        while x < PAGE_W - PAD_R - 60:
            self.d.line([(x, self.y + 6), (x + 14, self.y - 2), (x + 28, self.y + 6)],
                        fill=(206, 200, 184), width=2, joint="curve")
            x += 34
        self.y += 22

    def footer(self, topic, total=28):
        self.gap(14)
        self.need(60)
        sketch_line(self.d, PAD_L - 20, self.y, PAGE_W - PAD_R, self.y, INK_SOFT, 2,
                    self.rng, 1.4)
        self.y += 14
        f = font("arch", 21)
        self.d.text((PAD_L, self.y), f"take U forward · Striver A2Z DSA · {topic}",
                    font=f, fill=GRAY)
        rf = font("handb", 24)
        s = f"{int(self.num)} / {total}"
        self.d.text((PAGE_W - PAD_R - tw(rf, s), self.y - 2), s, font=rf, fill=RED)
        self.y += 40

    # -- save ---------------------------------------------------------------
    def save(self, path, total=28, topic="Arrays"):
        bottom = min(int(self.y) + 30, self.img.height)
        content = self.img.crop((0, 0, PAGE_W, bottom))
        H = content.height
        # paper + rules
        bg = Image.new("RGB", (PAGE_W, H), PAPER)
        bd = ImageDraw.Draw(bg)
        for y in range(120, H, RULE_H):
            bd.line([(0, y), (PAGE_W, y)], fill=RULE, width=1)
        bd.line([(MARGIN_LINE_X, 0), (MARGIN_LINE_X, H)], fill=MARGIN_RED, width=3)
        bd.line([(MARGIN_LINE_X + 8, 0), (MARGIN_LINE_X + 8, H)], fill=MARGIN_RED, width=2)
        # grain
        tile = Image.effect_noise((PAGE_W, 900), 16).convert("L")
        grain = Image.new("L", (PAGE_W, H))
        for y in range(0, H, 900):
            grain.paste(tile, (0, y))
        grain = grain.resize((PAGE_W, H))
        bg = Image.blend(bg, Image.merge("RGB", (grain, grain, grain)), 0.06)
        # hole punches
        hd = ImageDraw.Draw(bg)
        for hy in (int(H * 0.18), int(H * 0.5), int(H * 0.82)):
            hd.ellipse([26, hy - 24, 74, hy + 24], fill=(232, 226, 208),
                       outline=(206, 198, 178), width=2)
        # composite content on top of paper
        diff = ImageChops.difference(content, Image.new("RGB", content.size, PAPER))
        mask = diff.convert("L").point(lambda v: 255 if v > 5 else 0)
        bg.paste(content, (0, 0), mask)
        # corner tape
        bg = self._tape(bg)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        if path.endswith((".jpg", ".jpeg")):
            bg.save(path, quality=92, optimize=True, progressive=True)
        else:
            bg.save(path, optimize=True)
        return bg.size

    def _tape(self, img):
        d = ImageDraw.Draw(img)
        for cx, cy, ang, w, h in ((128, 34, -32, 190, 56), (PAGE_W - 128, 34, 30, 190, 56)):
            t = Image.new("RGBA", (w, h), (246, 244, 232, 150))
            td = ImageDraw.Draw(t)
            td.rectangle([0, 0, w, h], outline=(214, 210, 192, 170), width=2)
            for i in range(0, w, 9):
                td.line([(i, 0), (i + 4, h)], fill=(226, 222, 204, 120), width=2)
            t = t.rotate(ang, expand=True, resample=Image.BICUBIC)
            img.paste(t, (cx - t.width // 2, cy - t.height // 2), t)
        return img
