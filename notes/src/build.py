"""Build handwritten note images from content modules in src/content/."""
from __future__ import annotations

import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from render import Page  # noqa: E402

OUT = os.path.join(HERE, "..", "pages")


def load(path):
    spec = importlib.util.spec_from_file_location("m_" + os.path.basename(path)[:-3], path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main():
    args = sys.argv[1:]
    cdir = os.path.join(HERE, "content")
    files = sorted(f for f in os.listdir(cdir) if f.endswith(".py"))
    if args:
        files = [f for f in files if any(f.replace("v", "", 1).startswith(a.lstrip("v")) for a in args)]
    total = len([f for f in os.listdir(cdir) if f.endswith(".py")])
    for fn in files:
        mod = load(os.path.join(cdir, fn))
        meta = mod.META
        page = Page(seed=meta.get("seed", int(meta["num"]) * 13 + 5))
        page.header(meta["num"], meta["title"], meta["meta"], meta.get("tag"))
        mod.build(page)
        page.footer(meta.get("topic", "Arrays"), total)
        num = int(meta["num"])
        out = os.path.join(OUT, f"{num:02d}-{meta['slug']}.jpg")
        size = page.save(out)
        kb = os.path.getsize(out) // 1024
        print(f"[ok] {os.path.basename(out)}  {size[0]}x{size[1]}  {kb}KB")


if __name__ == "__main__":
    main()
