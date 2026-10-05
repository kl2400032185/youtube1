# Path B — Premium Launch Playbook (AI Image-to-Video, scene by scene)

**Goal:** turn the 66 finished PNGs into 66 animated clips, then assemble the full
13:58 film on top of the already-final audio (`audio_final/` or `EP01_MASTER_13m58s.mp3`).

Everything maps 1:1 with `AI_VIDEO_WORKLIST.csv` (66 rows):

| scene | duration_sec | image_file | clips_to_generate | image_to_video_prompt |
|-------|--------------|------------|-------------------|------------------------|

---

## 1. Pick your tool

| Tool | Best for | Notes |
|---|---|---|
| **Kling** (1.6/2.1 image-to-video) | Best motion quality for characters/faces | 5s or 10s per generation; use **Standard/Pro** as budget allows |
| **Runway Gen-4** | Good control + camera hints | 5s / 10s generations |
| **Hailuo (MiniMax)** | Budget-friendly, good motion | 6s generations (generate 2 per scene) |
| **Luma Dream Machine** | Fast drafts | 5s generations |

Any ONE tool works. Recommendation: **Kling** for faces/performance scenes (16, 18, 36, 48, 53, 59, 62, 63, 64) + any tool for atmosphere scenes (1–5, 21, 22, 37, 42, 44, 45, 50, 66).

## 2. Per-scene recipe (repeat 66×)

1. Upload `episode01/assets/EP01_Snn.png` as the start frame.
2. Paste the row's **image_to_video_prompt** from the CSV (already tuned per scene: camera, motion, what must stay locked).
3. Generate length:
   - `duration_sec ≤ 10` (4 scenes: 1, 2, 3, 15… check CSV) → **one** 10s generation, trim to duration.
   - Longer scenes → **two** generations (use **last-frame extend** feature if the tool has it, else regenerate from same image) and cut them together — or cover the remainder with a hold/slow-zoom on the still.
4. Settings: **16:9**, standard quality is fine (final film is 720p/1080p), **no text, no watermark covers**, motion strength ~0.5 (the prompts assume gentle, measured motion — this is a devotional slow burn, not an action trailer).
5. Save as `EP01_Snn.mp4` into a folder `video_clips/`.

**Total generations:** ~66–130 (avg ~2 per scene). On Kling/Runway standard plans this fits a single monthly subscription comfortably.

## 3. Assembly — two options

### Option A (recommended): send me the clips → I build the final film
When you have the 66 clips (even in batches), drop them in the repo
(`episode01/video_clips/EP01_Snn.mp4`) and tell me. I will:
- trim/extend each to its exact timeline duration (CSV col 2),
- x-fade transitions per each scene's J-item,
- grade uniformly, upscale to 1080p,
- mux the **final audio master** (narration + BGM + SFX, already done),
- deliver `EP01_FINAL_1080p.mp4` — finished film, zero editing work for you.

### Option B: DIY editing (CapCut / Premiere / DaVinci)
1. New project → timeline → import the 66 clips in scene order.
2. Trim each clip to its `duration_sec` from the CSV.
3. Add cross-dissolve 8–10 frames between scenes (hard cuts only at 14→15, 21→22, 47→48 and 64→65 — those are designed cuts).
4. Audio: drag **one** file — `EP01_MASTER_13m58s.mp3` — under the whole track. Or per-scene `audio_final/EP01_Snn.mp3` (each matches its scene length exactly).
5. Export 1080p, 24 fps, high bitrate. Subtitles optional (YouTube auto-Telugu captions work on this clean narration).
6. Upload with `thumbnail_ep01_catchy.jpg` as the thumbnail.

## 4. Quality rules (so 66 clips feel like ONE film)

- **Never** let the tool invent extra characters or change costumes — if it drifts, regenerate with the same prompt + "keep character design, costume and face identical to input image".
- Keep veena/Narada prompts as written — NARADA-REF (S59) is the locked look.
- Avoid the tool's built-in camera shake presets; our camera language is slow tracks, push-ins, arcs.
- No baked-in subtitles/text in the AI clips.

## 5. Upload metadata (ready to paste)

**Title:** అన్నీ రాసినా… వ్యాసుడికి ఎందుకు శాంతి రాలేదు? | భాగం 1
**Description:**
```
వేదాలు, పురాణాలు, ఉపనిషత్తులు — అన్నీ రాసిన వ్యాస మహర్షికి మనశ్శాంతి ఎందుకు రాలేదు?
ఆ ప్రశ్నకు సమాధానం చెప్పడానికి ఒక మహర్షి వస్తాడు… కథ ఇక్కడ మొదలవుతుంది.
(He wrote everything… but peace never came. The sage who arrives with the answer — next part.)

భాగం 2 కోసం SUBSCRIBE చేయండి 🙏
#Bhagavatam #TeluguStories #Mythology #Vyasa #Narada #భాగవతం
```
**Thumbnail:** `episode01/thumbnail_ep01_catchy.jpg`
**End screen:** subscribe at 13:43 (the S66 end card already calls for it).
