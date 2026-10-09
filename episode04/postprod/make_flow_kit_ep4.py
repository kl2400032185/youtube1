#!/usr/bin/env python3
"""Emits episode04/FLOW_PRODUCTION_KIT.md — Google Flow hand-off:
per scene: audio time window, narration, image file (16:9 keyframe),
IMAGE prompt (for still generation consistency) + ANIMATION prompt (Flow image-to-video).
Character locks ride every prompt where a character appears."""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sm = json.load(open(os.path.join(ROOT, 'scene_map_ep4.json')))
tx = json.load(open(os.path.join(ROOT, 'vo_script', 'EP04_scene_texts.json'), encoding='utf-8'))['scenes']
TXT = {s['n']: s['b'] for s in tx}

VYASA = ("Elderly sage Vyasa: long white beard, long white hair in a matted topknot, white tripundra "
         "tilak on forehead, saffron ochre robes, rudraksha mala, calm wise compassionate face")
SHUKA = ("Young sage Shuka, about eighteen: clean-shaven smooth face, long dark hair in a neat topknot, "
         "bright calm intelligent eyes, plain white and ochre ascetic robes, one thin rudraksha strand, bare feet")
WORLD = ("ancient Indian forest ashrama by a river, giant banyan and tamarind trees, thatched hermitage huts, "
         "blue mountains in the distance, palm-leaf manuscripts, golden natural light")
STYLE = ("premium 2.5D cinematic anime, Indian mythological painting, rich natural colors, volumetric golden "
         "divine lighting, expressive faces, family-friendly, 16:9, no text, no watermark")

