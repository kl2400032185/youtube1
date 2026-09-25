"""Create print/share-ready subject study sheets as PNGs.

The sheets are rendered directly to high-resolution PNGs with Pillow for easy
sharing in the browser and on mobile.
"""
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parents[1] / "assets" / "subject-cards"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 1800, 2700
BG = "#f6f8f3"
INK = "#12211f"
SOFT = "#41514e"
MUTED = "#75817d"
LINE = "#dfe6dc"
FOREST = "#143d35"
FOREST_2 = "#1d594a"
MINT = "#d9f27e"
CORAL = "#ec765d"
AMBER = "#e8b65b"
SKY = "#8fc3c4"
WHITE = "#ffffff"

subjects = [
    {
        "number": "01", "slug": "engineering-mathematics", "name": ["Engineering", "Mathematics"],
        "short": "MATH", "accent": "#3d8369", "focus": "Translate words into structure; check the invariant before calculating.",
        "topics": [("Propositional + first-order logic", "MUST"), ("Sets, relations, functions", "MUST"), ("Posets and lattices", "HIGH"), ("Monoids and groups", "HIGH"), ("Graph connectivity, matching, colouring", "MUST"), ("Counting + inclusion–exclusion", "MUST"), ("Recurrences + generating functions", "HIGH"), ("Matrices, determinants, linear systems", "MUST"), ("Eigenvalues + eigenvectors", "HIGH"), ("LU decomposition", "BUILD"), ("Limits, MVT, extrema, integration", "MUST"), ("Random variables + five distributions", "MUST"), ("Mean, median, mode, SD", "HIGH"), ("Conditional probability + Bayes", "MUST")],
        "questions": [
            ("COUNT / RECURRENCE", "How many binary strings of length n contain no consecutive 1s? Give a recurrence and base cases.", "aₙ=aₙ₋₁+aₙ₋₂; a₀=1, a₁=2; answer Fₙ₊₂."),
            ("GRAPH PROPERTY", "A connected graph has exactly two odd-degree vertices. What does this guarantee?", "An Euler trail, but not an Euler circuit."),
            ("MATRIX / EIGENVALUE", "For [[2,1],[0,2]], how many independent eigenvectors exist?", "One: eigenvalue 2 has a one-dimensional eigenspace."),
            ("BAYES", "Prevalence 1%, sensitivity 99%, false positive 5%. Find P(disease | positive).", "0.0099/(0.0099+0.0495)=1/6≈16.67%.")
        ]
    },
    {
        "number": "02", "slug": "digital-logic", "name": ["Digital", "Logic"],
        "short": "DL", "accent": "#c4775c", "focus": "Simplify first; design second; verify the circuit with a table.",
        "topics": [("Boolean algebra + duality", "MUST"), ("K-map minimisation", "MUST"), ("Quine–McCluskey tabular method", "HIGH"), ("MUX, decoder, encoder, comparator", "MUST"), ("Parity + code converters", "HIGH"), ("Half/full adders", "HIGH"), ("SR, JK, D, T flip-flops", "MUST"), ("FSM state design", "MUST"), ("Counters + registers", "HIGH"), ("2s complement + overflow", "MUST"), ("Fixed + floating point", "HIGH")],
        "questions": [
            ("MINIMISE", "Simplify Σm(0,2,8,10)+d(1,3,9,11).", "F=B′; use the don't-cares to group every cell with B=0."),
            ("MUX OUTPUT", "A 2:1 MUX has D0=A, D1=¬A, select S=B. Find F.", "F=B′A+B¬A=A XOR B."),
            ("SEQUENTIAL", "D=Q XOR X; Q₀=0; X=1 for two edges, then 0. Final Q?", "States: 1, 0, 0; final Q=0."),
            ("NUMBER SYSTEM", "Add 01111111 and 00000001 as 8-bit 2s complement.", "10000000 with signed overflow." )
        ]
    },
    {
        "number": "03", "slug": "computer-organization", "name": ["Computer", "Organization"],
        "short": "COA", "accent": "#8b6fa9", "focus": "Draw the path: instruction → data → timing.",
        "topics": [("Instruction formats + addressing modes", "MUST"), ("Effective address calculation", "MUST"), ("ALU + flags", "HIGH"), ("Hardwired control", "HIGH"), ("Microprogrammed control", "HIGH"), ("Memory hierarchy + AMAT", "MUST"), ("Direct / set / fully associative cache", "MUST"), ("Tag, index, offset fields", "MUST"), ("Write policies + dirty blocks", "HIGH"), ("Interrupts + DMA", "MUST"), ("Pipeline speedup + CPI", "MUST"), ("Structural, data, control hazards", "MUST")],
        "questions": [
            ("CACHE NUMERICAL", "32-bit byte address; 1 KiB direct cache; 16-byte lines. Tag/index/offset?", "22 tag bits, 6 index bits, 4 offset bits."),
            ("PIPELINE TIMING", "A 5-stage pipeline runs 100 independent instructions with no stalls. Cycles?", "104 cycles; ideal speedup 500/104≈4.81."),
            ("EFFECTIVE ADDRESS", "LOAD R1,20(R2), R2=1000. Effective address and reads?", "EA=1020; one operand-memory read."),
            ("I/O", "A 1 MiB transfer interrupts once per 4 KiB block. How many interrupts?", "256 interrupts." )
        ]
    },
    {
        "number": "04", "slug": "programming-data-structures", "name": ["Programming", "& Data Structures"],
        "short": "PDS", "accent": "#d1924f", "focus": "Trace state, pointers, invariants, and cost—not just syntax.",
        "topics": [("C arrays, pointers, strings, structs", "MUST"), ("Recursion + call stack", "MUST"), ("Arrays, stacks, queues", "MUST"), ("Linked lists", "MUST"), ("Tree traversals", "MUST"), ("Binary search trees", "MUST"), ("Binary heaps", "HIGH"), ("Graph representations", "HIGH"), ("Operation time + space", "HIGH")],
        "questions": [
            ("C TRACE", "int a[]={1,2,3}; int *p=a; (*p)++; p++; printf(\"%d %d\",a[0],*p);", "Prints 2 2."),
            ("RECURSION", "Solve T(n)=T(n−1)+n with T(0)=1.", "T(n)=1+n(n+1)/2, so Θ(n²) time and Θ(n) stack."),
            ("MIN-HEAP", "Insert 5,3,8,1,4 into an empty min-heap. Array?", "[1,3,8,5,4]."),
            ("STRUCTURE CHOICE", "Need O(1) index lookup and frequent middle insertion. Which trade-off?", "Array: lookup O(1), insert O(n); list: lookup O(n), insert O(1) once located." )
        ]
    },
    {
        "number": "05", "slug": "algorithms", "name": ["Algorithms"],
        "short": "ALG", "accent": "#5c8e9c", "focus": "State the invariant or recurrence before you execute the algorithm.",
        "topics": [("Worst-case time + space", "MUST"), ("Searching + boundary cases", "MUST"), ("Sorting + stability", "MUST"), ("Hashing + collisions", "HIGH"), ("Divide and conquer", "MUST"), ("Greedy + exchange argument", "MUST"), ("Dynamic programming", "MUST"), ("BFS + DFS", "MUST"), ("MST: Kruskal + Prim", "MUST"), ("Shortest paths", "MUST")],
        "questions": [
            ("COMPLEXITY", "What is the order of: i=1..n; j=1; j≤i; j*=2?", "Θ(n log n)."),
            ("GREEDY", "Which rule maximises the number of interval-scheduling activities?", "Repeatedly choose the compatible interval with earliest finish."),
            ("DYNAMIC PROGRAMMING", "0/1 knapsack W=5; items (2,3),(3,4),(4,5). Maximum value?", "7 by taking the first two items."),
            ("SHORTEST PATH", "Edges AB=1, AC=4, BC=2. Distances from A?", "d(A)=0, d(B)=1, d(C)=3 via B." )
        ]
    },
    {
        "number": "06", "slug": "theory-of-computation", "name": ["Theory of", "Computation"],
        "short": "TOC", "accent": "#7f79a7", "focus": "Classify the language before building the machine or proof.",
        "topics": [("Regular expressions", "MUST"), ("DFA, NFA, ε-NFA", "MUST"), ("Subset construction", "MUST"), ("DFA minimisation", "HIGH"), ("Regular-language closure", "MUST"), ("CFG derivations + parse trees", "MUST"), ("PDA + stack behaviour", "HIGH"), ("Pumping lemma", "MUST"), ("Turing machines", "HIGH"), ("Undecidability + reductions", "MUST")],
        "questions": [
            ("REGEX", "Give a regex over {0,1} for strings ending in 01.", "(0|1)*01."),
            ("MINIMISATION", "A reachable DFA has 8 states; refinement gives 5 equivalence classes. Minimum states?", "5 states."),
            ("PUMPING LEMMA", "Is {0ⁿ1ⁿ | n≥0} regular? State the proof idea.", "No; pumping changes the number of 0s but not 1s."),
            ("REDUCTION", "If HALT ≤m L and L is decidable, what follows?", "HALT would be decidable; therefore L is undecidable." )
        ]
    },
    {
        "number": "07", "slug": "compiler-design", "name": ["Compiler", "Design"],
        "short": "CD", "accent": "#bd7180", "focus": "Track information as it moves from source text to executable form.",
        "topics": [("Lexical analysis + longest match", "MUST"), ("FIRST + FOLLOW", "MUST"), ("LL(1) parsing", "MUST"), ("LR conflicts", "MUST"), ("Syntax-directed translation", "HIGH"), ("Activation records + scope", "MUST"), ("Three-address code", "MUST"), ("Basic blocks + CFG", "MUST"), ("Constant propagation + folding", "HIGH"), ("Liveness analysis", "MUST"), ("Common subexpression elimination", "HIGH")],
        "questions": [
            ("LEXER", "With '=' and '==' rules, how is a==b tokenised under longest match?", "identifier, ==, identifier; the two-character token wins."),
            ("FIRST / FOLLOW", "For S→AB, A→aA|ε, B→b|ε, find FIRST(S), FOLLOW(A), FOLLOW(B).", "FIRST(S)={a,b,ε}; FOLLOW(A)={b,$}; FOLLOW(B)={$}."),
            ("THREE-ADDRESS CODE", "Generate TAC for x=a+b*c.", "t1=b*c; t2=a+t1; x=t2."),
            ("DATA FLOW", "After x=1; y=x+2; print(y), what constants are known?", "x=1 and y=3; the addition can fold to print(3)." )
        ]
    },
    {
        "number": "08", "slug": "operating-systems", "name": ["Operating", "Systems"],
        "short": "OS", "accent": "#668d74", "focus": "Draw the process state, ready queue, resource graph, or address translation.",
        "topics": [("System calls + user/kernel mode", "MUST"), ("Processes + threads", "MUST"), ("IPC", "HIGH"), ("Race conditions + semaphores", "MUST"), ("Deadlock + Banker", "MUST"), ("CPU scheduling", "MUST"), ("I/O scheduling", "HIGH"), ("Paging + page tables", "MUST"), ("Virtual memory + replacement", "MUST"), ("File systems + allocation", "MUST")],
        "questions": [
            ("SCHEDULING", "SRTF: P1 arrives 0/burst 5; P2 arrives 1/burst 2. Schedule and waits?", "P1 0–1, P2 1–3, P1 3–7; waits P1=2, P2=0."),
            ("RACE", "Two threads read x=0, add one, and write without a lock. Possible final values?", "1 or 2; a lost update can occur."),
            ("DEADLOCK", "P1 holds (1,0), needs (2,1); P2 holds (0,1), needs (1,1); available (0,0). Safe?", "No; neither remaining need fits, so the state is unsafe."),
            ("PAGING", "With 2 FIFO frames, count faults for 1,2,1,3,1.", "4 faults." )
        ]
    },
    {
        "number": "09", "slug": "databases", "name": ["Data", "bases"],
        "short": "DB", "accent": "#4d8e8e", "focus": "Make the data model explicit before writing the query or schedule proof.",
        "topics": [("ER model + cardinality", "MUST"), ("Relational model + keys", "MUST"), ("Integrity constraints", "MUST"), ("Relational algebra", "MUST"), ("Tuple calculus + SQL", "MUST"), ("NULL + aggregation", "MUST"), ("FDs + candidate keys", "MUST"), ("2NF, 3NF, BCNF", "MUST"), ("File organisation", "HIGH"), ("B / B+ tree indexes", "MUST"), ("Transactions + serializability", "MUST"), ("Concurrency control", "HIGH")],
        "questions": [
            ("SQL RESULT", "For rows (1,10),(2,NULL),(3,20), what are COUNT(*) and COUNT(score)?", "COUNT(*)=3; COUNT(score)=2 because NULL is ignored."),
            ("NORMAL FORMS", "R(A,B,C), A→B and B→C. Key and highest normal form?", "A is a key; 2NF but not 3NF because B→C violates 3NF."),
            ("ER MAPPING", "In a 1:N Department–Employee relationship, where does the foreign key go?", "Department's key goes as NOT NULL FK in Employee, the N-side."),
            ("SERIALIZABILITY", "Schedule r1(X),w1(X),r2(X),w2(X): conflict-serializable?", "Yes; precedence graph has only T1→T2." )
        ]
    },
    {
        "number": "10", "slug": "computer-networks", "name": ["Computer", "Networks"],
        "short": "CN", "accent": "#4b7caa", "focus": "Follow the packet and count every boundary, bit, window, and round trip.",
        "topics": [("Layering + encapsulation", "MUST"), ("Switching + delay metrics", "HIGH"), ("Framing + CRC/checksum", "MUST"), ("MAC + Ethernet", "MUST"), ("Distance-vector routing", "MUST"), ("Link-state routing", "MUST"), ("IPv4 + fragmentation", "MUST"), ("CIDR + longest-prefix match", "MUST"), ("NAT", "HIGH"), ("TCP flow control", "MUST"), ("TCP congestion control", "MUST"), ("Sockets, DNS + HTTP", "MUST")],
        "questions": [
            ("CIDR", "For 192.168.10.0/26, range and usable host count?", "Range .0–.63; usable .1–.62: 62 hosts."),
            ("ROUTING", "A–B=1, B–C=2, A–C=4. Next hop and cost A→C?", "Next hop B, cost 3."),
            ("TCP WINDOW", "rwnd=4000 bytes and cwnd=6000 bytes. Maximum send window?", "min(rwnd,cwnd)=4000 bytes."),
            ("CRC", "For data 1101 and generator 1011, what remainder is appended?", "001."),
            ("TCP + HTTP", "What must complete before a normal HTTP request on a new TCP connection?", "The three-way handshake: SYN, SYN-ACK, ACK." )
        ]
    },
]


