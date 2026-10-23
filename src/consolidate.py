#!/usr/bin/env python3
"""Align extracted blocks to the official 65-question key per paper and tag each question."""
import json, re, pathlib, collections

try:
    import wordninja
except Exception:  # optional dependency
    wordninja = None

def repair_glued(text):
    """OCR/scan output sometimes loses inter-word spaces: 'Considerthefollowingtable'."""
    if not wordninja:
        return text
    def fix(m):
        w = m.group(0)
        if len(w) < 14 or not w.isalpha():
            return w
        parts = wordninja.split(w)
        return " ".join(parts) if len(parts) > 1 else w
    return re.sub(r'[A-Za-z]{14,}', fix, text)

DATA = pathlib.Path("/home/user/youtube1/data")
qs_all = json.loads((DATA / "questions.json").read_text())
keys = json.loads((DATA / "keys.json").read_text())

# ------------------------------------------------------------------ overrides
def _junk(t):
    t = t.strip()
    if len(t) < 12:
        return True
    if re.search(r'carry\s*(one|two)\s*marks?', t, re.I) and len(t) < 70:
        return True
    return False

def _ga2016(bs):
    """2016 Set-1 file duplicates the CS paper and puts the GA section on pages 1-3."""
    ga, cs, seen = [], [], set()
    for b in bs:
        if b["page"] and b["page"] <= 3 and b["qno"] <= 10 and b["qno"] not in seen:
            ga.append(b); seen.add(b["qno"])
        elif b["page"] and 4 <= b["page"] <= 21:
            cs.append(b)
    return ga[:10] + cs[:55]

OVERRIDES = {"GATE_2016_CS_Set-1": _ga2016}

# ------------------------------------------------------------------ alignment
def expected_qnos(blocks):
    q = [b["qno"] for b in blocks]
    if len(q) > 55 and max(q) >= 60:
        return list(range(1, 66))
    return list(range(1, 11)) + list(range(1, 56))

def align(blocks, expected):
    out = [None] * len(expected)
    bi = ei = 0
    while ei < len(expected):
        exp = expected[ei]
        if bi >= len(blocks):
            ei += 1; continue
        b = blocks[bi]
        if _junk(b["text"]):
            bi += 1; continue
        if b["qno"] == exp:
            out[ei] = b; bi += 1; ei += 1; continue
        found = next((k for k in range(bi + 1, min(bi + 4, len(blocks))) if blocks[k]["qno"] == exp), None)
        if found is not None:
            bi = found; continue
        ei += 1
    return out

