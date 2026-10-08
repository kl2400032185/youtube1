# EPISODE 3 — Asset Tracker (live)
## Status: BLUEPRINT + extractor ✅ · VO batches 5/7 ✅ (2026-10-08)
- Blueprint: `EPISODE_03_PRODUCTION_PLAN.md` — 14 sections, 68 contiguous scenes (A–G each), 8 beats, design ≈12:03; VISION grade (symbolic, never frightening); 4 Narada anchors (S02/S25/S38/S55); 2 humor beats (S17/S63); end card = exact 4 mandated lines.
- VO source of truth: `vo_script/EP03_scene_texts.json` (5,894 chars) + `EP03_VO_RECORDING_SCRIPT.md`; regen ONLY via `postprod/extract_vo.py`.
- Voices (`audio/EP03_SNN.mp3`, voice-00, 10/turn): **S01–S50 ✅** · next S51–S60.
- **Assembly recipe (locked):** tight flow everywhere; S19–S58 (ritual→meditation→vision) slot = max(blueprint design, VO+0.45s) so vision vistas/music breathe; other scenes VO+0.45s. Master floor >10:00 (projects ≈11:30). Gaps only under/after narration, never inside it.
- Font: `assets/fonts/NotoSansTelugu.ttf` (end-card Telugu text at film build).
- Pipeline: assemble_ep3.py ✅ · make_bgm_ep3.py ✅ (8 themes wired, vision anchors at S36/38/55/57/60). Todo: VO S51–S68 → 68 keyframes → preview/final films (end card = 4 exact lines via PIL+NotoSansTelugu) → short (S34→S40 hook) → upload kit.
