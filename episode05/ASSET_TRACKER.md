# EPISODE 5 ASSET TRACKER — "Parikshit's Seven Days" (పరిక్షిత్తు మహారాజు కథ)
Blueprint: vo_script/EP05_scene_texts.json — 40 scenes, 37 speaking + 3 visual (S12, S30, S40 end card)

## Status: IN PROGRESS
- [x] Thumbnail base + final (thumb_ep05_final.jpg commit c871aca)
- [x] Scene texts x40 (Telugu)
- [ ] Narration VO: 0/37 (add_voice re-audit REQUIRED next turn — voice ids reset; failed attempts burned this turn's speech cap)
- [ ] BGM build + mix (constants: DUCK=0.80, bed 0.38 — series standard from EP4)
- [ ] FLOW_PRODUCTION_KIT.md (after audio master exists)
- [x] Keyframes: 9/40 — S01–S09

## Keyframes
| S01 ridge walk+city glow | S02 throne portrait | S03 blessing subjects | S04 hunt |
| S05 thirsty at ashrama | S06 HUMOR bush-guard | S07 Shamika samadhi | S08 water-ask silence |
| S09 pride flicker close |\n| S10 the mistake | S11 turning away | S12 pond ripple | S13 whisper | S14 rage close | S15 water touch | S16 CURSE golden-7 | S17 father wakes | S18 rebuke | S19 runner |

## Character locks (image prompts — reuse in Flow)
- PARIKSHIT: noble young Indian king early thirties, sharp dignified face, determined eyes, golden jewel-studded crown, pearl necklaces, maroon + gold royal silks, bow/quiver in forest
- SHAMIKA: very old sage, long white beard, white matted topknot, white tilak, faded ochre robes, austere thin, deep meditation
- SHRINGI: teenage sage ~15, lean, saffron student robes, topknot, sacred thread, fiery intense eyes
- GAURAMUKHA: young ashrama disciple, ochre dhoti, carrying palm-leaf message
- JANAMEJAYA: boy prince ~10, small golden crown, blue silk
- SHUKA/VYASA: inherit EP4 locks (episode04/postprod/make_flow_kit_ep4.py)
- Style: premium 2.5D cinematic anime, Indian mythological painting, volumetric golden divine light, 16:9, family-friendly, no text

## MULTILINGUAL AUDIO (user directive: audio-only HI+EN, no images)
- [x] HI script 40 slots / EN script 40 slots (commit 9c27c35)
- [ ] HI VO 5/37 — S01-S05 done | [ ] EN VO 5/37 — S01-S05 done
- [ ] ENGINES: assemble cloned (assemble_ep5_lang.py) | BGM PORT PENDING — clone make_bgm_ep4_lang.py -> ep5, retarget theme table to EP5 10-cue map (C-ROYAL Hamsadhwani S02-03 / C-HUNT tabla S04-06 / C-THIRST Shivaranjani S05 / C-SAMADHI drone S07-09 / C-CURSE Bhairavi S10-20 / C-FATHER Kalyani S17-22 / C-RENOUNCE Mohanam S22-24 / C-GANGA Desh S23-30 / C-SHUKA Mohanakalyani S29-37 / C-END Mohanam+bell S37-40); duck .80/bed .38