def wrap(text: str, max_chars: int):
    words = text.split()
    lines, line = [], ""
    for word in words:
        candidate = f"{line} {word}".strip()
        if line and len(candidate) > max_chars:
            lines.append(line)
            line = word
        else:
            line = candidate
    if line:
        lines.append(line)
    return lines or [""]



FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")
FONT_REGULAR = FONT_DIR / "DejaVuSans.ttf"
FONT_BOLD = FONT_DIR / "DejaVuSans-Bold.ttf"
FONT_MONO = FONT_DIR / "DejaVuSansMono.ttf"
FONT_MONO_BOLD = FONT_DIR / "DejaVuSansMono-Bold.ttf"
_font_cache = {}


def pil_font(size, bold=False, mono=False):
    key = (size, bold, mono)
    if key not in _font_cache:
        path = FONT_MONO_BOLD if mono and bold else FONT_MONO if mono else FONT_BOLD if bold else FONT_REGULAR
        _font_cache[key] = ImageFont.truetype(str(path), size)
    return _font_cache[key]


def draw_wrapped(draw, xy, text, size, fill, max_chars, bold=False, mono=False, spacing=7):
    font = pil_font(size, bold=bold, mono=mono)
    lines = text if isinstance(text, list) else wrap(text, max_chars)
    draw.multiline_text(xy, "\n".join(lines), font=font, fill=fill, spacing=spacing)
    line_height = size + spacing
    return xy[1] + (len(lines) - 1) * line_height + size


