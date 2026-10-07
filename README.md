# youtube1

---

# Creations Diary 0.25 — Production Repo (Episodes 1–2 complete)

## 🎬 EPISODE 1 — "నా ఇంత జ్ఞానం ఉన్నా… నా మనసు ఎందుకు ప్రశ్శాంతంగా లేదు?" *(UPLOADED ✅)*
- Main video live: https://youtu.be/3J7Hdg4tR3g (20:48)
- Library: `episode01/` — film cuts, 66 keyframes, audio masters, BGM engine, upload kits
- 📱 Short: `episode01/shorts/EP01_YT_SHORT_HOOK.mp4` (53.7s) + `SHORT_UPLOAD_KIT.md`
- ⚠️ Reminder: main-video YouTube **Category still set to "Autos & Vehicles"** → switch to *Entertainment*.

## 🎬 EPISODE 2 — "నారద మహర్షి చెప్పిన ఆ ఒక్క మాట… వ్యాసుడి జీవితాన్ని మార్చింది!" *(BROADCAST-READY ✅)*
Upload-day kit → `episode02/`:
| Deliverable | Path |
|---|---|
| ▶ FINAL FILM (upload this) | `episode02/EP02_FINAL_FILM_720p.mp4` · 14:48 · 720p |
| Preview cut (fallback) | `episode02/EP02_PREVIEW_FILM_720p.mp4` |
| 📱 Short "The Confession" | `episode02/shorts/EP02_YT_SHORT_CONFESSION.mp4` · 44.7s |
| Thumbnail | `episode02/assets/EP02_THUMBNAIL.jpg` |
| Title/description/chapters/tags/pinned comment | `episode02/EP02_UPLOAD_KIT.md` |
| Audio masters | `EP02_CLEAN_VOICE.mp3` · `EP02_WITH_BGM.mp3` · `EP02_BGM_STEM.mp3` |
| Production | `EPISODE_02_PRODUCTION_PLAN.md` · 69 keyframes `assets/` · 69 VO clips `audio/` · scene map · all builders in `postprod/` |

## 🔧 Pipeline (all rerunnable)
`extract_vo.py` → scene texts · `assemble_ep2_v2.py` → tight voice master · `make_bgm_ep2.py` → 6-theme ducked music · `make_preview_film.py` / `make_film_v2.py` → films · `make_short_ep2.py` → Short.

## 🎵 Music grammar (EP2)
Shivaranjani cold-open → MohanaKalyani arrival → Kalyani résumé → Hamsadhwani teaching → Desh memory-gold → Mohanam home; Q-motive [0,2,4] bansuri vs A-answer [0,2,4,7,12] veena; S30 near-naked string; S45 question reversed upward; S68 cadence; S69 heartbeat + unanswered two notes.

## ▶ Next (when user opts in)
EP3 blueprint (creation begins — teased in EP2 S69), EP2 Short series #2/#3, Path-B animated-clips swap.
