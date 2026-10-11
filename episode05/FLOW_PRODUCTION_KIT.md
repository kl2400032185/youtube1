# EPISODE 5 — COMPLETE SCENE-BY-SCENE VIDEO ANIMATION KIT (Google Flow hand-off)
**పరిక్షిత్తు మహారాజు కథ — TAKSHAKA'S CURSE → SEVEN DAYS → SHUKA'S ARRIVAL**

Visual style: Ghibli-inspired, hand-painted anime backgrounds, premium 2.5D cinematic movement, Indian mythological painting palette · 16:9 YouTube · family + devotional · no on-frame source language (all text is baked in post).

## HOW TO USE THIS KIT
1. Timings below are **design targets** (locked at the blueprint); the FINAL mm:ss kit refreshes auto-generated after the audio master (`make_flow_kit` step) — this version is 1:1 aligned with that and keyframes S01–S09 already exist as locked stills.
2. In Flow: upload the named keyframe → paste the scene's ANIMATION prompt → generate 4s/8s clips → trim to the scene's mm:ss window on the timeline.
3. Narration audio is the timeline master; clips must fit their windows, never the reverse.
4. Keep every character lock text pasted verbatim in any prompt where that character appears.

## GLOBAL STYLE STRING (append to every STILL/ANIM prompt)
```
premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

## CHARACTER LOCKS (paste verbatim)
- **PARIKSHIT** — King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold
- **SHAMIKA** — Elderly sage Shamika: very old, long white beard, white matted hair topknot, white tilak, faded ochre robes, thin from austerity, deeply serene
- **SHRINGI** — Shringi: teenage sage boy about fifteen, lean, saffron student robes, small topknot, sacred thread across chest, fiery intense eyes
- **GAURAMUKHA** — Gauramukha: young ashrama disciple in his twenties, simple ochre dhoti, respectful hurried run, palm-leaf message in hand
- **JANAMEJAYA** — Janamejaya: boy prince about ten, small golden crown, deep blue silk, earnest young eyes
- **SHUKA** — Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet
- **VYASA** — Elderly sage Vyasa: long white beard, long white hair in matted topknot, white tripundra tilak, saffron ochre robes, rudraksha mala, calm wise compassionate face

## MUSIC CUE MAP (BGM engine will synthesize against final master; duck 0.80 / bed 0.38 story-first standard)
- **C-ROYAL** — Hamsadhwani warm brass-string answers — palace dignity (S02-06)
- **C-HUNT** — 7-beat light tabla jog + flute runs — motion not violence (S04-06)
- **C-THIRST** — Shivaranjani sparse santoor + cicadas (S05)
- **C-SAMADHI** — deep tanpura drone + rare bell — stillness you can hear (S07-09)
- **C-CURSE** — Bhairavi: reversed plucks, thunder, low swell — dread without gore (S10-20)
- **C-FATHER** — Kalyani cello-line — a father's sorrow (S17-22)
- **C-RENOUNCE** — Mohanam flute+veena duet — twilight letting-go (S22-24)
- **C-GANGA** — Desh river-santoor sparkle + waves — the gathering (S23-30)
- **C-SHUKA** — Mohanakalyani dawn bansuri — the answer is arriving (S29-37)
- **C-END** — Mohanam home + single temple bell — Bhagavatam begins next (S37-40)

---

### S01 · 0:00.00–0:08.00 · Bridge to the Kingdom
_ridge-walk silhouette vs. distant city glow_

**NARRATION (Telugu master):** శుక మహర్షి తన జ్ఞానయాత్రలో సిద్ధమవుతుండగా — దూరంగా ఒక మహారాజ్యంలో మరో గొప్ప కథ మొదలైంది.
**DURATION:** 8.0s target

**KEYFRAME:** `episode05/assets/EP05_S01.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
Distant cinematic view: Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet a tiny figure walking a golden forest ridge at dusk, far-horizon towers and flags of a grand ancient Indian capital; he walks away from the city glow, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
STATIC wide locked frame; slow 4% push-in. Shuka's figure drifts a few glowing steps along the ridge; heat shimmer rises from the distant city; birds cross the frame left-to-right. No dialogue. Music C-SHUKA (very faint, foreshadow). SFX: evening wind, distant temple bell.
```

### S02 · 0:08.00–0:16.00 · The Dharmic King
_throne portrait_

**NARRATION (Telugu master):** పాండవుల వంశ వారసుడైన ధర్మంలో వేలుగు చేసిన గొప్ప రాజు — పరిక్షిత్తు మహారాజు.
**DURATION:** 8.0s target

**KEYFRAME:** `episode05/assets/EP05_S02.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold seated upright on an ornate golden throne, grand durbar hall, courtiers folded palms, Hastinapura palace, carved maroon pillars, oil lamps, marigold garlands, sandstone courtyard, royal standards, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow lateral dolly across courtiers to the king; lamp flames breathe; silk banners sway millimeters. Expression: composed authority, single slow blink. C-ROYAL enters with veena answer-phrase. SFX: hall ambience, one soft conch.
```

### S03 · 0:16.00–0:23.00 · Beloved Protector
_blessing subjects, boaster shrinks_

**NARRATION (Telugu master):** ప్రజలను కన్నబిడ్డల్లా చూసే ఆ ధర్మరాజు — పొగరులను మాత్రం క్షమించేవాడు కాదు.
**DURATION:** 7.0s target

**KEYFRAME:** `episode05/assets/EP05_S03.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold at palace steps, right hand raised blessing farmers mothers children; a boasting arrogant man shrinking pale at crowd edge, Hastinapura palace, carved maroon pillars, oil lamps, marigold garlands, sandstone courtyard, royal standards, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Camera starts on children's upturned faces, cranes up and back to reveal the king's blessing hand; the arrogant man edges backward out of frame — gentle comic timing. C-ROYAL warm. SFX: crowd murmur, anklets, a child's giggle.
```

### S04 · 0:23.00–0:30.50 · The Hunt
_gallop through light-shafts_

**NARRATION (Telugu master):** ఒక రోజు అటవీ వేటలో ఆ మహారాజు ఒక జింకను వెంట దూరదూరం నడిచాడు.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S04.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
Dynamic forest hunt: King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold drawing longbow astride galloping white horse, fleet golden deer leaping ahead through silver light bars, dust, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Tracking shot alongside the gallop at deer-height; hand-painted motion streaks; mane and silk stream; bowstring draws but is NOT released within clip (no violence). C-HUNT jog rhythm + flute runs. SFX: hoofbeats, deer leap whoosh, forest birds scatter.
```