# ------------------------------------------------------------------ classifier
STRONG = {
 "DL": ["2's complement","two's complement","booth","flip-flop","flip flop","k-map","karnaugh","multiplexer","demultiplexer",
        "decoder","encoder","boolean function","boolean expression","logic gate","nand","nor gate","xor gate","sop form",
        "pos form","sequential circuit","combinational circuit","state diagram","ring counter","johnson counter","ieee 754",
        "ieee-754","floating point","normalized form","minterm","maxterm","don't care","shift register","latch","asm chart",
        "mealy","moore","saturating counter","up-counter","down-counter","ripple counter","sign-magnitude","sign magnitude",
        "radix","base-5","base 5","number system","binary representation","hexadecimal","octal","boolean variable",
        "boolean operator","boolean logic","carry lookahead","adder","half adder","full adder","multiplier circuit",
        "synchronous counter","toggle","t flip-flop","d flip-flop","j-k","radix-4","radix-5","base-5","base 5","base-3",
        "radix","2's complement representation","binary number","decimal representation","flip-flops"],
 "COA": ["cache","pipeline","hazard","stall","dma","interrupt","tlb","addressing mode","instruction format","cpi","speedup",
         "clock cycle","clock rate","branch predictor","register renaming","superscalar","microprogram","control unit",
         "alu","datapath","memory hierarchy","raid","disk access","sector","cylinder","word-addressable","byte-addressable",
         "little endian","big endian","miss rate","associative","write-back","write-through","effective memory access",
         "memory interleaving","i/o device","programmed i/o","cycle stealing","burst mode","dram","sram","chip select",
         "memory chip","address lines","execution time","machine cycle","instruction pipeline","out-of-order","instruction level",
         "register file","flash memory","hard disk","solid state","secondary storage","memory access time","opcode",
         "instruction format","general purpose registers","immediate operand","register operand","instruction word",
         "number of bits","bits are needed","bits required"],
 "OS": ["process","thread","semaphore","deadlock","mutual exclusion","critical section","context switch","scheduler",
        "scheduling algorithm","page fault","page replacement","thrashing","virtual memory","page table","demand paging",
        "segmentation","file system","inode","disk scheduling","fork()","producer-consumer","readers-writers","starvation",
        "preemptive","round robin","fcfs","sjf","srtf","working set","belady","dirty bit","logical address","physical address",
        "spin lock","monitor","banker","safe state","resource allocation graph","system call","kernel","shell","pipe",
        "memory management","frame","page size","page number","offset"],
 "TOC": ["regular expression","dfa","nfa","context-free","context free","cfg","pda","pushdown","turing machine","decidable",
         "undecidable","pumping lemma","myhill-nerode","regular language","recursively enumerable","halting problem",
         "closure properties","language accepted","grammar","derivation","parse tree","ambiguity","ambiguous grammar",
         "chomsky","finite automaton","finite automata","epsilon transition","minimization of dfa","countably infinite",
         "uncountable","regular grammar","left linear","language is","l = {","strings of"],
 "CN": ["tcp","udp","ip address","subnet","routing protocol","ethernet","crc","sliding window","congestion","dns","http",
        "arp","mac address","packet","datagram","fragment","ttl","csma","router","switch","ipv4","ipv6","bgp","ospf","nat",
        "socket","token bucket","leaky bucket","stop-and-wait","go-back-n","selective repeat","mtu","subnet mask","classless",
        "link-state","distance vector","three-way handshake","port number","application layer","transport layer","network layer",
        "data link layer","ip header","tcp header","bandwidth","propagation delay","transmission delay","queuing delay",
        "throughput","collision domain","broadcast domain","vpn","tls","dhcp","smtp","pop3","imap","ftp","802.11","rsa",
        "digital signature","cryptograph","public key","private key","gf(2)","polynomial","checksum","error detection",
        "flow control","mac protocol","wireless","multicast","broadcast","host","link of rate","bits/sec","bandwidth-delay",
        "round trip time","rtt","congestion window","slow start","ip datagram","fragmentation offset","mtu"],
 "DBMS": ["sql","relational algebra","normal form","bcnf","3nf","2nf","1nf","functional dependency","functional dependencies",
         "candidate key","superkey","primary key","foreign key","transaction","acid","serializable","conflict serializable",
         "concurrency control","two-phase locking","b+ tree","b+ trees","b-tree","index","er diagram","er model",
         "relational schema","tuple","trigger","view","join","rollback","log record","checkpoint","recovery","isolation level",
         "dirty read","phantom","lossless decomposition","dependency preservation","query optimization","aggregate",
         "group by","outer join","studentname","coursename","entity set","weak entity","owner entity","cardinality ratio",
         "schedule","write(x)","read(x)","recoverable","cascadeless","strict two-phase"],
 "CD": ["compiler","lexical analysis","lexical analyzer","parser","parsing","ll(1)","lr(0)","slr","lalr","clr",
        "shift-reduce","syntax tree","abstract syntax tree","intermediate code","three-address","three address","quadruple",
        "triple","code generation","code optimization","register allocation","liveness","data flow analysis","reaching definition",
        "available expression","activation record","linker","loader","peephole","constant folding","strength reduction",
        "common subexpression","dead code","symbol table","s-attributed","l-attributed","semantic analysis","left recursion",
        "left factoring","first set","follow set","handle","viable prefix","backpatching","dynamic linking","static linking",
        "relocation","assembler","macro expansion","basic block","control flow graph","static single assignment",
        "live variable","live variables","in(s)","out(s)","use(s)","lexeme","token","pattern matching","nfa to dfa",
        "regular expression to","parse table","recursive descent","operator precedence","yacc","lex","compiler design",
        "flow graph","loop invariant","induction variable","copy propagation","partial redundancy"],
 "EM-LA": ["matrix","determinant","eigenvalue","eigenvector","rank of","linearly independent","linear equations","trace of",
           "characteristic polynomial","diagonalizable","orthogonal matrix","symmetric matrix","singular value","null space",
           "column space","row space","invertible","singular matrix","vector space","basis","adjugate","column vectors",
           "linear combination","eigen","eigenvalues","eigenvectors","determinant of","matrix a","4 x 4","n x n","m x n",
           "system of linear equations","homogeneous"],
 "EM-PS": ["probability","random variable","probability density","probability mass","distribution","expectation","variance",
           "standard deviation","bayes","conditional probability","mutually independent","uniform distribution","normal distribution",
           "poisson","binomial","geometric distribution","exponential distribution","covariance","correlation","moment generating",
           "central limit","confidence interval","hypothesis","maximum likelihood","mean of","median","mode of","quartile",
           "fair coin","dice","tossed","randomly chosen","random experiment","expected number","probability that",
           "independently","uniformly distributed","normal random","exponential random","sample","population",
           "standard normal","z-score","p-value","bernoulli","coin is tossed","balls are drawn","cards are drawn"],
 "EM-CALC": ["limit","lim ","x→","x ->","dy/dx","d/dx","derivative","differentiable","continuity","continuous at","maxima",
             "minima","taylor","mean value theorem","rolle","gradient","divergence","curl","partial derivative",
             "increasing function","decreasing function","increasing everywhere","converges","diverges","∫","integral",
             "area bounded","power series","critical point","saddle point","hessian","lagrange multiplier","asymptote",
             "inflection","f(x)","f (x)","g(x)","real-valued function","real valued function","derivative of",
             "area of the region","bounded by","sin x","cos x","e^x","log x","series converges","monotonically",
             "supremum","infimum","differentiable at","continuous at x","limit of","as x approaches"],
 "DM": ["propositional","propositions","tautology","predicate logic","predicate calculus","quantifier","power set","set theory",
        "partial order","poset","lattice","equivalence relation","group","subgroup","cyclic group","ring","field",
        "homomorphism","pigeonhole","permutation","combination","binomial coefficient","generating function","inclusion-exclusion",
        "recurrence relation","graph theory","eulerian","hamiltonian","planar graph","chromatic number","bipartite","isomorphic",
        "degree of a vertex","spanning tree","vertices","edges","clique","vertex cover","matching","adjacency matrix",
        "connected component","counting","onto function","one-to-one","injective","surjective","number of relations",
        "boolean algebra","hasse diagram","first-order logic","first order logic","well-formed formula","logically equivalent",
        "logically implied","predicate","sets","subset","cardinality","relation r","binary relation","reflexive","symmetric",
        "transitive","colouring","coloring","edge-colour","edge color"],
 "ALGO": ["asymptotic","running time","worst case running","best case running","time complexity","space complexity","recurrence",
          "master theorem","quicksort","quick sort","merge sort","mergesort","heapsort","heap sort","insertion sort","bubble sort",
          "selection sort","counting sort","radix sort","dynamic programming","greedy","dijkstra","kruskal","prim's","floyd-warshall",
          "bellman-ford","np-complete","np-hard","np class","reduction","binary search","divide and conquer","minimum spanning tree",
          "shortest path","topological sort","huffman","activity selection","knapsack","longest common subsequence","matrix chain",
          "amortized","lower bound","comparison sort","string matching","kmp","rabin-karp","max flow","min cut","2-sat","bfs","dfs","edge weights","graph with edge","undirected graph with","weighted graph",
          "depth first search","breadth first search","depth-first","breadth-first","spanning tree weight","algorithm",
          "sort", "sorted order", "minimum number of comparisons", "asymptotically", "log n", "n log n", "o(n", "theta("],
 "PDS": ["pointer","array","linked list","stack","queue","binary tree","binary search tree","bst","heap","hash table","hashing",
         "struct","printf","malloc","c program","c code","c statements","inorder","preorder","postorder","leaf node","internal node",
         "recursion","recursive function","function call","stack frame","string","character array","typedef","union","enum",
         "dynamic memory","calloc","realloc","free()","dangling","memory leak","level order","avl","red-black","collision resolution",
         "open addressing","chaining","circular queue","priority queue","dequeue","adjacency list","pseudo-code","pseudocode",
         "int main","#include","dynamic scoping","call by reference","passed by reference","linked list","node of",
         "tree traversal","height of a tree","binary heap","min heap","max heap","unsigned long int","unsigned int",
         "char *","printf(","scanf(","c program","c code","array p[]","int a[","sizeof"],
}