IMG = {
1: f"{VYASA} seated in deep meditation on a smooth flat river-stone, soft golden divine aura slowly swirling around him, morning river mist, {WORLD}, {STYLE}",
2: f"Symbolic divine vision flash in indigo space: radiant golden divine light at the center, below it drifting golden sparks behind a shimmering aurora veil of maya, beautiful comforting, not frightening, ethereal celestial gold, {STYLE}",
3: f"Extreme close-up of {VYASA}'s forehead in meditation, white tripundra tilak glowing softly, light blooming outward, river bokeh behind, {STYLE}",
4: f"{VYASA}'s eyes just opened with renewed clarity at the riverbank, his weathered hands lifting a cord-bound bundle of palm leaves and a thin nail-stylus, resolve dawning, warm morning gold, {STYLE}",
5: f"Macro of an elderly sage's weathered hand engraving long elegant strokes onto a fresh palm leaf with a thin nail-stylus, dark ink blooming in the grooves, brass ink pot beside, warm desk light, {STYLE}",
6: f"Sage's writing desk: ink pot and resting stylus, one palm-leaf corner lifting in a gentle breeze, two young disciples in ochre dhotis bringing a fresh stack of palm leaves from a respectful distance, {WORLD}, {STYLE}",
7: f"Time passing over a sage's work: golden sunlight tracking across a growing stack of completed palm-leaf manuscripts, long shadows sweeping across the desk, a small oil lamp waiting for evening, {STYLE}",
8: f"Night writing: a single steady oil-lamp flame in the foreground, {VYASA}'s silhouette engraving palm leaves by its light, tall stacks of completed manuscripts beside him, deep blue night outside the hut window, {STYLE}",
9: f"Dawn arriving: oil lamp fading as morning gold pours through the hut window onto {VYASA} who is still calmly writing, light flooding the room, {STYLE}",
10: f"Epic top-down canopy view of the {WORLD}, sacred fire kund with a thread of smoke, a tiny golden figure of {VYASA} writing at the riverbank far below, {STYLE}",
11: f"{VYASA} has just stopped writing, nail-stylus resting in hand, gazing long and peacefully at a bundle of completed palm-leaf manuscripts on his desk, a quiet thoughtful question on his brow, window light, {STYLE}",
12: f"Golden forest morning, dew on a lotus pond, peacock silhouette on a branch, a lean young figure walking barefoot on a leaf-litter path at the ashrama edge, partially hidden by light shafts, {WORLD}, {STYLE}",
13: f"{SHUKA} walking calmly through morning light shafts in the forest, two young disciples pausing their chores in the background to watch him pass, serene {WORLD}, {STYLE}",
14: f"Gentle comedy: behind {SHUKA} walking gracefully, a small monkey carefully imitates his upright two-legged walk with arms folded like a scholar; the monkey wobbles and catches itself on a bush while trying again, {WORLD}, {STYLE}",
15: f"{SHUKA} drifting past a mango grove, untempted by fallen fruit, crouching gently to watch a spider weaving its web between two leaves with fascination, {WORLD}, {STYLE}",
16: f"{SHUKA} standing among friendly deer in the forest, a small fawn nuzzling his hand, birds settled on branches above him, soft smile, morning gold, {STYLE}",
17: f"{SHUKA} settling calmly into meditation posture on the same smooth river-stone where his father once meditated, water mirroring his stillness, {WORLD}, {STYLE}",
18: f"Close on {SHUKA}'s chest and hands in meditation — slow even breathing, rudraksha strand resting motionless on his wrist, river blurred beyond, {STYLE}",
19: f"Close-up of {SHUKA}'s face as his eyes gently close, sunlight dappling his forehead through moving leaves, absolute peace, {STYLE}",
20: f"{SHUKA} in meditation seen through soft golden edge blur, eyes fully closed, a single green leaf falling past the frame edge, the world dissolving gently, {STYLE}",
21: f"Inner spark: infinite indigo space with one small point of golden lantern-light appearing and softly pulsing, contemplative cosmic minimalism, ethereal glow, {STYLE}",
22: f"Warm festive village scene glimpsed between forest trees: villagers in fine clothes, ornaments catching light, decorated ox-cart, drummers and laughter, colorful and joyful, seen in soft focus through trunks, {STYLE}",
23: f"Warm village life: an old woman laughing with her grandchild, two friends greeting each other with folded palms, beads and marigold garlands, ordinary life glowing beautifully, {STYLE}",
24: f"{SHUKA} walking the quiet empty forest trail with gentle contentment, the dim festival glow fading far behind him between trees, no bitterness, {WORLD}, {STYLE}",
25: f"{SHUKA} carefully stepping around a fallen beehive with respect, one butterfly circling him twice and leaving, his eyes following it with a soft untethered gaze, {WORLD}, {STYLE}",
26: f"Epic wide of a mountain valley opening before {SHUKA} standing small at a cliff edge, silver river far below, enormous sky, wind moving his hair, {STYLE}",
27: f"Over-shoulder from {VYASA}'s writing desk: he looks up from his manuscript and sees {SHUKA} at the distant treeline returning home, love and a subtle worry on the father's face, shallow focus, {STYLE}",
28: f"{VYASA} approaching {SHUKA} gently near the temple-tree at the ashrama, golden afternoon light, both calm, medium two-shot, {STYLE}",
29: f"Profile close of {SHUKA} turning to his father with folded hands and bright respectful eyes, soft rim light, {STYLE}",
30: f"Over-the-shoulder of {VYASA}: {SHUKA} speaking calmly in soft sunlight, young serene face, father's white-beard silhouette in foreground, {STYLE}",
31: f"{VYASA} listening to his son, eyes glistening with pride and pain at once, {SHUKA} steady and gentle beside him under the temple-tree, {STYLE}",
32: f"Extreme low frame: a pair of simple sandals left on the ashrama path edge as {SHUKA}'s bare feet step past them walking away, cu of resolve, {STYLE}",
33: f"{VYASA} standing at the ashrama edge, his hand halfway lifted then lowered with quiet dignity, white beard moving in the wind, disciples watching silently from chores in soft-focus background, {STYLE}",
34: f"Long view from behind: {SHUKA} walking alone down the tall forest path away from home, steady barefoot stride, trees towering over him, distant festival drums becoming silence, {WORLD}, {STYLE}",
35: f"Gentle comedy: at a distance behind {SHUKA} on the forest path, the same small monkey still practices upright walking, wobbling, catching itself with its tail; the tiniest smile at Shuka's lip edge though he does not turn, {STYLE}",
36: f"{VYASA} with his wooden staff begins to follow at a long distance at the forest mouth, disciples bowing as their guru passes, a father's silent chase, {WORLD}, {STYLE}",
37: f"{VYASA} among tall trees cupping his mouth tenderly to call out across the forest, worry and love held inside, golden shafts, {STYLE}",
38: f"Wide forest canyon under evening blue: leaves quivering, a flock of birds rising briefly as a father's call travels and echoes deep through the valley, {WORLD}, {STYLE}",
39: f"{SHUKA} pauses a single breath on the path with eyes softening at the echo behind him, then continues forward; far at the treeline {VYASA} still following small in the frame, cinematic depth, {STYLE}",
40: f"Vast high-crane wide of the forest path: two tiny figures, son ahead glowing in golden light, father behind in gentler shade, enormous trees around both, {WORLD}, {STYLE}",
41: f"The river at a different golden hour: soft dome of light swirling around {SHUKA} seated upstream on a stone, lotus petals drifting in the current, poetry of time passing, {STYLE}",
42: f"{SHUKA} stepping into a vertical shaft of pure divine golden light, his silhouette glowing, grace passing through him, the air alive with light motes, symbolic transformation, not frightening, {STYLE}",
43: f"Mature aura {SHUKA} at the river at sunrise, the same young face with deeper stillness, lotus flowers circling him in the water, halo of sun behind his topknot, low-angle divine framing, {STYLE}",
44: f"Wide reveal: elderly forest hermits bowing to {SHUKA} one by one while he humbly carries firewood for them, accepting nothing from anyone, morning gold, {STYLE}",
45: f"{VYASA} holding a completed palm-leaf GRANTHAM bundle tied with yellow cloth, disciples bowing to the sacred book in the ashrama courtyard, close on hands then calm faces, {STYLE}",
46: f"Profile of {VYASA} at his window holding the bound manuscript, his gaze traveling toward the forest where his son walked away, lamp light, {STYLE}",
47: f"Vision-layer: soft seeds of golden light floating upward from the bound manuscript like fireflies toward a vast painted world of valleys and rivers, the story traveling to the world, {STYLE}",
48: f"Dusk: {VYASA} alone at his desk again, oil lamp lit, bound manuscript beside him, a father's calm patient waiting, single warm push, {STYLE}",
49: f"Inside a lamp-lit royal sabha hall: a young noble Indian king in hunting dress sitting respectfully on a plain seat among aged white-bearded sages, hands joined with humility, alert intelligent eyes (King Parikshit honored among sages, no throne), carved pillars and oil lamps, {STYLE}",
50: f"Forest hermitage at night: rows of meditating sages under starlight, a central empty wooden seat prepared for an honored speaker, moths circling a single diya flame, anticipation hush, {STYLE}",
51: f"Close profile of {VYASA} standing at his ashrama doorway, evening wind pulling at his saffron shawl, watching the western sky with quiet knowing, {STYLE}",
52: f"Ground-level frame: {SHUKA}'s bare feet walking forward on a mountain pass trail, unhurried and certain, evening golden haze ahead, dust motes rising, {STYLE}",
53: f"Extreme close-up of {SHUKA}'s peaceful face, eyes lowered in contentment, hair moving softly in mountain wind, the calm of one who has arrived, {STYLE}",
54: f"Far royal palace silhouette glowing on an island of dusk clouds, golden lamps lit in its windows, mystery and destiny in vignette, distant Indian kingdom, {STYLE}",
55: f"Split-vision: silhouette of a king on the left crest, silhouette of a sage on the right crest, a river of golden light winding between them, three silent questions hanging in the dusk, {STYLE}",
56: f"Golden carved mandala like a luminous Sri-Yantra orb behind a small forest hermitage at twilight, banyan silhouette below, vast warm dusk sky, reserved space in lower third for title text, ethereal celestial gold, {STYLE}",
}

