# భృగు మహర్షి — Keyframe జనరేషన్ ప్లాన్ & స్టేటస్

**వీడియో:** భృగు మహర్షి కథ — త్రిమూర్తుల పరీక్ష (10:00)
**కీఫ్రేమ్‌లు:** 17–20 చిత్రాలు (నిమిషానికి 2 చొప్పున), 16:9 సినిమాటిక్ ఫ్రేమ్‌లు
**టార్గెట్:** Pixar-style 3D అనిమేషన్, ఒకే స్టైల్‌లో స్థిరంగా
**ఫోల్డర్:** `keyframes/bhrugu/` (JPEG q92 — repo తేలికగా ఉండేందుకు PNG renders నుండి మార్చినవి)

> **స్టేటస్:** 10 చిత్రాలు ఈ టర్న్‌లో పూర్తయ్యాయి (image limit 10 per turn). మిగిలిన 7 చిత్రాలు తదుపరి టర్న్‌లో generate చేయగలను — కింద "PENDING" గా గుర్తించినవి.

---

## 1. ప్రాంప్ట్ స్టైల్ (ప్రతి ప్రాంప్ట్ చివర్లో తప్పనిసరిగా జోడించాలి)

```
...in a consistent Pixar-style 3D animation, high detail, 8k resolution, cinematic lighting, vibrant colors, epic mythological theme.
```

**అదనంగా జోడించాల్సినవి (నాణ్యత కోసం):**
- **Aspect:** `wide cinematic 16:9 frame` (పోర్ట్రెయిట్ రాకుండా — ఫ్రేమ్ 02 ఇలాగే పోర్ట్రెయిట్ వచ్చింది, తిరిగి చేయాలి)
- **Negative prompt:** `no text, no watermark, no extra limbs, no deformed hands, no distorted faces, no modern objects, no photorealistic style, no low quality, no cropped heads`
- **చిన్న టిప్:** ఒకే సీన్‌లోని షాట్‌లకు ఒకే "character locked" వాక్యం ముందు పెట్టడం వల్ల పాత్రలు ఒకేలా వస్తాయి (సెక్షన్ 3 చూడు).

---

## 2. పూర్తి టైమ్‌లైన్ & స్టేటస్

| # | సమయం | ఫైల్ | కంటెంట్ | స్టేటస్ |
| :--- | :--- | :--- | :--- | :--- |
| 1 | 0:00–0:30 | `01_0m00s_vedic_assembly.jpg` | యజ్ఞశాల wide shot — మునుల సభ, బంగారు దీపాలు | ✅ పూర్తి |
| 2 | 0:45–1:15 | `02_0m45s_bhrigu_closeup.jpg` | భృగు మహర్షి close-up — తీవ్రమైన చూపు | ⚠️ పూర్తి (పోర్ట్రెయిట్ — 16:9 లో తిరిగి కావాలి) |
| 3 | 1:15–1:30 | `17_1m15s_bhrigu_oath.jpg` | భృగువు నిలబడి ప్రతిజ్ఞ చేసే షాట్ (అగ్ని కాంతి) | ⏳ PENDING |
| 4 | 1:30–2:00 | `03_1m30s_sages_debating.jpg` | మునులు చర్చ, ఆకాశం వైపు చూపుతూ | ✅ పూర్తి |
| 5 | 2:15–2:45 | `04_2m15s_brahmaloka.jpg` | బ్రహ్మలోక ప్రవేశం — పద్మంపై చతుర్ముఖ బ్రహ్మ | ✅ పూర్తి |
| 6 | 3:00–3:30 | `05_3m00s_bhrigu_before_brahma.jpg` | భృగువు నమస్కరించకుండా నిలబడటం, బ్రహ్మ ఆఘాతం | ✅ పూర్తి |
| 7 | 3:45–4:00 | `06_3m45s_brahma_controlling_anger.jpg` | బ్రహ్మ కళ్లు మూసి కోపాన్ని అణచుకోవడం | ✅ పూర్తి |
| 8 | 4:15–4:45 | `07_4m15s_mount_kailash_shiva.jpg` | కైలాసం — ధ్యానంలో శివుడు, మంచు శిఖరాలు | ✅ పూర్తి |
| 9 | 5:00–5:30 | `08_5m00s_kailash_confrontation.jpg` | భృగువు అరుపు, త్రిశూలంతో శివుడు, మధ్యలో పార్వతి | ✅ పూర్తి |
| 10 | 5:45–6:00 | `09_5m45s_parvati_calming_shiva.jpg` | పార్వతి శాంతపరచడం, త్రిశూలం దింపడం | ✅ పూర్తి |
| 11 | 6:15–6:45 | `10_6m15s_ksheera_sagara_vishnu.jpg` | క్షీరసాగరం — ఆదిశేషుడిపై విష్ణువు, లక్ష్మి | ✅ పూర్తి |
| 12 | 7:00–7:30 | `11_7m00s_the_kick_impact.jpg` | విష్ణువు వక్షస్థలంపై తన్నిన క్షణం, అలలు | ⏳ PENDING |
| 13 | 7:45–8:00 | `12_7m45s_srivatsa_impact_mark.jpg` | వక్షంపై పాదముద్ర close-up, దివ్య కాంతి | ⏳ PENDING |
| 14 | 8:15–8:45 | `13_8m15s_vishnu_holding_feet.jpg` | విష్ణువు లేచి భృగువు పాదాలు పట్టుకోవడం | ⏳ PENDING |
| 15 | 8:50–9:00 | `14_8m50s_bhrigu_in_tears.jpg` | భృగువు కన్నీళ్లతో మోకాళ్లపై కూలడం | ⏳ PENDING |
| 16 | 9:15–9:40 | `15_9m15s_bhrigu_returns_to_assembly.jpg` | సభకు తిరిగి వచ్చి తీర్పు చెప్పడం | ⏳ PENDING |
| 17 | 9:45–10:00 | `16_9m45s_srivatsa_glowing_ending.jpg` | శ్రీవత్స చిహ్నం మెరుస్తూ ముగింపు | ⏳ PENDING |
| 18 | థంబ్‌నెయిల్ | `00_thumbnail_three_gods.jpg` | బ్రహ్మ / శివుడు / విష్ణువు 3-ప్యానెల్ + "ఎవరు శాంతమూర్తి?" | ⏳ PENDING |