### S05 · 0:30.50–0:38.00 · Thirst at the Gate
_parched arrival_

**NARRATION (Telugu master):** కలత చెందిన ఆ రాజు తీవ్ర దాహంతో — పక్కనే గల ఆశ్రమానికి చేరాడు.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S05.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
Weary King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold dismounted beside white horse at simple hermitage gate, sweat on brow, parched lips, hand at dry throat, leaning on tall bow like a staff, evening amber, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow push from gate to king's face; he swallows dryly, wipes brow; horse exhales and lowers head; dust motes fall through a light shaft. C-THIRST (sparse santoor). SFX: cicadas, saddle leather, faint hut wind-chime.
```

### S06 · 0:38.00–0:45.50 · Bush-Buster (humor)
_guard vs. hare_

**NARRATION (Telugu master):** గాలిలో కదిలిన మొక్కను జింక అనుకున్న అంగరక్షకుడు — రాజు కన్నెత్తి చూడగా నవ్వు దాచుకున్నాడు.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S06.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
Gentle comedy: royal guard in bronze helmet red plume frozen in dramatic battle crouch, spear aimed at a rustling bush, eyes wide brave-terror, tiny startled hare hopping out; King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold behind, one amused raised eyebrow, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Locked comedic frame; bush rustles 2 heavy beats; guard's knees knock (subtle); hare bounds out and stops nose-to-spear; beat; king's eyebrow rises. C-HUNT drops to playful pizzicato. SFX: tambura 'twang' on reveal, muffled snort from the horse.
```

### S07 · 0:45.50–0:52.00 · Samadhi
_stone-still sage reveal_

**NARRATION (Telugu master):** ఆశ్రమంలో శమీక మహర్షి — గాఢమైన మౌన ధ్యానంలో ఉన్నాడు.
**DURATION:** 6.5s target

**KEYFRAME:** `episode05/assets/EP05_S07.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
Elderly sage Shamika: very old, long white beard, white matted hair topknot, white tilak, faded ochre robes, thin from austerity, deeply serene motionless in absolute meditation under giant banyan, soft amber aura shimmer, falling leaves, deep holy stillness, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Extreme slow push-in on the sage's closed face; a leaf lands on his shoulder — he does not stir; aura pulses like slow breath. Cut king's approach into the far corner, small and dusty (scale of silence). C-SAMADHI tanpura drone swells. SFX: deep forest hush, single water drop.
```

### S08 · 0:52.00–0:58.50 · The Unanswered Ask
_cupped hands, silence_

**NARRATION (Telugu master):** దాహంతో విసిగిన రాజు నీరు అడిగాడు — కానీ ఎటువంటి సమాధానం రాలేదు.
**DURATION:** 6.5s target