ANIM = {
1: "Slow camera push-in; golden aura gently swirling around the seated sage; river mist drifting right to left; cloth and beard moving almost imperceptibly with breath; serene, keep face natural.",
2: "Dreamy float forward through the indigo space; golden sparks drifting upward; aurora veil shimmering like fabric of light; mandala light slowly rotating; slow breathing glow.",
3: "Micro-movement only: light blooming brighter then softer on the tilak; very slight slow orbit; bokeh shimmering; eyelids absolutely still; meditative.",
4: "Two-beat move: rack from eyes opening to hands lifting the palm leaves; gentle push-in; morning light slowly brightening; sleeve and beard subtle sway.",
5: "Macro crane slowly lowering onto the hand; stylus engraving continuously with small back-and-forth engraving tremors; ink blooming line by line; dust motes in the light.",
6: "Slow lateral slide; page corner fluttering in breeze loops; disciples approach in the background walking politely; lamp flame flickering.",
7: "Time-lapse feel: long shadow sweeping across the parchment stacks; paper edges fluttering; ambient dust floating; warm-to-dim light transition.",
8: "Slow dolly past the flame in foreground; silhouette hand writing steadily behind; flame wavering with air; deep blue night window inhaling light; grain calm.",
9: "Pull-out through the window from inside to outside; lamp fading as gold pours in; sleeve moving with writing rhythm; birds beginning to chirp visually outside.",
10: "Top-down orbit slowly descending; smoke thread winding upward; river current flowing in curls; distant mountains breathing haze.",
11: "Slow push-in to the sage's face over several seconds; eyes blinking once thinking; manuscript corner rustling; expression deep in question.",
12: "Ankle-height tracking shot following the young walker's steps; dew drops flicking from grass; light shafts sliding across frame; peacock silhouette turning its head.",
13: "Lateral track keeping pace with the walking young sage; hair-topknot swaying gently; servants pause sweeping to watch in the background; dust motes dancing in light shafts.",
14: "Follow shot from behind the monkey: monkey upright-walking with comedic wobbles, catches itself on a bush, tries again repeatedly; main figure walking graceful unaware; warm amused tone, no slapstick.",
15: "Gentle pan from mango fruit to the young sage's eyes; he crouches slowly; spider weaving thread by thread in macro insert perspective; soft breathing.",
16: "290-degree orbit around the moment; fawn nuzzling hand; ears twitching; birds shifting on branches; all very gentle; leaves falling slowly.",
17: "Dissolve feel from walking into seated meditation; slow push in; water ripples settling to stillness; reflection stabilizing.",
18: "Static frame: chest rising and falling slowly; rudraksha still; river bokeh shimmering in background; screensaver-calm.",
19: "Extreme close: eyelids lowering over two seconds; dappled leaf-light drifting on forehead; hair edge micro-movement; breath slowing.",
20: "Camera gently easing out of focus around the edges; a single leaf falls in slow motion past frame; world gold haze; absolutely calm.",
21: "Slow inward drift toward the point of light; pulse glow expanding and softening; indigo haze subtle swirl; meditative tempo.",
22: "Parallax wander through tree trunks into the festivity; flags swaying; people moving naturally in merriment; dust glitter in light; distant drums felt subtly.",
23: "Small handheld wander between families; child running past; garlands swinging; everyone smiling; motherly warmth.",
24: "Low-angle hero pass as Shuka walks steadily; his simple robes swaying; festival glow dimming behind bokeh; resolve on face.",
25: "Knee-level follow; careful step around beehive; butterfly circles twice and exits frame; gentle smile follows it; slow leaf fall.",
26: "Huge pull-out reveal from the figure to the vast valley; wind blowing hair and cloth strongly; clouds drifting fast over mountains; scale dwarfing.",
27: "Focus rack from manuscript to the distant figure at treeline over two seconds; the old sage's hand pausing; window light steady.",
28: "Slow dolly in on both father and son; affectionate warm light; both breathing naturally; peepul leaves rustling.",
29: "Profile close: Shuka turns gracefully, hands folding; eyes bright attentive; hair edge sway; respectful.",
30: "Over-the-shoulder with slow push; Shuka speaking with calm steadiness; small hand gesture of knowing; light constant.",
31: "Slow orbital arc around the pair; father's eyes glistening; a held blink; wind touch on beard; emotion held inside.",
32: "Extreme low angle: sandals abandoned in foreground while bare feet step past them walking away; heel lifts, toes touch, resolve; path dust.",
33: "Rack focus hand to face: hand halfway rises and slowly lowers with dignity; beard wind; disciples' brooms freeze mid-sweep.",
34: "Long follow from behind; the figure dwindles down the path; trees towering; distant drum ambience silencing; light evening-warm.",
35: "Trailing two-shot: monkey practices upright walking, wobbles, catches its tail; Shuka's half-profile with the tiniest smile; gentle amused camera sway.",
36: "Wide forester shot: old guru begins to walk with staff from ashrama to forest; disciples bowing as he passes; dust and light swirl.",
37: "Close portrait: cupped hands at mouth, tender restrained call; eyes holding worry; leaves shivering around.",
38: "Wide canyon: birds lift from trees as the call travels; leaves quivering in wave; echo visualized by repeated gentle shimmer in the air; evening blue.",
39: "Intercut feel in one move: Shuka pauses, eyes soften, then steps on; far behind the small father figure still following; long lens depth.",
40: "High crane pullback to god's-eye: two tiny figures entering golden road vs shaded road; forest enormous; very slow rise.",
41: "Concentric slow orbit around the seated young sage; petals drifting in current; dome of light breathing; water silver curls.",
42: "Light-wipe transformation: he steps INTO the golden shaft; motes swirling toward him; his silhouette passes through the light and emerges with softer brighter aura; slow elegant camera rise.",
43: "Low-angle halo framing: sun behind his topknot flaring; lotus flowers drifting to circle him; his stillness absolute; slow push with flare control.",
44: "Rising crane over hermits bowing while he carries firewood with a smile; his humility at center; courtyard life busy around.",
45: "Close on the yellow-tied bundle in hand, then slow tilt up to his eyes; disciples bowing deeply around; sacred quiet.",
46: "Profile steadying: his gaze travels to the forest through the window; lamplight flicker; manuscript weight in arms; held composition.",
47: "Aerial drift point of view of golden seeds of light rising off the manuscript and spilling across a stylized world of valleys and rivers; dream drift.",
48: "Slow single push toward the lamp: flame breathing small; the waiting manuscript; night hush deepening; gentle.",
49: "Court pan across lamps and sages then settling on the young king's attentive face; oil lamp flames flickering; he bows respectfully.",
50: "Wide vigil: sage rows motionless starlit, central seat empty; moth halo round the diya; the night expectant; barely-moving.",
51: "Close profile: evening wind tugs the shawl; his gaze steady to the west; beard brushing slowly; a knowing half-smile.",
52: "Ground-level track following bare feet on the mountain pass; evening dust swirling; golden haze pulsing subtle; certain rhythm.",
53: "Static extreme close: eyes lowered; single strand of hair moving in wind; peace absolute, almost sculpted.",
54: "Slow approach toward the cloud-island palace; lights flickering through haze; shadow vignette tightening; mystery growing.",
55: "Slow two-thirds pull-apart tension: king silhouette left, sage silhouette right, gold river winding between; dusk dimming at edges; suspense without fear.",
56: "Slow settling behind the dusk mandala: orb glowing behind the hermitage; fireflies drifting up; gentle tail fade; breathe-out ending.",
}