**నిమిషానికి కీఫ్రేమ్‌లు:** 0–2 నిమి = 3 • 2–4 = 3 • 4–6 = 3 • 6–8 = 3 • 8–10 = 4 — i.e. ప్రతి నిమిషానికి 2–3 కంటే ఎక్కువే ఉన్నాయి. ✅

**Contact sheet:** `_contact_sheet_01-10.jpg` (పూర్తయిన 10 చిత్రాల సమీక్ష)

---

## 3. పాత్రల స్థిరత్వం (Continuity Sheet) — ఇది ప్రతి ప్రాంప్ట్‌లో ముందు పెట్టు

| పాత్ర | ప్రాంప్ట్ వాక్యం (ఇదే పదాలతో వాడు) |
| :--- | :--- |
| **భృగు మహర్షి** | `Sage Bhrigu: elderly Indian sage, long silver-white beard and hair tied in a topknot, three horizontal white ash lines with a red mark on the forehead, saffron-orange robes, rudraksha bead necklaces, intense piercing eyes` |
| **బ్రహ్మ** | `Lord Brahma: four heads, white beard, golden crown, cream-white silk robes, seated on a giant pink lotus, golden divine aura` |
| **శివుడు** | `Lord Shiva: blue-grey skin, matted dark hair with crescent moon, third eye on forehead, tiger-skin garment, silver trident, snow-white aura` |
| **పార్వతి** | `Goddess Parvati: fair skin, red and green silk saree, golden crown and jewellery, calm compassionate smile, soft white glow` |
| **విష్ణువు** | `Lord Vishnu: blue skin, yellow silk garments, golden crown, calm smiling face, chest emblem, conch and chakra nearby, warm golden glow` |
| **లక్ష్మి** | `Goddess Lakshmi: golden-red silk saree, gold jewellery, seated on a pink lotus, radiant gentle smile` |
| **ఆదిశేషుడు** | `Sheshnag: gigantic white multi-hooded serpent, jewel-topped hoods, coiled as a bed over the milky ocean` |

**శైలి గుర్తుంచుకోవాల్సినవి:** warm golden ↔ cool blue contrast (సభ = బంగారం, కైలాసం = మంచు నీలం, క్షీరసాగరం = పాల తెలుపు + నీలం), రంగులు ఎప్పుడూ vibrant కానీ mythological గంభీరం.