def _norm(text):
    t = text.lower().replace("\u2019", "'").replace("\u2018", "'")
    t = t.replace("\u2013", "-").replace("\u2014", "-").replace("\u2212", "-")
    return re.sub(r'\s+', ' ', t)

ORDER = ["CD","DBMS","TOC","CN","OS","COA","DL","ALGO","EM-LA","EM-PS","EM-CALC","DM","PDS"]

def classify(text):
    t = " " + _norm(text) + " "
    scores = {}
    for subj, cues in STRONG.items():
        sc = 0.0
        for c in cues:
            n = t.count(c)
            if n:
                sc += min(n, 2) * (4 if len(c) > 8 else 3)
        scores[subj] = sc
    if not max(scores.values()):
        return "GEN", 0.0
    best = max(scores.values())
    for s in ORDER:
        if scores[s] >= best - 0.01:
            return s, best
    return max(scores, key=scores.get), best

# Manual labels for the zero-score questions (reviewed one by one)
MANUAL = ['DM', 'PDS', 'CN', 'DM', 'DM', 'DBMS', 'EM-LA', 'DL', 'DL', 'TOC', 'DM', 'DL', 'ALGO', 'TOC', 'DM', 'DM', 'DM', 'DL', 'ALGO', 'DL', 'EM-LA', 'ALGO', 'DL', 'DM', 'EM-CALC', 'EM-CALC']