**KEYFRAME:** `episode05/assets/EP05_S08.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold standing before meditating Elderly sage Shamika: very old, long white beard, white matted hair topknot, white tilak, faded ochre robes, thin from austerity, deeply serene whose eyes stay closed; king holds cupped empty hands raised politely, one leaf suspended mid-air between them, taut silence, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Two-beat locked shot: king's hands slowly rise, wait, tremble almost imperceptibly; sage does not move; the suspended leaf finally falls to the earth — that softness lands like a judgment. C-SAMADHI thins. SFX: heart-beat sub-pulse (barely audible).
```

### S09 · 0:58.50–1:06.00 · The Proud Flicker
_face close — dignity to anger_

**NARRATION (Telugu master):** ధ్యానస్థుడి స్థితి అర్థంకాని నిమిషంలో — ఆ రాజు గర్వం చిన్నగా మనసులోకి చేరింది.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S09.jpg` (DONE ✓)

**STILL PROMPT (image):**
```
Tight close on King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold's face: brow lowering, jaw clenching, hurt hardening to a small cold spark, ember-orange rim light on one cheekbone, blurred banyan darkening at edges, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Macro-shallow focus on the eyes; the irises seem to cool from warm brown to ember-lit; single muscle-jump under the cheek; wind dies audibly. C-SAMADHI drops to silence; one reversed-pluck premonition (Bhairavi color) at 80%. SFX: none — dead-air beat.
```

### S10 · 1:06.00–1:14.50 · The Mistake
_grey snake, bow-tip drape_

**NARRATION (Telugu master):** ఆ తర్వాత ఎరుగని తప్పు — అతడు పక్కనే ఉన్న చనిపోయిన పామును తీసి — మహర్షి మెడలో వేశాడు.
**DURATION:** 8.5s target

**KEYFRAME:** `episode05/assets/EP05_S10.jpg` (to generate)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold face clouded with wounded pride yet a seed of regret, draping a limp lifeless dull-grey snake (like a grey scarf, not frightening) held at the tip of his tall wooden bow around the shoulders of Elderly sage Shamika: very old, long white beard, white matted hair topknot, white tilak, faded ochre robes, thin from austerity, deeply serene who sits stone-still in samadhi, light gone cool at edges, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow obedient camera circling at ground level; the grey snake settles like drab fabric; king's hand hesitates mid-motion (the moment he could undo it) then withdraws; his own shadow crosses the sage. C-CURSE first low swell. SFX: dry rasp of cloth-like snake, distant crow.
```

### S11 · 1:14.50–1:21.00 · Turning Away
_exit shot_

**NARRATION (Telugu master):** ఆ తర్వాత అతడు ఆశ్రమాన్ని వదిలి వెనక్కి తిరిగాడు.
**DURATION:** 6.5s target

