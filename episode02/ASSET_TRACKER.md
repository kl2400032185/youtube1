
### Scene keyframes (COMPLETE: 69/69 ✅)
- `assets/EP02_S01–S69.jpg` — anime keyframes for animation; batches of 10/turn. DONE: ALL S01–S69 (7 batches).

### Motion-preview film (done, 2026-10-07)
- `EP02_PREVIEW_FILM_720p.mp4` — 14:48 · 1280x720/24 · 80.3MB. Ken-Burns motion over all 69 keyframes, straight cuts on scene map, WITH_BGM soundtrack, authored black-beats kept (S06->07, S69 tail fade).
- Rebuild: `postprod/make_preview_film.py` (rerunnable; swap keyframes for user-animated clips for the final grade).

### FINAL motion-grade film + Short (2026-10-07)
- `EP02_FINAL_FILM_720p.mp4` — 14:48 · 77.3MB · type-aware motion (close-ups 4.5% push / wides 7.5% / THE RISE 14%), authored black beats, contrast+sat grade, live grain. Builder: `postprod/make_film_v2.py`.
- `shorts/EP02_YT_SHORT_CONFESSION.mp4` — 44.7s vertical hook (S30 confession -> S33 tease, true-audio segment, CTA end card). Builder: `postprod/make_short_ep2.py`.