# ------------------------------------------------------------------ build
_TAIL_JUNK = [
    re.compile(r'CS\s*\d+/\d+\s*GATE\s*\d{4}.*$', re.I),
    re.compile(r'GATE\s*\d{4}\s*COMPUTER SCIENCE.*$', re.I),
    re.compile(r'Computer Science (?:&|and) Information Technology.*$', re.I),
    re.compile(r'Organi[sz]ing Institute.*$', re.I),
    re.compile(r'Page\s*\d+\s*of\s*\d+.*$', re.I),
    re.compile(r'Copyright\s*©.*$', re.I),
]

def clean_text(t):
    t = re.sub(r'\s+', ' ', t).strip()
    changed = True
    while changed:
        changed = False
        for rx in _TAIL_JUNK:
            new = rx.sub('', t)
            if new != t:
                t = new.strip()
                changed = True
    return t

FIG_HINT = re.compile(r'(shown below|as shown|the figure|figure shows|shown in the|given figure|the given diagram|'
                      r'the table below|table below|following table|given table|circuit diagram|state transition table|'
                      r'control flow graph|adjacency matrix shown|following graph)', re.I)

def split_options(txt):
    idxs = [m.start() for m in re.finditer(r'\(A\)', txt)]
    if not idxs:
        # some stems lose the "(A)" marker: recover A..D when B, C and D are present
        marks = [(m.group(1), m.start()) for m in re.finditer(r'\(([A-D])\)', txt)]
        letters = [m[0] for m in marks]
        if letters[:3] == ["B", "C", "D"] or (len(letters) >= 3 and letters[:3] == ["B", "C", "A"]):
            b_pos = marks[0][1]
            head = txt[:b_pos]
            # option A text = trailing segment of the stem after the last sentence break
            m = re.search(r'(?:^|[.?!;]\s+)([^.?!;]{1,120})$', head)
            a_text = m.group(1) if m else ""
            stmt = head[:len(head) - len(a_text)].strip()
            opts = {"A": a_text.strip()}
            for n, (L, pos) in enumerate(marks):
                end = marks[n + 1][1] if n + 1 < len(marks) else len(txt)
                opts[L] = re.sub(r'\s+', ' ', txt[pos + 3:end]).strip()
            if all(len(v) < 400 for v in opts.values()):
                return stmt, {k: v for k, v in opts.items() if v}
    for i in idxs:
        tail = txt[i:]
        letters = {m.group(1): m.start() for m in re.finditer(r'\(([A-D])\)', tail)}
        if len(letters) >= 3 and "B" in letters:
            order = sorted(letters.items(), key=lambda kv: kv[1])
            opts = {}
            for n, (L, st) in enumerate(order):
                end = order[n + 1][1] if n + 1 < len(order) else len(tail)
                opts[L] = re.sub(r'\s+', ' ', tail[st + 3:end]).strip()
            if opts and all(len(v) < 400 for v in opts.values()):
                return txt[:i].strip(), opts
    return txt.strip(), {}