**KEYFRAME:** `episode05/assets/EP05_S11.jpg` (to generate)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold back three-quarter view walking out of the hermitage clearing into cooler forest shade, shoulders heavy, Elderly sage Shamika: very old, long white beard, white matted hair topknot, white tilak, faded ochre robes, thin from austerity, deeply serene small in the golden far edge, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
King walks toward camera then past it; camera does NOT follow — shame stays with the sage. Horse nickers softly as if uneasy. C-CURSE held tense under drone. SFX: boots on leaf-litter slowing once, once look-back beat (head turns, doesn't stop).
```

### S12 · 1:21.00–1:27.00 · Traveling News (visual)
_dusk ripple transition_

**NARRATION:** — (visual-only beat)
**DURATION:** 6.0s target

**KEYFRAME:** `episode05/assets/EP05_S12.jpg` (to generate)

**STILL PROMPT (image):**
```
Symbolic transition: still hermitage pond at dusk reflecting the banyan and meditating sage; a single drop rings the water; the ripple's gold turns slowly to ember-red — news traveling, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Locked frame; ripples expand in super-slow-motion; reflection trembles and cools in hue; cut on ripple crest. Pure visual beat C-CURSE shimmer. SFX: water drop, low omen rumble.
```

### S13 · 1:27.00–1:35.00 · The Friend's Whisper
_play paused_

**NARRATION (Telugu master):** శమీక మహర్షి కుమారుడు శృంగి ఆటల్లో ఉండగా — ఈ విషయమంతా వినిపించాడు ఒక స్నేహితుడు.
**DURATION:** 8.0s target

**KEYFRAME:** `episode05/assets/EP05_S13.jpg` (to generate)

**STILL PROMPT (image):**
```
Shringi: teenage sage boy about fifteen, lean, saffron student robes, small topknot, sacred thread across chest, fiery intense eyes playing aim-toss with a wooden ring near the ashrama, a fellow student leaning in whispering urgently into his ear, arm frozen mid-throw, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Handheld-but-gentle push past the whisperer onto Shringi's face; the wooden ring drops and spins twice on the ground; his eyes narrow as birds stop singing one by one. C-CURSE reversed plucks begin ticking. SFX: ring clatter, sudden hush.
```

### S14 · 1:35.00–1:42.00 · Rage of a Son
_anger montage_

**NARRATION (Telugu master):** తండ్రి అవమానం విన్న ఆ పిల్లవాడి హృదయం — ఘోరమైన కోపంతో మండిపడింది.
**DURATION:** 7.0s target

**KEYFRAME:** `episode05/assets/EP05_S14.jpg` (to generate)

**STILL PROMPT (image):**
```
Close on Shringi: teenage sage boy about fifteen, lean, saffron student robes, small topknot, sacred thread across chest, fiery intense eyes's face: nostril flare, eyes blazing copper, sacred thread catching hard light, hair stirring in hot wind, banyan leaves whipping past behind, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Quick three-beat push: chest heaving, fist closes on air, tilt to burning eyes; background animates violently though the boy is statue-still. C-CURSE full entry. SFX: fire-crack undertone, bhairavi string stab.
```

### S15 · 1:42.00–1:48.50 · The Water Touch
_ritual precision_

**NARRATION (Telugu master):** కోపంతో దివ్యజలాన్ని స్పర్శించి — ఆ పిల్లవాడు శాపం పలికాడు.
**DURATION:** 6.5s target

**KEYFRAME:** `episode05/assets/EP05_S15.jpg` (to generate)

**STILL PROMPT (image):**
```
Shringi: teenage sage boy about fifteen, lean, saffron student robes, small topknot, sacred thread across chest, fiery intense eyes kneeling at the forest stream, fingertips lifting a single scoop of glowing water cupped in both palms, determined tearless face, reflection steady, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Top-down over the cupped water shimmer; his face resolves in the reflection and hardens; camera rises with him to full height. C-CURSE drone pitch-rises quarter-tone. SFX: stream hush, shell-water droplets.
```

### S16 · 1:48.50–1:57.00 · The Curse
_raised hand, golden 7_

**NARRATION (Telugu master):** నా తండ్రిని అవమానించిన రాజుకు — ఏడు రోజుల్లో — తక్షకుడి దంశంతో మరణం తప్పదు!
**DURATION:** 8.5s target

**KEYFRAME:** `episode05/assets/EP05_S16.jpg` (to generate)

**STILL PROMPT (image):**
```
Shringi: teenage sage boy about fifteen, lean, saffron student robes, small topknot, sacred thread across chest, fiery intense eyes full figure fierce, right hand raised palm-forward heavenward, a bold golden seven-shaped bolt of light erupting from his palm across an ink-dark sky, small meditating father silhouette far-left, thumbnail-composition echo, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Frozen heroic pose; the-seven bolt blooms in three frames then crackles; embers drift down like ash; camera whip-tilt up the arm to the numeral; held two beats. C-CURSE thunders: taiko hit + Bhairavi tremolo. SFX: thunderclap, ringing aftertone.
```

### S17 · 1:57.00–2:04.50 · The Father Wakes
_pain in opened eyes_

**NARRATION (Telugu master):** ఆకాశంలో మెరుపు వెలిగింది — మౌనంలోనుండి లేచిన శమీక మహర్షి చూపు దుఃఖంతో నిండింది.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S17.jpg` (to generate)

**STILL PROMPT (image):**
```
Elderly sage Shamika: very old, long white beard, white matted hair topknot, white tilak, faded ochre robes, thin from austerity, deeply serene's eyes slowly open — not anger, only deep glistening sorrow — the grey snake still resting on his shoulders like a wilted garland, ember light dying at frame edge, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Extreme close: lashes part one millimeter per second; moisture builds not falling; the amber aura gutters out. Silence, then one soft tanpura achcha. C-FATHER begins (cello-like line). SFX: the forest lets out one long breath.
```

### S18 · 2:04.50–2:12.00 · A Father's Rebuke
_gentle thunder_

**NARRATION (Telugu master):** ఆ మహర్షి మృదువుగా హెచ్చరించాడు — ప్రజలను కాపాడే రాజును శాపం చేయటం బాలబుద్ధి అని.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S18.jpg` (to generate)

**STILL PROMPT (image):**
```
Elderly sage Shamika: very old, long white beard, white matted hair topknot, white tilak, faded ochre robes, thin from austerity, deeply serene now softly addressing downcast Shringi: teenage sage boy about fifteen, lean, saffron student robes, small topknot, sacred thread across chest, fiery intense eyes; hand raised palm-down in restraint not anger; boy's fist slowly opening as tears finally come; ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow rotation around the pair; father's mouth moves with measured words (release VO only — no lip-sync needed at this distance); boy's anger visibly melting into shame, shoulders sinking. C-FATHER warm under strings. SFX: evening insects resume.
```

### S19 · 2:12.00–2:19.00 · The Runner
_Gauramukha dispatched_

**NARRATION (Telugu master):** వెంటనే తన శిష్యుడైన గౌరముఖుడిని పంపాడు — రాజుకు ఈ వార్త చెప్పమని.
**DURATION:** 7.0s target

**KEYFRAME:** `episode05/assets/EP05_S19.jpg` (to generate)

**STILL PROMPT (image):**
```
Gauramukha: young ashrama disciple in his twenties, simple ochre dhoti, respectful hurried run, palm-leaf message in hand sprinting down the forest path toward the distant palace glow at dusk, palm-leaf clasped to his chest, torchlight streaking past raised trunks, ancient Indian forest, giant banyan and tamarind trees, thatched hermitage huts, blue mountains, golden light, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Side-tracking at run speed then bird's-eye: the messenger a small ochre comet on the darkening path, city speck far ahead. C-CURSE urgency pulse (tabla kayda). SFX: running breath, torch flapping.
```

### S20 · 2:19.00–2:25.50 · A Kingdom Holds Its Breath (visual)
_silent palace_

**NARRATION (Telugu master):** ఆ వార్త చేరగానే — హస్తినాపురం అంతా నిశ్శబ్దమైంది.
**DURATION:** 6.5s target

**KEYFRAME:** `episode05/assets/EP05_S20.jpg` (to generate)

**STILL PROMPT (image):**
```
Hastinapura courtyard in suspended evening: attendants frozen mid-gesture, oil lamps unwavering, a garland's petal falling through the hush, King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold distant on the steps hearing the message, Hastinapura palace, carved maroon pillars, oil lamps, marigold garlands, sandstone courtyard, royal standards, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow dolly past frozen attendants to the lone figure; petal falls in the foreground — the only movement in the kingdom. C fade-to-near-silence. SFX: held-breath room-tone, one far conch that stops abruptly.
```

### S21 · 2:25.50–2:34.00 · Remorse, Not Fear
_the king's true wound_

**NARRATION (Telugu master):** కానీ పరిక్షిత్తు మహారాజు — మరణం గురించి కాదు — తాను చేసిన తప్పు గురించి హృదయంతో బాధపడ్డాడు.
**DURATION:** 8.5s target

**KEYFRAME:** `episode05/assets/EP05_S21.jpg` (to generate)

**STILL PROMPT (image):**
```
Close on King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold seated at palace terrace edge at night, crown removed beside him, thumb pressing the memory of his own misdeed, eyes wet and steady — grieved, not afraid, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Very slow push; a single lamp-water reflection trembles in his unturned eye; he looks up at stars as if apologizing. C-FATHER continues, one veena note hangs. SFX: night breeze, distant Ganga-like water.
```

### S22 · 2:34.00–2:41.50 · Crown to Crown
_Janamejaya receives_

**NARRATION (Telugu master):** కుమారుడు జనమేజయుడికి రాజ్యం అప్పగించి — సింహాసనాన్ని స్వయంగా వద్దన్నేశాడు.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S22.jpg` (to generate)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold placing his own golden crown upon Janamejaya: boy prince about ten, small golden crown, deep blue silk, earnest young eyes's small lowered head in the torch-lit court; courtiers kneeling; father's hands linger on the crown, Hastinapura palace, carved maroon pillars, oil lamps, marigold garlands, sandstone courtyard, royal standards, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Over-boy-shoulder up to the king's calm face; the crown descends in three weights; torchlight flares on gold; slow pull-back reveals the whole kneeling court. C-RENOUNCE enters (flute+veena duet). SFX: torch crackle, soft collective indrawn breath.
```

### S23 · 2:41.50–2:49.50 · To the Ganga
_twilight crossing_

**NARRATION (Telugu master):** ఆయన చేరినది గంగా తీరం — మిగిలిన ఏడు దినాలను దివ్య కథకే అంకితం చేయాలని నిర్ణయించుకున్నాడు.
**DURATION:** 8.0s target

**KEYFRAME:** `episode05/assets/EP05_S23.jpg` (to generate)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold in simple white travel-dhoti walking the dark forest toward a first shimmer of wide dawn water, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current ahead, the city relinquished behind, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Wide establishing pan from black forest into dawn gold; king small center-frame grows with each cut closer; mist parts on the river. C-GANGA river-santoor sparkle begins. SFX: first morning birds, water widening.
```

### S24 · 2:49.50–2:57.50 · The Ring Fallen (humor)
_detachment beat_

**NARRATION (Telugu master):** కిరీటాన్ని కింద పెట్టేటప్పుడు రాజు నగలో చిన్న ఉంగరం దారిలో పడిపోయింది — దాన్ని కూడా తిరిగి చూడకుండా నడిచాడు.
**DURATION:** 8.0s target

**KEYFRAME:** `episode05/assets/EP05_S24.jpg` (to generate)

**STILL PROMPT (image):**
```
Ground-level close: King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold's hand setting the heavy golden crown onto white sand; a small gold ring slips from his finger rolling in a slow circle and lying still; his bare feet step past it without pause, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Locked ground shot; ring rolls, wobbles, dies; foot enters frame, passes; camera tilts up to find the king already several steps gone and not looking back — tiny perfect comedy of detachment. C-RENOUNCE sustained. SFX: soft gold-on-sand fizz, river wash.
```

### S25 · 2:57.50–3:05.00 · The Sages Gather
_arrival montage_

**NARRATION (Telugu master):** ఆ గంగా తీరానికి — భారతదేశంలోని గొప్ప మహర్షులు ఒక్కొక్కరుగా చేరుకొన్నారు.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S25.jpg` (to generate)

**STILL PROMPT (image):**
```
Reverent montage wide of the riverbank: saffron sages arriving from three directions on foot, some with staffs, some by simple boat, marigold boats of light on the water, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Three-layered cross-dissolve of arrivals at different hours, each sage's shadow walking ahead of them like blessing the ground; petals slide downstream continuously. C-GANGA + temple bell. SFX: oar strokes, staff taps, namaskara murmurs.
```

### S26 · 3:05.00–3:12.50 · Atri — Vasishtha — Bharadvaja — Gautama
_four faces_

**NARRATION (Telugu master):** అత్రి మహర్షి… వశిష్ఠ మహర్షి… భరద్వాజ మహర్షి… గౌతమ మహర్షి — జ్ఞానంలో భారతదేశమే ఒకచోట చేరినట్లైంది.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S26.jpg` (to generate)

**STILL PROMPT (image):**
```
Four gentle portrait plates in sequence: ancient sages Atri (dark serene), Vasishtha (white-robed luminous), Bharadvaja (broad-shouldered calm), Gautama (quiet-eyed ascetic), each against the river's gold, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Four one-second portrait holds with slow iris-open between; wind reads over each still face; no titles needed (VO names them). C-GANGA motif cycles. SFX: conch per portrait, soft.
```

### S27 · 3:12.50–3:18.50 · Maha Sabha
_assembly wide_

**NARRATION (Telugu master):** గంగా తీరం అంతటా మహర్షుల మహా సభగా మారిపోయింది.
**DURATION:** 6.0s target

**KEYFRAME:** `episode05/assets/EP05_S27.jpg` (to generate)

**STILL PROMPT (image):**
```
Epic wide from water toward bank: hundreds of saffron-robed sages seated in concentric leaf-mat arcs facing a simple raised seat of kusha grass, marigold petals drifting the full frame, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow aerial drift along the arcs revealing scale; a hundred breathing stillness; ghee-lamps kindle row by row. C-GANGA fullest bloom + mridangam whisper. SFX: river of quiet murmur.
```

### S28 · 3:18.50–3:25.00 · The King Bows
_humility pays its seat_

**NARRATION (Telugu master):** పరిక్షిత్తు మహారాజు సభ్యులందరికీ నమస్కరించి — గాఢమైన ప్రశ్న వేశాడు.
**DURATION:** 6.5s target

**KEYFRAME:** `episode05/assets/EP05_S28.jpg` (to generate)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold in simple white, crownless, palms joined, deep bowing with forehead nearly to the sand before the seated assembly, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Low camera behind the king's bowed back looking up at the sea of sages; the bow holds; he rises with the question forming in his settled face. C thins to tanpura. SFX: fabric, breath, river.
```

### S29 · 3:25.00–3:33.00 · The Question
_world's softest thunder_

**NARRATION (Telugu master):** మహాత్ములారా — మరణం సమీపంలో ఉన్న మనిషి — మిగిలిన దినాలు ఏ మార్గంలో గడపాలి?
**DURATION:** 8.0s target

**KEYFRAME:** `episode05/assets/EP05_S29.jpg` (to generate)

**STILL PROMPT (image):**
```
Intense reverent close on King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold seated palms-joined before the assembly, eyes clear as lamps asking the great question; sages' faces leaning in at soft focus behind, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Push in to eyes on the question's final word; one petal crosses the frame and stops — time has walked into a circle. C-SHUKA arises faint first time (dawn bansuri). SFX: hush, heartbeat resolves to river.
```

### S30 · 3:33.00–3:39.50 · Sacred Silence (visual)
_silence montage_

**NARRATION:** — (visual-only beat)
**DURATION:** 6.5s target

**KEYFRAME:** `episode05/assets/EP05_S30.jpg` (to generate)

**STILL PROMPT (image):**
```
Symbolic silent beat: golden river shimmer, closed lotus buds, meditating faces in warm dusk glow, one oil lamp unwavering, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Four gentle dissolves; nobody speaks; the lotus bud breathes but does not yet open. TOTAL hush — music does not intrude. SFX: only river and a soft temple bell, once.
```

### S31 · 3:39.50–3:47.50 · A Light on the Path
_distant arrival_

**NARRATION (Telugu master):** ఆ క్షణంలో — దారి అంచున ఒక అపూర్వ కాంతి కనిపించింది — ఒక శాంతమైన యువరూపం నడుస్తున్నది.
**DURATION:** 8.0s target

**KEYFRAME:** `episode05/assets/EP05_S31.jpg` (to generate)

**STILL PROMPT (image):**
```
Dawn edge view down the riverbank path: a small luminous figure walking out of morning gold, light seeming to walk ahead of him, sages' heads beginning to turn one by one, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Long-lens path shot; the figure shimmers between trees; turning heads ripple through the assembly like wind over grain. C-SHUKA bansuri rises. SFX: bare feet on wet sand, each step softly glowing.
```

### S32 · 3:47.50–3:56.00 · Shuka Revealed
_eighteen and endless_

**NARRATION (Telugu master):** చూడటానికి యువకుడి అందమైన ముఖం — కానీ గభీరమైన ఆత్మజ్ఞాన నిశ్శబ్దత — అతడే శుకదేవ గోస్వామి!
**DURATION:** 8.5s target

**KEYFRAME:** `episode05/assets/EP05_S32.jpg` (to generate)

**STILL PROMPT (image):**
```
Full revealing frame of Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet arriving at the assembly edge, face serene beyond age, faint gold aura threading through the air around him, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow crane from feet to eyes as he steps in; petal-light swirls; his eyes meet the camera once — a student's openness with a realized sage's depth. C-SHUKA full dawn phrase. SFX: hush-break of joyful soft murmurs.
```

### S33 · 3:56.00–4:04.50 · The King Rises
_respect completes_

**NARRATION (Telugu master):** వ్యాస మహర్షి కుమారుడు — జ్ఞాన వైరాగ్యాలకు శరీరమైన ఆ ఋషికి — పరిక్షిత్తు లేచి ఆదరంగా నమస్కరించాడు.
**DURATION:** 8.5s target

**KEYFRAME:** `episode05/assets/EP05_S33.jpg` (to generate)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold rising swiftly yet controlled, deep respectful namaskara with both hands and bowed head toward the arriving Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Two-shot deepen: king enters lower left, raises joined palms to forehead; cut reverse on Shuka's soft acknowledgment nod; both at correct heights of grace. C-SHUKA warms. SFX: robes, river.
```

### S34 · 4:04.50–4:12.00 · Seat of Honor
_assembly orders itself_

**NARRATION (Telugu master):** మహర్షులందరు శుకుని ఉన్నత ఆసనంలో కూర్చోబెట్టారు — అతడు ఆ సభ కేంద్రమాయ్యాడు.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S34.jpg` (to generate)

**STILL PROMPT (image):**
```
Elderly sages gesturing Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet to the central raised kusha seat, the young sage folded into it simply, lamp-light finding his face from many small lamps, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow top-spiral down as the seat accepts him; lamps kindle in expanding rings; the frame settles into perfect symmetry — question and answer now seated. C-SHUKA + temple bell cadence. SFX: settling cloth, mridangam one sweet hit.
```

### S35 · 4:12.00–4:19.00 · The Question, Again
_repeated to the one_

**NARRATION (Telugu master):** పరిక్షిత్తు అదే ప్రశ్న శుకుని ముందు వేశాడు — జోడించిన చేతులతో, నమ్రదృష్టితో.
**DURATION:** 7.0s target

**KEYFRAME:** `episode05/assets/EP05_S35.jpg` (to generate)

**STILL PROMPT (image):**
```
King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold leaning forward palms-joined repeating his question to seated Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet, face open like a child's before a true teacher, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Over-Shuka-shoulder onto the king's asking face; the answerer's closed eyes and soft smile hold the background. C thins to tanpura + flute answering motif (Q-rise). SFX: one sustained river breath.
```

### S36 · 4:19.00–4:28.50 · Shuka's Answer
_soft smile, seed of everything_

**NARRATION (Telugu master):** శుకుడు మృదువుగా నవ్వి — మహారాజా — ఇదే సరైన ప్రశ్న. మరణించే జీవులకు శ్రేష్ఠమైనది — భగవద్గుణ కథల శ్రవణం.
**DURATION:** 9.5s target

**KEYFRAME:** `episode05/assets/EP05_S36.jpg` (to generate)

**STILL PROMPT (image):**
```
Close on Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet: eyes opening gentle, the kind smile of a sage asked a perfect question, resting glow on his brow, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current bokeh behind, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Locked face close; eyes open and the world seems to exhale; smile widens by degrees as the answer lands (VO carries). C-SHUKA blooms to Mohanam home phrase. SFX: soft conch, far bell, first birdsong of day one.
```

### S37 · 4:28.50–4:36.00 · The Recitation Begins
_sound becomes river_

**NARRATION (Telugu master):** అప్పుడు శుక మహర్షి — శ్రీమద్భాగవత కథను పలకడం ప్రారంభించాడు.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S37.jpg` (to generate)

**STILL PROMPT (image):**
```
Symbolic beauty shot: from Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet's opening mouth a stream of golden letter-light pours and becomes a river of glowing script flowing across the night air over the seated assembly, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Macro mouth→letters→river composite; script-river winds above the listeners' upturned faces whose every line is lit gold. C-SHUKA + Bhakti river (Desh). SFX: veena shimmer, river-light chime.
```

### S38 · 4:36.00–4:43.50 · Seven Suns and Seven Moons
_time-wheel montage_

**NARRATION (Telugu master):** ఆ ఏడు దినాలు — గంగా తీరాన్ని దివ్య కథా ప్రవాహంగా మార్చేశాయి.
**DURATION:** 7.5s target

**KEYFRAME:** `episode05/assets/EP05_S38.jpg` (to generate)

**STILL PROMPT (image):**
```
Time-montage over the riverbank: sun-moon wheel arcing through the sky above the unmoving sabha, petals falling, lamps relit, Ganga changing colors through days, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Accelerated clouds behind STILL foreground figures (time passes around them, not through them); a day-count hinted by seven brief sunrise flares. C-GANGA+DESH cycling. SFX: bell each dawn.
```

### S39 · 4:43.50–4:50.50 · Absorbed Hearts
_devotion weather_

**NARRATION (Telugu master):** సభ్యులందరి మనసులు ఆ కథలో నిమగ్నమయ్యాయి — కాలం కూడా నిశ్చలమైపోయింది.
**DURATION:** 7.0s target

**KEYFRAME:** `episode05/assets/EP05_S39.jpg` (to generate)

**STILL PROMPT (image):**
```
Intimate faces of listeners: an old sage weeping smiling, a child disciple asleep on a shoulder, King Parikshit: noble young Indian king in his thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, royal silk garments in deep maroon and gold rain-washed serene, all bathed in the same warm glow, sacred Ganga riverbank at dawn and dusk, wide shimmering water, white sand, leaf-mat seats, marigold petals on the current, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow pan across the gallery of faces; each tells the whole story; end on king's face utterly at home. C thins to flute only, then hearts-hush. SFX: river, tear-warmth silence.
```

### S40 · 4:50.50–5:00.50 · End Card (visual + text bake)
_grantham on lotus — EP6 pointer_

**NARRATION:** — (visual-only beat)
**DURATION:** 10.0s target

**KEYFRAME:** `episode05/assets/EP05_S40.jpg` (to generate)

**STILL PROMPT (image):**
```
Sacred end-card backdrop: closed yellow-bound palm-leaf grantham resting on an open pink lotus above the calm Ganga, soft Sri-Yantra mandala glowing behind in maroon-gold, petals adrift, premium 2.5D cinematic anime, Indian mythological painting, Ghibli-inspired hand-painted backgrounds, rich natural colors, volumetric golden divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark
```

**ANIMATION PROMPT (Flow · image-to-video):**
```
Slow breathe zoom on the grantham; mandala rotates almost imperceptibly; petals drift. TEXT IS BAKED SEPARATELY (uharfbuzz pipeline — never model-rendered): 'తరువాతి భాగంలో… / శ్రీమద్భాగవతం — మంగళాచరణం / SRIMAD BHAGAVATAM – EPISODE 6 / Series by Creations Diary'. C-END mohanam home + solo temple bell. SFX: one bell, wavelet, fade.
```

---

**Total design runtime: 5:00.5** (final master will land ~+8–12% with natural TTS pacing; slots absorb via 0.45s tails).

_Next in series: **EPISODE 6 — శ్రీమద్భాగవతం మంగళాచరణం** (S40 end card points here only — no later plot revealed)._