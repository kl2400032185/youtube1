# Style Bible — Telugu Funny Animation Shorts

One shared look, voice, and sound for all 5 episodes. Every generation prompt in
[`episodes/`](../episodes/) inlines the relevant parts of this file, but keep this
document as the single source of truth when you edit or add episodes.

---

## 🖌️ Visual style (all episodes)

> Whimsical hand-painted Japanese animated-film aesthetic: soft watercolor backgrounds,
> warm gentle lighting, painterly textures, expressive rounded characters, clean 2D
> animation with squash-and-stretch comedy timing, reaction zooms, and quick comic cuts.

- **Aspect / quality:** vertical **9:16, 1080×1920, 24–30 fps**, crisp 2D (no 3D CGI look,
  no photorealism)
- **Palette:** warm pastels — cream, teal, mustard, soft pinks; evenings in warm lamp
  amber, mornings in golden sunlight
- **World:** cozy middle-class Indian interiors — plastic chairs, steel tumblers,
  wall calendar, tube light, mandir corner, terrace water tank
- **Faces:** big readable expressions; comedy comes from **reaction shots**
  (deadpan, freeze, eye-pop, slow head-turn, dramatic zoom)
- **Motion:** smooth and simple; use exaggerated pauses — **the pause before the
  punchline is the joke**

### Consistency rules (very important for AI tools)

- Keep characters on-model: same face, hair, and wardrobe colors every episode
  (see cast below). If your tool supports reference images, generate one clean
  character sheet first and reuse it as the reference.
- Generate in **short 3–6 second shots** matching the beat sheet, then stitch in
  your editor — one 20s generation usually drifts off-model and off-story.
- Same subtitle style, same music bed, same end-card in every episode → series feel.

---

## 🎭 Cast (recurring)

| Character | Role | Design | Voice |
|---|---|---|---|
| **అమ్మ (Amma)** | Babu's mother (ep. 1) | 40s, teal-pink saree, bindi, hair in a bun | Calm, flat, deadpan — never raises her voice |
| **బాబు (Babu)** | Dramatic son at home (ep. 1) | ~18, messy hair, mustard oversized t-shirt | Young, fast, over-the-top melodrama |
| **చైతు (Chaitu)** | College student (ep. 2, 4, 5) | ~20, green hoodie, backpack, sleepy eyes | Whiny when panicked, dreamy when praying |
| **చిన్ని (Chinni)** | Young woman on a diet (ep. 3) | ~22, pink kurta, long hair | Confident… for exactly 3 seconds |

Side characters (roommate, friends, shop boy) stay generic and silent — the
punchline always belongs to the speaking character.

---

## 🎙️ Dialogue & voice-over rules

1. **Every spoken sentence is Telugu.** No English sentences anywhere (dialogue,
   narration, on-screen text).
2. **Loanwords are allowed and expected** — this is how people actually speak:
   Wi-Fi, battery, charger, diet, paper, pass, phone, minutes, life, restart.
   In Telugu subtitles write them in **Telugu script**: వైఫై, బ్యాటరీ, ఛార్జర్,
   డైట్, పేపర్, పాస్, ఫోన్, నిమిషాలు, లైఫ్.
   - Fully native swap list (if a client wants zero English): minutes → నిమిషాలు,
     life → జీవితం/ప్రాణం, paper → ప్రశ్నాపత్రం, phone → ఫోన్ (unavoidable).
3. **Register:** casual Andhra/Telangana colloquial — short lines (3–7 words),
   everyday words (*అయ్యో, రా, ఏంటి, అయితే*). No bookish Telugu.
4. **VO budget:** 20s video ≈ 12–15s of speech, 3–5 lines. Leave 1–2s silence after
   each punchline — the pause gets the laugh.
5. **Delivery:** comedy timing over accuracy speed. The deadpan character speaks
   *slower* than the panicked one — the contrast is the joke.

### Pronunciation watch-list

| Word | Say it as | Trap |
|---|---|---|
| తినను | *thinnanu* (double n, long i) = **won't eat** | *thinānu* = **I ate** — flips the joke! |
| అయితే | *ayithe* = "so what?" | don't say *aithe* |
| చెయ్యి | *cheyyi* = "do it" (casual) | not *chēyi* (hand) |
| రూటర్ | *ROO-ter* | not "rooter" with a rolled r |
| ఛార్జర్ | *CHAAR-jar* | the ఛ (cha) must aspirate |
| 9 అయిపోయిందా | *thommidhi aipoyindā* feel → "9 aipoyindā?!" | shock on **అయ్యో**, then rush |

---

## 🔊 Music & SFX (all episodes)

- **Bed:** light playful comedy music — ukulele + flute + soft percussion, ~15–20%
  under the VO. Same track family across episodes (different 15–20s cut, same mood).
- **Stops:** cut the music for 0.5s right before each punchline, then back in.
- **SFX style:** classic cartoon — boing, slide whistle, sad trombone, bonk,
  sniff-sniff, alarm buzz. Sparse: 1 SFX per beat, never a noise soup.
- **End:** tiny musical "button" (xylophone ding or cymbal tick) on the final reaction.

---

## 📝 Subtitle style (burned in)

- Font: **bold rounded Telugu** — Ramabhadra, Mandali, or Noto Sans Telugu Bold
- White text, soft dark outline (or gentle shadow), max **2 lines**
- Bottom third, inside mobile-safe margins (leave room for Shorts UI!)
- In sync with each spoken line; narration cards ("కొన్ని నిమిషాల తర్వాత…") get
  the same style, centered mid-screen on the time-card
- No English anywhere on screen

---

## 🚫 Do-not list (paste into every prompt)

- No English dialogue, no English signage or UI text
- No extra characters beyond the beat sheet, no talking animals
- No brand logos, no watermarks, no captions other than the Telugu subtitles
- No photorealism, no 3D CGI look, no slow-motion drama (this is comedy)
- No distorted faces/fingers; no gore; nothing that breaks the gentle tone
- Don't rush the ending — always finish on the button reaction