def main():
    final, zero_items = {}, []
    for prefix, payload in qs_all.items():
        blocks = payload["questions"]
        if prefix in OVERRIDES:
            blocks = OVERRIDES[prefix](blocks)
        aligned = align(blocks, expected_qnos(blocks))
        k = keys[prefix]
        out = []
        for i, b in enumerate(aligned):
            key = k[i]
            if b is None:
                out.append({"pos": i+1, "missing": True, "type": key["type"], "marks": key["marks"],
                            "section": key["section"], "answer": key["key"], "text": "", "stmt": "",
                            "options": {}, "page": None, "subject": "GEN", "score": 0})
                continue
            txt = re.sub(r'Q\.?\s*\d+\s*[-–]\s*Q\.?\s*\d+\s+Carry[^.]*?each\.?', ' ', b["text"], flags=re.I)
            txt = clean_text(txt)
            ocr_pages = payload.get("ocr_pages") or []
            if b.get("page") in ocr_pages:
                txt = repair_glued(txt)
            stmt, opts = split_options(txt)
            stmt = clean_text(stmt)
            opts = {k: clean_text(v) for k, v in opts.items()}
            fig = bool(FIG_HINT.search(txt))
            subj, score = classify(txt)
            rec = {"pos": i+1, "qno": b["qno"], "type": key["type"], "marks": key["marks"],
                   "section": key["section"], "answer": key["key"], "text": txt, "stmt": stmt,
                   "options": opts, "page": b["page"], "subject": subj, "score": score, "missing": False,
                   "ocr": b.get("page") in (payload.get("ocr_pages") or []), "figure": fig}
            if score == 0 and key["section"] != "GA":
                zero_items.append((out, len(out)))
            out.append(rec)
        for rec in out:
            a = rec["answer"]
            m = re.fullmatch(r'(-?[\d.]+)\s*to\s*(-?[\d.]+)', a)
            if m:
                lo, hi = m.group(1), m.group(2)
                rec["answer"] = lo if lo == hi else f"{lo} – {hi}"
        final[prefix] = {"file": payload["file"], "questions": out}

    # apply manual labels in order
    assert len(zero_items) == len(MANUAL), f"{len(zero_items)} zero-score vs {len(MANUAL)} labels"
    for (lst, idx), lab in zip(zero_items, MANUAL):
        lst[idx]["subject"] = lab

    (DATA / "final_questions.json").write_text(json.dumps(final, indent=1))

    tot = sum(len(v["questions"]) for v in final.values())
    miss = sum(q["missing"] for v in final.values() for q in v["questions"])
    print(f"TOTAL questions: {tot}  missing text: {miss}")
    c = collections.Counter(q["subject"] for v in final.values() for q in v["questions"]
                            if q["section"] != "GA" and not q["missing"])
    print("CS tags:", dict(c.most_common()))
    print("GA:", sum(1 for v in final.values() for q in v["questions"] if q["section"] == "GA"))

if __name__ == "__main__":
    main()
