# Telugu Funny Animation Shorts 🎬😂

A ready-to-produce series of **5 short AI-animated Telugu comedy videos** (15–30s each),
built around **voice-over + short funny Telugu dialogue**. Each episode is a self-contained
production pack: a polished copy-paste prompt for AI video tools, a time-coded Telugu
voice-over script, burned-in subtitle specs, sound cues, and YouTube Shorts metadata.

> Series rule: **all spoken sentences are Telugu.** Everyday loanwords (Wi-Fi, battery,
> charger, diet, phone…) are fine — they're natural spoken Telugu — but no English
> sentences. All on-screen subtitles are in Telugu script.

---

## 📺 Episodes

| # | Episode | Duration | The joke | File |
|---|---------|----------|----------|------|
| 1 | Wi-Fi Joke | 20s | Wi-Fi పోతే జీవితం ఆగిపోయిందట… అమ్మ సమాధానం ఒక్కటే | [episodes/01-wifi-joke.md](episodes/01-wifi-joke.md) |
| 2 | Exam Joke | 20s | పరీక్ష ముందు దేవుడికి "చదువుతా" ప్రామిస్… తర్వాత కూడా అదే ప్రామిస్ | [episodes/02-exam-joke.md](episodes/02-exam-joke.md) |
| 3 | Diet Joke | 15s | Strict diet… బిర్యానీ వాసన వరకు | [episodes/03-diet-joke.md](episodes/03-diet-joke.md) |
| 4 | Alarm Joke | 20s | 5 గంటల అలారం → "ఇంకో 5 నిమిషాలు" → 9 గంటలు | [episodes/04-alarm-joke.md](episodes/04-alarm-joke.md) |
| 5 | Phone Battery Joke | 20s | Battery 1%… ఫోన్ కాదు, లైఫ్ పోతోంది | [episodes/05-phone-battery-joke.md](episodes/05-phone-battery-joke.md) |

Subtitles for editors live in [`episodes/subtitles/`](episodes/subtitles/) as ready `.srt` files
(Telugu script, time-coded to the beat sheets).

---

## 📦 Download pack — audio · thumbnails · metadata

**▶ Open [`index.html`](index.html)** (or the local preview server) for the one-page
download pack. Every short has:

| What | Where |
|---|---|
| 🎬 **Final edited shorts (upload-ready MP4, 9:16)** | [`videos/`](videos/) |
| 🎧 Telugu VO audio (downloadable `.mp3`) | [`assets/audio/`](assets/audio/) |
| 🖼️ Thumbnail (vertical 9:16 `.jpg`) | [`assets/thumbnails/`](assets/thumbnails/) |
| 🏷️ Title · description · hashtags (copy buttons) | [`index.html`](index.html) |

The MP4s are fully edited: scene-by-scene art with Ken-Burns motion, Telugu VO on
the beat, burned-in Telugu subtitles (Noto Sans Telugu), comedy music bed + cartoon
SFX from the cue sheets. Built with `tools/build_video.py` (re-runnable).

VO cast: **voice-00** = బాబు & చైతు (auto-assigned male voice) · **voice-01** = అమ్మ ·
**voice-02** = చిన్ని. Episode 1 ships as a full merged track plus separate
Babu/Amma parts so you can time the cuts precisely.

---

## 🎨 One look, five jokes

All five shorts share a single visual identity so they feel like **one show**, not five
random clips: whimsical hand-painted Japanese animated-film aesthetic, the same recurring
cast, the same subtitle style, the same comedy music bed. The full spec is in
**[docs/STYLE-BIBLE.md](docs/STYLE-BIBLE.md)** — read it once before generating anything.

Recurring cast:

- **అమ్మ (Amma)** — deadpan mother, saree, unshakable calm
- **బాబు (Babu)** — her dramatic son, mustard t-shirt, movie-melodrama energy
- **చైతు (Chaitu)** — sleepy/dramatic college student, green hoodie (episodes 2, 4, 5)
- **చిన్ని (Chinni)** — confident young woman, pink kurta (episode 3)

---

## 🛠️ How to produce an episode

1. **Generate the video** — open the episode file, copy the *AI video generation prompt*
   (it is fully self-contained), and run it in your AI video tool (Sora, Veo, Kling,
   Runway, Pika, Hailuo…). Generate silent clips if the tool can't speak Telugu —
   the VO is added in the edit.
2. **Record the voice-over** — use the time-coded script (Telugu line + romanization +
   delivery note). Two voices cover most episodes. If your TTS supports Telugu, the
   scripts are written TTS-friendly.
3. **Add subtitles** — burn in the `.srt` file with a bold rounded Telugu font
   (Ramabhadra / Mandali / Noto Sans Telugu Bold), white with a soft dark outline.
4. **Music & SFX** — one light comedy bed under all episodes (ukulele + flute + soft
   percussion), cartoon SFX only at the marked beats. Keep music ~15–20% under VO.
5. **Upload as a YouTube Short** — 9:16, ≤60s (ours are 15–20s), title with the hook,
   description + hashtags from the episode file, `#shorts` in the title or description.

---

## ✍️ What "polished" means here

Compared to a raw one-liner prompt, every episode file adds:

- **Beat-by-beat shot list with timecodes** — AI video tools follow concrete actions
  and cuts far better than "make it funny"
- **Punchline structure** — setup → escalation → button (a final visual laugh)
- **Telugu script cleanup** — natural colloquial Telugu, consistent Telugu-script
  loanwords, plus romanization + English gloss for editors and voice talent
- **Pronunciation traps flagged** — e.g. *తినను* (won't eat) vs *తినాను* (ate)
- **Audio plan** — VO direction, music level, specific SFX cues
- **Negative list** — what the generator must avoid (English signage, extra characters…)
- **Shorts metadata** — title options, description, hashtags

Alternate punchlines are kept in each file so you can A/B test versions.

---

## 📁 Repo layout

```
youtube1/
├── README.md                      ← you are here
├── docs/
│   └── STYLE-BIBLE.md             ← shared visual/audio/character spec
└── episodes/
    ├── 01-wifi-joke.md            ← prompt + VO script + metadata
    ├── 02-exam-joke.md
    ├── 03-diet-joke.md
    ├── 04-alarm-joke.md
    ├── 05-phone-battery-joke.md
    └── subtitles/
        ├── 01-wifi-joke.te.srt
        ├── 02-exam-joke.te.srt
        ├── 03-diet-joke.te.srt
        ├── 04-alarm-joke.te.srt
        └── 05-phone-battery-joke.te.srt
```

---

*ఐదు జోక్స్… ఒక్కో జోక్ 20 సెకన్లు… నవ్వు మాత్రం ఫుల్ లెంగ్త్!* 😄