def draw_centered(draw, box, text, size, fill, bold=False, mono=False):
    font = pil_font(size, bold=bold, mono=mono)
    left, top, right, bottom = box
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((left + right - tw) / 2 - bbox[0], (top + bottom - th) / 2 - bbox[1]), text, font=font, fill=fill)


def render_png(subject, output):
    image = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(image)
    accent = subject["accent"]

    # Decorative background and hero.
    draw.ellipse((1460, -60, 1820, 300), fill="#eaf0e8", outline=None)
    draw.ellipse((1530, 10, 1750, 230), outline="#c8d9c4", width=3)
    draw.rounded_rectangle((70, 70, 1730, 640), radius=30, fill=FOREST)
    draw.rounded_rectangle((70, 70, 85, 640), radius=7, fill=accent)
    draw_wrapped(draw, (130, 125), "GATE CS 2027  /  RANKROOM STUDY SHEET", 23, MINT, 90, bold=True, mono=True, spacing=3)
    title_font = pil_font(84, bold=True)
    draw.multiline_text((130, 205), "\n".join(subject["name"]), font=title_font, fill=WHITE, spacing=8)
    title_bottom = 205 + len(subject["name"]) * 92
    draw_wrapped(draw, (130, title_bottom + 15), subject["focus"], 25, "#b0c4b9", 74, spacing=8)
    draw.rounded_rectangle((130, 515, 375, 572), radius=12, fill=MINT)
    draw_centered(draw, (130, 515, 375, 572), "TARGET  < 1000", 22, FOREST, bold=True)
    draw.text((1608, 168), subject["number"], font=pil_font(154, bold=True), fill=MINT, anchor="ra")
    draw.text((1608, 554), subject["short"], font=pil_font(27, bold=True, mono=True), fill="#8fa99d", anchor="ra")

    # Checklist.
    draw_wrapped(draw, (90, 730), "01  /  CHECKLIST", 22, FOREST_2, 30, bold=True, mono=True, spacing=3)
    draw_wrapped(draw, (90, 780), "Don’t leave these open", 42, INK, 40, bold=True, spacing=6)
    draw.line((90, 850, 1710, 850), fill=LINE, width=2)
    rows = (len(subject["topics"]) + 1) // 2
    row_height = 78
    topic_y = 910
    for i, (topic, priority) in enumerate(subject["topics"]):
        col, row = i // rows, i % rows
        x, y = 100 + col * 810, topic_y + row * row_height
        draw.rounded_rectangle((x, y - 31, x + 34, y + 3), radius=9, fill="#e6f2d3")
        draw_centered(draw, (x, y - 31, x + 34, y + 3), "✓", 20, FOREST_2, bold=True)
        draw_wrapped(draw, (x + 51, y - 8), topic, 21, INK, 39, bold=True, spacing=3)
        badge_fill = {"MUST": "#f8e3de", "HIGH": "#f8edcf", "BUILD": "#dceff0"}[priority]
        badge_text = {"MUST": "#9d4e3d", "HIGH": "#8b6825", "BUILD": "#467d7f"}[priority]
        bx = x + 690
        draw.rounded_rectangle((bx, y - 28, bx + 100, y - 2), radius=6, fill=badge_fill)
        draw_centered(draw, (bx, y - 28, bx + 100, y - 2), priority, 13, badge_text, bold=True, mono=True)

    checklist_end = topic_y + rows * row_height - 16
    q_heading_y = checklist_end + 105
    draw_wrapped(draw, (90, q_heading_y), "02  /  ACTIVE RECALL", 22, FOREST_2, 30, bold=True, mono=True, spacing=3)
    draw_wrapped(draw, (90, q_heading_y + 50), "Most expected question shapes", 42, INK, 40, bold=True, spacing=6)
    draw.text((1710, q_heading_y + 40), "TRY COLD  →  REVEAL  →  LOG THE MISS", font=pil_font(17, mono=True), fill=MUTED, anchor="ra")
    q_top, q_height = q_heading_y + 105, 190
    for i, (kind, prompt, answer) in enumerate(subject["questions"]):
        y = q_top + i * q_height
        fill = WHITE if i % 2 == 0 else "#eef3eb"
        draw.rounded_rectangle((90, y, 1710, y + 165), radius=16, fill=fill, outline=LINE, width=2)
        draw.rounded_rectangle((115, y + 25, 360, y + 58), radius=7, fill=accent)
        draw_centered(draw, (115, y + 25, 360, y + 58), kind, 14, WHITE, bold=True, mono=True)
        draw_wrapped(draw, (395, y + 28), prompt, 21, INK, 75, bold=True, spacing=3)
        draw_wrapped(draw, (395, y + 105), "ANSWER  /  " + answer, 16, SOFT, 112, spacing=3)
        draw.text((1650, y + 28), f"{i + 1:02d}", font=pil_font(18, bold=True, mono=True), fill=accent, anchor="ra")

    footer_y = q_top + len(subject["questions"]) * q_height + 35
    draw.line((90, footer_y, 1710, footer_y), fill=LINE, width=2)
    draw.text((90, footer_y + 35), "THE LOOP", font=pil_font(18, bold=True, mono=True), fill=CORAL)
    draw_wrapped(draw, (250, footer_y + 35), "Learn  →  retrieve  →  solve timed  →  classify the miss  →  retest in 72 hours", 21, INK, 100, bold=True, spacing=3)
    draw.text((1710, footer_y + 35), "OFFICIAL PYQs FIRST", font=pil_font(17, mono=True), fill=MUTED, anchor="ra")
    image.save(output, format="PNG", optimize=True)


for subject in subjects:
    png_path = OUT / f"{subject['number']}-{subject['slug']}.png"
    render_png(subject, png_path)
    print(png_path)
