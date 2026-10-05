# EPISODE 1 — ASSET PRODUCTION TRACKER
Plan: EPISODE_01_PRODUCTION_PLAN.md · Runtime 13:58 · 66 scenes

## IMAGES (target: 66 scene PNGs, 16:9)
DONE: **ALL 66 SCENES** (S01-S66) + thumbnail_ep01.jpg
(S05=ASHRAMA-REF · S06=VYASA-REF · S59=NARADA-REF)
PENDING: none — images complete ✅
Folder: episode01/assets/EP01_Snn.png

## NARRATION AUDIO (target: 66 clips, Telugu narrator voice-00)
DONE: **ALL 66 SCENES** (S01-S66) — voice-00 ✅
PENDING: none — audio complete ✅
Folder: episode01/audio/EP01_Snn.mp3

## USER-ADDED IN EDITING (outside AI generation)
BGM themes T1-T5 (Plan S11) · per-scene SFX (Scene-E) · image-to-video clips (Scene-I prompts) · Telugu title/end cards · final assembly (Plan S12)

## POST-PRODUCTION (done by agent)
- BGM-mixed scene audio: `episode01/audio_bgm/EP01_Snn.mp3` — 66/66 ✅ (narration ducked over synthesized BGM; pauses capped 0.62s; 43/66 natural pace, 23 scenes ≤5% time-fit)
- Full master: `episode01/EP01_MASTER_13m58s.mp3` — 13:58, −16.5 LUFS, 192 kbps ✅
- Engine: `episode01/postprod/bgm_mix.py` (rerun to regenerate)
- Themes: T1 Mohanam flute/veena (S01–06) · T2 Kalyani veena+pad (S07–14, crest+hard stop @02:47) · T3 Shivaranjani bansuri (S15–21,30–52) · T4 Hamsadhwani ashrama warmth (S22–29, humour stingers S23/24/38/40) · T5 Mohana-Kalyani Narada (S53–66)
- Motif rule honoured: Q = 3 rising→fall 4th (S20/30/33/37/48/65), A = 4 rising (S53+), fused ONLY S64 (4 bars) → full stop @13:30; S62 held chord; S65 unresolved; S66 harmonic + final thump + clean tail.
- NOT included (editor adds per plan §11/E-items): SFX (wind, river, birds, bells…), image-to-video animation, thumbnail Telugu text overlay.

## FINAL DELIVERABLES (v2)
- `audio_final/EP01_Snn.mp3` — 66/66 per-scene clips with FULL MIX (narration + BGM + SFX) ✅
- `EP01_MASTER_13m58s.mp3` — full episode audio master (narration + 5-theme BGM + SFX per item E), −16.5 LUFS ✅
- `EP01_PREVIEW_CUT_540p.mp4` — complete 13:58 preview cut (66 images animated, Ken Burns + fades, full audio) ✅ (720p master render: `EP01_PREVIEW_CUT.mp4` in workspace, git-ignored)
- `thumbnail_ep01_text.jpg` — finished thumbnail with Telugu title text (shaping-correct) ✅
- `postprod/` — bgm_mix.py (BGM+SFX synth & mix), make_preview.py (video), make_thumbnail.py (Telugu text via uharfbuzz+freetype)
- Remaining manual: none blocking — optional polish = real image-to-video via AI tools using prompt I per scene; upload-time thumbnail = thumbnail_ep01_text.jpg.

## PATH B KICKOFF (premium launch)
- `AI_VIDEO_WORKLIST.csv` — 66 rows: scene, duration, image, clips needed, ready-to-paste image-to-video prompts ✅
- `AI_VIDEO_GUIDE.md` — tool picks (Kling/Runway/Hailuo/Luma), per-scene recipe, assembly (agent rebuilds final 1080p film when clips are returned), upload metadata ✅
- Thumbnail v2 (catchy): `thumbnail_ep01_catchy.jpg` — dramatic Vyasa/Narada art + big shaped Telugu title ✅ (base: `thumbnail_catchy_base.png`)