def mmss(x):
    m, s = divmod(float(x), 60)
    return f"{int(m):02d}:{s:04.1f}"

L = []
L.append("# EPISODE 4 — GOOGLE FLOW PRODUCTION KIT")
L.append("**Audio masters (use EP04_WITH_BGM.mp3 as the final timeline base in Flow):**")
L.append("- `episode04/EP04_WITH_BGM.mp3` — narration + 10-cue devotional score + river/birds ambience (7:32.99)")
L.append("- `episode04/EP04_CLEAN_VOICE.mp3` — narration only (if Flow adds its own underscore)")
L.append("")
L.append("**How to use:** each scene below = one Flow clip. Upload the listed keyframe image as the first frame, paste the ANIMATION PROMPT, generate ~6–8s, then trim to the audio span shown. Keep the film under the audio; the audio IS the timeline.")
L.append("")
L.append("## CHARACTER LOCKS (auto-included inside prompts):")
L.append(f"- VYASA — {VYASA}.")
L.append(f"- SHUKA — {SHUKA}.")
L.append("")
for s in sm['scenes']:
    n = s['n']
    L.append(f"## SCENE {n:02d} — {mmss(s['start'])} → {mmss(s['end'])} (span {(s['end']-s['start']):.1f}s)")
    if TXT.get(n):
        L.append(f"**Narration (Telugu):** {TXT[n]}")
    else:
        L.append("**Narration:** — (music/ambience only)")
    L.append(f"**Keyframe image:** `episode04/assets/EP04_S{n:02d}.jpg`")
    L.append(f"**IMAGE prompt (if regenerating the still):** {IMG[n]}")
    L.append(f"**ANIMATION prompt (paste into Google Flow):** {ANIM[n]}")
    L.append("")

out = os.path.join(ROOT, 'FLOW_PRODUCTION_KIT.md')
open(out, 'w', encoding='utf-8').write("\n".join(L))
print('WROTE', out, len("\n".join(L)), 'chars · scenes:', len(sm['scenes']))