---

## 4. మిగిలిన 7 ప్రాంప్ట్‌లు (తదుపరి టర్న్‌లో generate చేయడానికి సిద్ధం)

```
11. 7:00–7:30 — "Dramatic moment in the Milky Ocean: Sage Bhrigu raising his leg toward the reclining Lord Vishnu's chest, Vishnu still peacefully lying on the giant serpent with eyes just opening, Goddess Lakshmi gasping in the background, ripples spreading across the white ocean, swirling wind, dramatic shadow and divine glow, wide cinematic 16:9 frame, in a consistent Pixar-style 3D animation, high detail, 8k resolution, cinematic lighting, vibrant colors, epic mythological theme."

12. 7:45–8:00 — "Extreme close-up of Lord Vishnu's chest in the Milky Ocean, a glowing luminous footprint mark radiating golden divine light from the point of contact, blue skin with yellow silk garment, tiny sparkles and lotus petals floating, sacred and peaceful mood, wide cinematic 16:9 frame, ...suffix..."

13. 8:15–8:45 — "Lord Vishnu standing up on the milky ocean, gently holding Sage Bhrigu's feet with both hands, face full of love and concern, Bhrigu stunned and ashamed, Sheshnag rising behind, soft golden lighting, wide cinematic 16:9 frame, ...suffix..."

14. 8:50–9:00 — "Sage Bhrigu falling to his knees in tears on the milky ocean shore of white waves, hands folded in devotion and regret, Lord Vishnu blessing him with a raised palm, warm divine light, wide cinematic 16:9 frame, ...suffix..."

15. 9:15–9:40 — "Sage Bhrigu back in the Vedic assembly hall explaining his journey to the sages with expressive hand gestures, sages listening in awe with wide eyes, sacred fire glowing, golden lamp light, wide cinematic 16:9 frame, ...suffix..."

16. 9:45–10:00 — "Close-up of Lord Vishnu's chest with the glowing 'Srivatsa' symbol radiating bright golden light, cosmic starry background with soft nebula, peaceful divine ending mood, wide cinematic 16:9 frame, ...suffix..."

17. 1:15–1:30 — "Sage Bhrigu standing tall in the Vedic assembly hall, raising his hand to take a vow, subtle fiery aura around his body, sages looking up at him with hope, embers floating, wide cinematic 16:9 frame, ...suffix..."

18. Thumbnail — "Three divine figures in one dramatic frame: Lord Brahma with reddened eyes on the left, Lord Shiva gripping a silver trident in the centre, Lord Vishnu smiling serenely on the right, cosmic background, in a consistent Pixar-style 3D animation, high detail, 8k resolution, cinematic lighting, vibrant colors, epic mythological theme."
```

---

## 5. షాట్‌లకు వాడే విధానం (Video timeline)

- ప్రతి కీఫ్రేమ్‌ను **5–8 సెకన్ల** పాటు చూపించి, మధ్యలో **నెమ్మది zoom / pan (parallax)** ఇవ్వడం వల్ల 10 నిమిషాలకు చక్కగా సరిపోతుంది.
- ఎక్కువ సమయం ఉన్న సీన్‌లలో (2 నిమిషాల యాక్ట్‌లు) ఒకే చిత్రాన్ని **2 shots** గా కట్ చేయి (wide → close-up), లేదా ఆడియోలోని పాజ్‌ల వద్ద కొత్త frame కి మార్చు.
- **టైమింగ్:** `audio/bhrugu/final/build_info.json` లో భాగాల మార్కులు ఉన్నాయి — 0:00.8 • 1:15 • 2:26 • 3:37 • 4:50 • 6:04 • 7:16 • 8:22 • 9:31. యాక్ట్ మార్పులు: **2:07 బ్రహ్మ లోకం • 4:06 కైలాసం • 6:15 క్షీరసాగరం • 8:35 ముగింపు** — storyboard ను వీటికి అనుగుణంగా కట్ చేయి.
- **AI వీడియో (img2vid) కి:** ప్రతి కీఫ్రేమ్‌ను మొదటి ఫ్రేమ్‌గా పెట్టి 5 సెకన్ల మోషన్ క్లిప్ చేయవచ్చు (subtle camera move + cloth/hair movement చెప్పు; పాత్రలు కదలకుండా).
