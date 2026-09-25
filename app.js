const subjects = [
  {
    id: "math", number: "01", short: "MATH", abbr: "M", name: "Engineering Mathematics", color: "#3d8369",
    description: "Logic, algebra, calculus & probability",
    focus: "Scoring foundation: translate words into structure.",
    topics: [
      ["logic", "Propositional logic and proof patterns", "Implication, equivalence, CNF/DNF, validity, contradiction.", "must"],
      ["sets", "Sets, relations and functions", "Closures, equivalence relations, injective/surjective/bijective maps.", "must"],
      ["posets", "Partial orders and lattices", "Hasse diagrams, maximal/minimal elements, meet and join.", "high"],
      ["algebra", "Monoids and groups", "Operation tables, identity, inverse, subgroups and basic properties.", "high"],
      ["graphs", "Connectivity, matching and colouring", "Components, degree facts, bipartite tests, matchings and chromatic ideas.", "must"],
      ["counting", "Counting and combinatorics", "Pigeonhole, permutations, combinations, inclusion–exclusion.", "must"],
      ["recurrence", "Recurrence relations and generating functions", "Solve standard recurrences; extract coefficients and recognise patterns.", "high"],
      ["matrices", "Matrices, determinants and linear systems", "Rank, consistency, elimination and determinant properties.", "must"],
      ["eigen", "Eigenvalues and eigenvectors", "Characteristic polynomial, eigenspaces, trace/determinant checks.", "high"],
      ["lu", "LU decomposition", "Triangular solves, pivoting intuition and operation count.", "build"],
      ["calculus", "Limits, continuity and differentiability", "One-sided limits, continuity tests and differentiability conditions.", "must"],
      ["mvt", "Maxima, minima and mean value theorem", "Critical points, boundary checks and theorem hypotheses.", "high"],
      ["integration", "Integration", "Definite integrals, area, substitutions and standard forms.", "must"],
      ["probability", "Random variables and distributions", "Binomial, Poisson, uniform, normal, exponential; expectation and variance.", "must"],
      ["stats", "Descriptive statistics", "Mean, median, mode, variance and standard deviation; effect of transformations.", "high"],
      ["bayes", "Conditional probability and Bayes theorem", "Independence, total probability and posterior updates.", "must"]
    ],
    questionTypes: [
      { type: "Count / recurrence", pattern: "Turn a counting story into a recurrence or inclusion–exclusion expression.", why: "The trap is counting overlapping cases twice or choosing the wrong base case.", method: "Define the state precisely; list the first two small cases before simplifying.", difficulty: "High", tags: ["counting", "recurrence"] },
      { type: "Graph property", pattern: "Given degrees or a graph description, infer connectivity, bipartiteness, matching, or colouring facts.", why: "A local degree fact can constrain the whole graph; do not draw more than the statement gives you.", method: "Write the invariant first: degree sum, odd-cycle test, component count, or Hall-style condition.", difficulty: "High", tags: ["graphs", "invariant"] },
      { type: "Matrix / eigenvalue", pattern: "Find rank, consistency, eigenvalues, or a quantity derived from a matrix without full expansion.", why: "Trace, determinant, row operations, and triangular structure often remove most calculation.", method: "Check structure and invariants before computing a characteristic polynomial.", difficulty: "Medium", tags: ["linear algebra", "shortcut"] },
      { type: "Probability update", pattern: "Compute a conditional probability, posterior, or distribution statistic from a short experiment.", why: "The common miss is confusing P(A|B) with P(B|A), or using independence without evidence.", method: "Name the sample space; write Bayes or total probability symbolically before numbers.", difficulty: "High", tags: ["Bayes", "distributions"] },
      { type: "Calculus decision", pattern: "Use continuity, MVT, extrema, or an integral to decide a value or property.", why: "The theorem's hypotheses and endpoint checks matter as much as differentiation.", method: "State domain and hypotheses, then differentiate / integrate and verify candidates.", difficulty: "Medium", tags: ["calculus", "MVT"] }
    ]
  },
  {
    id: "logic", number: "02", short: "DL", abbr: "D", name: "Digital Logic", color: "#c4775c",
    description: "Boolean design, arithmetic & FSMs",
    focus: "Simplify first; design second; verify with a table.",
    topics: [
      ["boolean", "Boolean algebra and duality", "Laws, De Morgan, consensus, canonical SOP/POS forms.", "must"],
      ["kmap", "Karnaugh map minimisation", "Groups, wrap-around, don't-cares, hazards and minimal forms.", "must"],
      ["tabular", "Tabular / Quine–McCluskey method", "Prime implicants, essential implicants and systematic minimisation.", "high"],
      ["comb", "Combinational circuit building blocks", "MUX, decoder, encoder, comparator, parity and code converters.", "must"],
      ["adder", "Adders and arithmetic circuits", "Half/full adders, ripple carry, carry look-ahead intuition.", "high"],
      ["latch", "Latches and flip-flops", "SR, JK, D, T behaviour, excitation and characteristic tables.", "must"],
      ["fsm", "Sequential circuit / FSM design", "State diagram, state table, encoding, next-state and output logic.", "must"],
      ["counter", "Counters and registers", "Synchronous/asynchronous counters, mod-n design, shift registers.", "high"],
      ["number", "Number representation and arithmetic", "Bases, signed magnitude, 1s/2s complement, overflow and subtraction.", "must"],
      ["float", "Fixed and floating-point representation", "Normalisation, exponent bias, precision and representable range.", "high"]
    ],
    questionTypes: [
      { type: "Minimise", pattern: "Minimise a Boolean function with minterms, maxterms, and don't-care terms.", why: "One missed adjacency or illegal group creates a non-minimal answer.", method: "Mark all cells, form largest legal groups first, then cover isolated minterms.", difficulty: "High", tags: ["K-map", "SOP/POS"] },
      { type: "Circuit output", pattern: "Find the output of a MUX / decoder / comparator network for a given input.", why: "Select-line ordering and active-low notation are the usual traps.", method: "Rewrite the block as an equation and evaluate from the inside out.", difficulty: "Medium", tags: ["MUX", "combinational"] },
      { type: "FSM / counter", pattern: "Derive next state, sequence, or required flip-flop inputs for a sequential circuit.", why: "Current-state versus next-state labels are easy to swap.", method: "Make a state table; derive excitation inputs row by row; mark unused states.", difficulty: "High", tags: ["FSM", "flip-flop"] },
      { type: "Representation", pattern: "Convert a signed integer or floating-point word and test overflow / range.", why: "Carry out is not always overflow; exponent bias and hidden bits matter.", method: "Separate sign, magnitude/exponent, and fraction. Check the target format first.", difficulty: "Medium", tags: ["2s complement", "floating point"] }
    ]
  },
  {
    id: "coa", number: "03", short: "COA", abbr: "C", name: "Computer Organization", color: "#8b6fa9",
    description: "Datapath, memory, I/O & pipelines",
    focus: "Draw the path: instruction → data → timing.",
    topics: [
      ["isa", "Instruction set and addressing modes", "Instruction formats, effective address, immediate, indirect and indexed modes.", "must"],
      ["alu", "ALU and arithmetic datapath", "Adder/subtractor, flags, shifts, multiplication/division intuition.", "high"],
      ["control", "Hardwired and microprogrammed control", "Control signals, sequencing, microinstructions and trade-offs.", "high"],
      ["memory", "Memory hierarchy and performance", "Locality, hit time, miss penalty, AMAT and hierarchy comparisons.", "must"],
      ["cache", "Cache mapping and replacement", "Direct, set-associative, fully associative; tag/index/offset.", "must"],
      ["write", "Cache write policies", "Write-through/back, allocate/no-allocate and dirty blocks.", "high"],
      ["interface", "Memory interfacing", "Address decoding, chip select, address/data bus and capacity.", "build"],
      ["interrupt", "Interrupt-driven I/O and DMA", "Priority, vectored interrupts, cycle stealing and transfer paths.", "must"],
      ["pipeline", "Instruction pipelining", "Speedup, throughput, latency, ideal and non-ideal CPI.", "must"],
      ["hazard", "Pipeline hazards", "Structural, data and control hazards; forwarding, stalls and branch penalties.", "must"]
    ],
    questionTypes: [
      { type: "Cache numericals", pattern: "From address width, line size, cache size, and associativity, find tag/index/offset or hit/miss.", why: "A single unit conversion or bit-field error invalidates the entire answer.", method: "Write address = tag | set | byte/word offset; compute each field independently.", difficulty: "High", tags: ["cache", "AMAT"] },
      { type: "Pipeline timing", pattern: "Compute cycles, speedup, CPI, or stalls for a sequence with data and branch hazards.", why: "Forwarding does not remove every load-use or control hazard.", method: "Draw the instruction-by-cycle grid; annotate the exact dependency before inserting bubbles.", difficulty: "High", tags: ["pipeline", "hazards"] },
      { type: "Effective address", pattern: "Evaluate an instruction's effective address and identify memory accesses for an addressing mode.", why: "The operand value, address, and number of accesses are different quantities.", method: "Label registers before and after; track PC-relative and indirect steps explicitly.", difficulty: "Medium", tags: ["ISA", "addressing"] },
      { type: "I/O / control", pattern: "Compare interrupt, polling, and DMA timing or choose a control implementation.", why: "CPU involvement and transfer ownership are the deciding variables.", method: "Trace who moves each word and when the CPU is blocked or interrupted.", difficulty: "Medium", tags: ["DMA", "control unit"] }
    ]
  },
  {
    id: "programming", number: "04", short: "PDS", abbr: "P", name: "Programming & Data Structures", color: "#d1924f",
    description: "C, recursion, trees, heaps & graphs",
    focus: "Trace state, not just syntax.",
    topics: [
      ["c", "C fundamentals and pointer tracing", "Arrays, pointers, strings, structs, precedence, call-by-value and memory layout.", "must"],
      ["recursion", "Recursion and call stacks", "Base cases, stack frames, recurrence, return order and tail behaviour.", "must"],
      ["arrays", "Arrays, stacks and queues", "Indexing, circular queues, implementation and operation cost.", "must"],
      ["lists", "Linked lists", "Insertion/deletion, pointer updates, doubly/circular variants.", "must"],
      ["trees", "Trees and traversals", "Pre/in/post/level order, height, subtree sizes and reconstruction.", "must"],
      ["bst", "Binary search trees", "Search, insert, delete, predecessor/successor and worst-case shape.", "must"],
      ["heap", "Binary heaps", "Heap property, build-heap, insert, delete, heap sort and priority queues.", "high"],
      ["graphs", "Graph representations", "Adjacency matrix/list, edge cases and storage/operation trade-offs.", "high"],
      ["trace", "Complexity of data-structure operations", "Choose the right representation for access, update, search, and traversal.", "high"]
    ],
    questionTypes: [
      { type: "C trace", pattern: "Predict output, pointer values, or array state after a short C fragment.", why: "Precedence, evaluation order, pointer arithmetic, and off-by-one errors stack together.", method: "Make a table for each variable and draw the pointed-to object; do not run it mentally.", difficulty: "High", tags: ["C", "pointers"] },
      { type: "Recursion", pattern: "Find return value, number of calls, or stack depth for a recursive function.", why: "The recurrence and the evaluation tree are not always the same as the output expression.", method: "Expand the first 2–3 calls, mark base cases, then solve the call-count recurrence.", difficulty: "Medium", tags: ["recursion", "stack"] },
      { type: "Tree / heap", pattern: "Infer traversal, BST shape, heap array, or the result after an update sequence.", why: "Insertion order and whether the tree is a BST or merely a binary tree change everything.", method: "Apply the invariant after every operation; write indices for heap parent/children.", difficulty: "High", tags: ["BST", "heap"] },
      { type: "Representation choice", pattern: "Compare time and space for a stack, queue, list, tree, or graph representation.", why: "Asymptotic cost depends on the operation and on the chosen representation.", method: "List required operations, then make a cost table before selecting a structure.", difficulty: "Medium", tags: ["complexity", "graphs"] }
    ]
  },
  {
    id: "algorithms", number: "05", short: "ALG", abbr: "A", name: "Algorithms", color: "#5c8e9c",
    description: "Complexity, design & graph algorithms",
    focus: "State the invariant before the steps.",
    topics: [
      ["asymptotic", "Worst-case time and space complexity", "O, Ω, Θ, little-o intuition, nested loops and dominant terms.", "must"],
      ["search", "Searching techniques", "Linear, binary, boundary variants and precondition checks.", "must"],
      ["sort", "Sorting algorithms", "Insertion, selection, bubble, merge, quick, heap; stability and bounds.", "must"],
      ["hash", "Hashing", "Collision resolution, chaining, open addressing and load factor.", "high"],
      ["divide", "Divide and conquer", "Recurrence setup, merge / partition work and master-style reasoning.", "must"],
      ["greedy", "Greedy design", "Activity selection, interval choices, exchange argument and scheduling.", "must"],
      ["dp", "Dynamic programming", "State, transition, base case, order, reconstruction and space reduction.", "must"],
      ["traversal", "Graph traversals", "BFS/DFS, discovery times, components, cycles and complexity.", "must"],
      ["mst", "Minimum spanning trees", "Kruskal, Prim, cut/cycle properties and uniqueness.", "must"],
      ["shortest", "Shortest paths", "Dijkstra, Bellman–Ford, Floyd–Warshall and negative-edge limits.", "must"]
    ],
    questionTypes: [
      { type: "Complexity", pattern: "Classify a loop, recurrence, or algorithm's worst-case time and auxiliary space.", why: "The outer loop bound and the cost of the inner operation are often dependent.", method: "Count executions with a boundary table; include recursion stack / auxiliary arrays separately.", difficulty: "High", tags: ["Big-O", "recurrences"] },
      { type: "Greedy proof", pattern: "Choose the greedy rule or decide whether a proposed greedy strategy is valid.", why: "A plausible local choice is not a proof of global optimality.", method: "Look for an exchange argument or a counterexample before calculating.", difficulty: "High", tags: ["greedy", "proof"] },
      { type: "DP recurrence", pattern: "Build a state and transition for knapsack-like, sequence, or grid optimisation.", why: "The state must contain enough history; an underspecified state gives a convincing wrong answer.", method: "Write what the state means in one sentence, then test the transition on tiny inputs.", difficulty: "High", tags: ["DP", "state"] },
      { type: "Graph algorithm", pattern: "Run BFS/DFS, MST, or shortest path and report order, weight, or distance.", why: "Tie-breaking, stale priority-queue entries, and negative edges can alter the result.", method: "Write the frontier / set and relaxation invariant after every extraction.", difficulty: "High", tags: ["MST", "shortest path"] }
    ]
  },
  {
    id: "toc", number: "06", short: "TOC", abbr: "T", name: "Theory of Computation", color: "#7f79a7",
    description: "Automata, grammars & decidability",
    focus: "Classify the language before building the machine.",
    topics: [
      ["regex", "Regular expressions and languages", "Operators, precedence, closure properties and language descriptions.", "must"],
      ["dfa", "DFA and NFA construction", "Subset construction, ε-closures, acceptance and equivalent machines.", "must"],
      ["minimize", "DFA minimisation", "Reachability, distinguishability and minimum-state reasoning.", "high"],
      ["regular", "Regular language properties", "Closure, decision questions and product constructions.", "must"],
      ["cfg", "Context-free grammars", "Derivations, parse trees, ambiguity and language generation.", "must"],
      ["pda", "Push-down automata", "Stack behaviour, acceptance mode and CFG ↔ PDA intuition.", "high"],
      ["pumping", "Pumping lemma", "Choose a split-independent witness and use quantifiers correctly.", "must"],
      ["cfl", "Context-free language properties", "Closure / non-closure patterns and grammar-based reasoning.", "high"],
      ["tm", "Turing machines", "Configurations, recognisers, deciders and machine-level simulation.", "high"],
      ["undecidable", "Undecidability", "Reduction direction, halting-style problems and recognisability.", "must"]
    ],
    questionTypes: [
      { type: "Regex ↔ automaton", pattern: "Construct or simplify a regex / NFA / DFA for a described language.", why: "Operator scope, ε-transitions, and missing sink behaviour produce subtle wrong machines.", method: "Start with language examples and counterexamples; test ε, shortest accepted, and near-miss strings.", difficulty: "High", tags: ["DFA", "NFA"] },
      { type: "State minimisation", pattern: "Find equivalent DFA states or the minimum number of states needed.", why: "Unreachable states do not count, and distinguishability is pairwise, not visual.", method: "Remove unreachable states, mark final/non-final pairs, then propagate distinctions.", difficulty: "Medium", tags: ["DFA", "equivalence"] },
      { type: "Pumping lemma", pattern: "Show a language is not regular or not context-free using the pumping lemma.", why: "You choose the string; the adversary chooses the split. Quantifiers decide validity.", method: "Assume membership, pick a parameterised witness, enumerate every legal split, contradict.", difficulty: "High", tags: ["pumping", "proof"] },
      { type: "Reduction / decidability", pattern: "Classify a language or problem as decidable, recognisable, or undecidable.", why: "Reducing in the wrong direction or confusing recogniser with decider reverses the result.", method: "Name the source problem, map instances explicitly, and state what a solver would imply.", difficulty: "High", tags: ["TM", "reduction"] }
    ]
  },
  {
    id: "compiler", number: "07", short: "CD", abbr: "C", name: "Compiler Design", color: "#bd7180",
    description: "Lexing, parsing, IR & optimisation",
    focus: "Track information as it moves through the pipeline.",
    topics: [
      ["lex", "Lexical analysis", "Regular expressions, tokens, longest match, priorities and lexical errors.", "must"],
      ["firstfollow", "FIRST and FOLLOW sets", "ε propagation, lookahead and predictive parsing table entries.", "must"],
      ["parsing", "Top-down and bottom-up parsing", "LL(1), LR intuition, shift/reduce and reduce/reduce conflicts.", "must"],
      ["syntax", "Syntax-directed translation", "Attributes, dependency order, postfix / three-address translation.", "high"],
      ["runtime", "Runtime environments", "Activation records, parameter passing, scope and storage allocation.", "must"],
      ["ir", "Intermediate code generation", "Three-address code, temporaries, basic blocks and control flow.", "must"],
      ["local", "Local optimisation", "Constant folding / propagation, copy propagation and algebraic simplification.", "high"],
      ["cse", "Common subexpression elimination", "Available expressions, value numbering and side-effect safety.", "high"],
      ["live", "Liveness analysis", "Use/def sets, in/out equations and dead-code elimination.", "must"],
      ["flow", "Data-flow analysis workflow", "CFG, direction, meet operator, initialisation and fixed point.", "must"]
    ],
    questionTypes: [
      { type: "Lexer trace", pattern: "Tokenise a string under competing regular-expression rules.", why: "Maximal munch and rule priority can change the token stream before parsing even starts.", method: "At each cursor position list all matching tokens, then apply longest match and priority.", difficulty: "Medium", tags: ["lexing", "regex"] },
      { type: "FIRST / FOLLOW", pattern: "Compute sets and decide whether a grammar is LL(1), or fill a parsing table.", why: "Nullable nonterminals make ε propagation easy to stop too early.", method: "Iterate to a fixed point; record the production that contributed each terminal.", difficulty: "High", tags: ["LL(1)", "grammar"] },
      { type: "Runtime / TAC", pattern: "Draw an activation record or generate three-address code and basic blocks.", why: "Temporaries, parameter order, and control-flow leaders affect later analyses.", method: "Name every temporary; mark leaders at jumps, targets, and post-jump instructions.", difficulty: "Medium", tags: ["IR", "runtime"] },
      { type: "Data flow", pattern: "Compute liveness / constant propagation or identify an optimisation opportunity.", why: "The analysis direction and boundary value determine the equations.", method: "Write GEN/KILL or USE/DEF, then iterate IN/OUT until no set changes.", difficulty: "High", tags: ["liveness", "optimisation"] }
    ]
  },
  {
    id: "os", number: "08", short: "OS", abbr: "O", name: "Operating Systems", color: "#668d74",
    description: "Processes, concurrency, memory & files",
    focus: "Draw the state, queue, or address translation.",
    topics: [
      ["syscalls", "System calls and OS structure", "User/kernel mode, traps, process API and context-switch boundary.", "must"],
      ["process", "Processes, threads and scheduling states", "PCB, lifecycle, context switch, user/kernel threads and concurrency.", "must"],
      ["ipc", "Inter-process communication", "Pipes, shared memory, message passing and synchronization implications.", "high"],
      ["sync", "Concurrency and synchronization", "Race conditions, mutexes, semaphores, monitors and classic problems.", "must"],
      ["deadlock", "Deadlock", "Four conditions, resource graph, prevention, avoidance and Banker-style safety.", "must"],
      ["cpu", "CPU scheduling", "FCFS, SJF/SRTF, priority, round robin, waiting/turnaround/response time.", "must"],
      ["io", "I/O scheduling", "Request queues, seek movement and scheduling trade-offs.", "high"],
      ["paging", "Memory management and paging", "Page tables, TLB, logical/physical address, fragmentation and allocation.", "must"],
      ["virtual", "Virtual memory", "Demand paging, page faults, replacement, thrashing and working set intuition.", "must"],
      ["files", "File systems", "Allocation, directories, inodes, free space and file access paths.", "must"]
    ],
    questionTypes: [
      { type: "Scheduling table", pattern: "Draw a schedule and compute waiting, turnaround, response, or context-switch cost.", why: "Arrival time, preemption, and the exact tie-break rule change the queue.", method: "Build a timeline first; annotate each process's ready-queue entry and completion.", difficulty: "High", tags: ["CPU", "RR/SJF"] },
      { type: "Semaphore trace", pattern: "Determine whether a concurrent program races, deadlocks, or produces a possible output.", why: "One interleaving is not proof; semaphore wait/signal ordering constrains the set.", method: "List shared variables and critical sections, then explore the smallest conflicting interleavings.", difficulty: "High", tags: ["sync", "race"] },
      { type: "Deadlock safety", pattern: "Check a resource state for safe sequence, deadlock, or possible recovery.", why: "Available resources must be updated after each hypothetical completion.", method: "Compute Need = Max − Allocation; repeatedly find a process whose Need fits.", difficulty: "High", tags: ["Banker", "deadlock"] },
      { type: "Paging / replacement", pattern: "Translate an address or count page faults under FIFO, LRU, or an optimal policy.", why: "Page versus offset bits and the initial empty frames are common traps.", method: "Separate page number/offset, then draw frame state after every reference.", difficulty: "High", tags: ["VM", "TLB"] }
    ]
  },
  {
    id: "db", number: "09", short: "DB", abbr: "B", name: "Databases", color: "#4d8e8e",
    description: "SQL, design, indexes & transactions",
    focus: "Make the data model explicit before querying it.",
    topics: [
      ["er", "ER model and mapping", "Entities, relationships, cardinality, participation, weak entities and keys.", "must"],
      ["relational", "Relational model and constraints", "Keys, domains, entity/referential integrity and relational schemas.", "must"],
      ["algebra", "Relational algebra", "Selection, projection, joins, division, grouping and equivalence transformations.", "must"],
      ["sql", "SQL / tuple calculus", "Nested queries, joins, NULL, aggregation, GROUP BY, HAVING and quantifiers.", "must"],
      ["fd", "Functional dependencies", "Closure, candidate keys, minimal cover and implication.", "must"],
      ["normal", "Normal forms", "1NF, 2NF, 3NF, BCNF, lossless join and dependency preservation.", "must"],
      ["files", "File organisation", "Heap / sequential organisation, records, blocks and access paths.", "high"],
      ["btree", "B-tree and B+ tree indexes", "Height, fanout, search, insertion, split and range-query behaviour.", "must"],
      ["txn", "Transactions and serializability", "ACID, conflict/view serializability, precedence graphs and schedules.", "must"],
      ["cc", "Concurrency control", "Locks, 2PL variants, deadlocks, timestamps and recovery intuition.", "high"]
    ],
    questionTypes: [
      { type: "SQL result", pattern: "Predict the rows from joins, NULLs, aggregation, nested queries, or HAVING.", why: "Join multiplicity and three-valued logic make an apparently simple query deceptive.", method: "Build the intermediate relation after each FROM/JOIN, then apply WHERE, grouping, HAVING, SELECT order.", difficulty: "High", tags: ["SQL", "NULL"] },
      { type: "Keys / normal form", pattern: "Find candidate keys, highest normal form, or a valid decomposition from FDs.", why: "A closure proves a key; a single partial or transitive dependency can change the normal form.", method: "Compute attribute closure and mark prime attributes before testing each dependency.", difficulty: "High", tags: ["FD", "BCNF"] },
      { type: "Algebra / ER", pattern: "Translate an ER or English requirement into relational algebra, schema, or constraints.", why: "Cardinality and participation are lost if the model is translated mechanically.", method: "Write the entities and relationship keys first; then compose operations with explicit joins.", difficulty: "Medium", tags: ["ER", "algebra"] },
      { type: "Schedule / index", pattern: "Test serializability or compute B+ tree height / access cost after updates.", why: "Conflicts are directional and B+ tree leaves are linked for ranges.", method: "Draw the precedence graph or update each level and split before counting I/Os.", difficulty: "High", tags: ["transactions", "B+ tree"] }
    ]
  },
  {
    id: "networks", number: "10", short: "CN", abbr: "N", name: "Computer Networks", color: "#4b7caa",
    description: "Switching, routing, TCP, DNS & HTTP",
    focus: "Follow the packet and count every boundary.",
    topics: [
      ["layers", "Layering and encapsulation", "Service interfaces, headers, MTU path and protocol responsibility.", "must"],
      ["switching", "Circuit, packet and virtual-circuit switching", "Setup, store-and-forward, delay components and performance metrics.", "high"],
      ["error", "Error detection and framing", "Parity, checksum, CRC, minimum distance and framing choices.", "must"],
      ["mac", "Medium access control and Ethernet", "Shared medium, CSMA/CD intuition, frames, switching and collision domain.", "must"],
      ["dv", "Distance-vector routing", "Bellman–Ford updates, count-to-infinity and split-horizon intuition.", "must"],
      ["ls", "Link-state routing", "Flooding, shortest-path computation and database consistency.", "must"],
      ["ipv4", "IPv4 addressing and fragmentation", "Header fields, TTL, fragmentation offset, MTU and reassembly.", "must"],
      ["cidr", "CIDR and subnetting", "Prefix ranges, route aggregation, longest-prefix match and address counts.", "must"],
      ["nat", "Network address translation", "Mappings, port translation and end-to-end trade-offs.", "high"],
      ["tcp", "TCP flow and congestion control", "Window, ACKs, retransmission, slow start, congestion avoidance and fast recovery.", "must"],
      ["apps", "Socket API, DNS and HTTP", "Client/server calls, resolution, caching, methods, status and persistent connections.", "must"]
    ],
    questionTypes: [
      { type: "CIDR / fragmentation", pattern: "Find subnet range, longest-prefix route, fragment offsets, or number of fragments.", why: "Host bits, network bits, 8-byte fragment units, and inclusive ranges are easy to mix.", method: "Write the binary boundary and header payload size before doing arithmetic.", difficulty: "High", tags: ["IPv4", "CIDR"] },
      { type: "Routing table", pattern: "Run distance-vector / link-state updates or choose the forwarding interface.", why: "The advertised distance includes the next-link cost, and longest prefix beats metric only after match.", method: "Make a neighbour table each round; separate route computation from forwarding lookup.", difficulty: "High", tags: ["DV", "LS"] },
      { type: "TCP window", pattern: "Compute send window, ACK progression, throughput, or congestion-window changes.", why: "Flow-control and congestion-control limits are different; timeout and duplicate ACK signals differ.", method: "Track sequence, ACK, rwnd, cwnd, and effective window on a timeline.", difficulty: "High", tags: ["TCP", "congestion"] },
      { type: "Protocol timing", pattern: "Calculate end-to-end delay or identify the headers / API calls in a DNS, HTTP, or switching path.", why: "Propagation, transmission, queueing, and processing delays are not interchangeable.", method: "Draw the path and label each serial/parallel component; state what is cached.", difficulty: "Medium", tags: ["DNS", "HTTP"] },
      { type: "CRC / Ethernet", pattern: "Compute a CRC remainder, detect an error, or reason about MAC behaviour.", why: "The generator degree determines appended zeros and XOR alignment.", method: "Write the bit polynomial / frame steps exactly; never drop leading zeros.", difficulty: "Medium", tags: ["CRC", "Ethernet"] }
    ]
  }
];

const practicePrompts = {
  math: [
    { prompt: "How many binary strings of length n contain no consecutive 1s? Give a recurrence and base cases.", answer: "a_n = a_{n−1} + a_{n−2}, with a_0 = 1 and a_1 = 2; therefore a_n = F_{n+2}." },
    { prompt: "A connected graph has exactly two vertices of odd degree. What does this guarantee?", answer: "It has an Euler trail but not an Euler circuit (assuming the graph has at least one edge)." },
    { prompt: "For A = [[2,1],[0,2]], how many linearly independent eigenvectors does A have?", answer: "One. The only eigenvalue is 2, and (A−2I)v=0 forces the second component of v to be zero." },
    { prompt: "Prevalence is 1%, sensitivity 99%, and false-positive rate 5%. Given a positive test, find P(disease | positive).", answer: "0.0099/(0.0099+0.0495) = 1/6 ≈ 16.67%." },
    { prompt: "Find the global maximum and minimum of f(x)=x³−3x on [−2,2].", answer: "Maximum 2 at x=−1 and x=2; minimum −2 at x=−2 and x=1." }
  ],
  logic: [
    { prompt: "Simplify F(A,B,C,D)=Σm(0,2,8,10)+d(1,3,9,11).", answer: "F = B′. Use the don't-care cells to make one group containing every minterm with B=0." },
    { prompt: "A 2:1 MUX has D0=A, D1=¬A, and select S=B. What is its output?", answer: "F = B′A + B¬A = A XOR B." },
    { prompt: "A D flip-flop has D=Q XOR X. Starting Q=0, X=1 for two clock edges and then X=0 for one edge. Find Q after three edges.", answer: "The states are 1, 0, 0; final Q=0." },
    { prompt: "Add 01111111 and 00000001 as 8-bit two's-complement numbers. Give the result and overflow status.", answer: "The bit result is 10000000, and signed overflow occurs: 127+1 cannot be represented." }
  ],
  coa: [
    { prompt: "A 32-bit byte-addressed machine has a 1 KiB direct-mapped cache with 16-byte lines. Find tag, index, and offset bits.", answer: "There are 64 lines: offset=4 bits, index=6 bits, tag=22 bits." },
    { prompt: "A 5-stage pipeline executes 100 independent instructions with no stalls. How many cycles and what is the ideal speedup over a 5-cycle non-pipelined design?", answer: "104 cycles; speedup = 500/104 ≈ 4.81." },
    { prompt: "For LOAD R1, 20(R2) with R2=1000, find the effective address and number of memory reads.", answer: "Effective address=1020; one memory read supplies the operand (instruction fetch is separate)." },
    { prompt: "A 1 MiB transfer uses one interrupt per 4 KiB block. How many interrupts are generated?", answer: "1 MiB / 4 KiB = 256 interrupts." }
  ],
  programming: [
    { prompt: "What is printed? int a[]={1,2,3}; int *p=a; (*p)++; p++; printf(\"%d %d\",a[0],*p);", answer: "2 2. The increment changes a[0], then p points to a[1]." },
    { prompt: "Solve the order of T(n)=T(n−1)+n with T(0)=1.", answer: "T(n)=1+n(n+1)/2, so T(n)=Θ(n²) and the recursion stack is Θ(n)." },
    { prompt: "Insert 5,3,8,1,4 into an initially empty min-heap. What is the array representation?", answer: "[1,3,8,5,4]. Restore the heap property after each insertion." },
    { prompt: "You need O(1) indexed lookup and frequent insertions in the middle. Which basic structure gives which trade-off?", answer: "An array gives O(1) index lookup but O(n) middle insertion; a linked list gives O(n) lookup but O(1) insertion once the node is located." }
  ],
  algorithms: [
    { prompt: "What is the order of: for i=1..n, for j=1; j≤i; j*=2?", answer: "Θ(n log n), because the inner work is Σᵢ log i = Θ(n log n)." },
    { prompt: "For interval scheduling, which local rule is optimal for maximising the number of non-overlapping activities?", answer: "Repeatedly choose the compatible activity with the earliest finish time; the exchange argument proves it is optimal." },
    { prompt: "0/1 knapsack has capacity 5 and items (weight,value)=(2,3),(3,4),(4,5). What is the maximum value?", answer: "7, by taking the first two items; the 4-weight item alone gives only 5." },
    { prompt: "Edges are AB=1, AC=4, BC=2. What shortest distances from A does Dijkstra compute?", answer: "d(A)=0, d(B)=1, d(C)=3 via B." }
  ],
  toc: [
    { prompt: "Give a regular expression over {0,1} for all strings ending in 01.", answer: "(0|1)*01." },
    { prompt: "A reachable DFA has 8 states; partition refinement ends with 5 equivalence classes. How many states does the minimal DFA have?", answer: "5 states." },
    { prompt: "Is L={0ⁿ1ⁿ | n≥0} regular? State the proof idea.", answer: "No. Pumping a sufficiently long 0ⁿ1ⁿ string changes the number of 0s without changing the 1s, so the pumped string leaves L." },
    { prompt: "If HALT ≤m L and L is decidable, what can you conclude?", answer: "HALT would be decidable, a contradiction; therefore L is undecidable." }
  ],
  compiler: [
    { prompt: "With rules for '=' and '==', how is a==b tokenised under longest match?", answer: "identifier(a), equality operator(==), identifier(b); the two-character rule wins at the second character." },
    { prompt: "For S→AB, A→aA|ε, B→b|ε, find FIRST(S), FOLLOW(A), and FOLLOW(B), with $ as end marker.", answer: "FIRST(S)={a,b,ε}; FOLLOW(A)={b,$}; FOLLOW(B)={$}." },
    { prompt: "Generate three-address code for x = a + b*c.", answer: "t1=b*c; t2=a+t1; x=t2." },
    { prompt: "After x=1; y=x+2; print(y), what constants can a local constant-propagation pass know?", answer: "At print, x=1 and y=3; the addition can be folded to print(3) if the language permits the rewrite." }
  ],
  os: [
    { prompt: "Under preemptive SRTF, P1 arrives at 0 with burst 5; P2 arrives at 1 with burst 2. Give the schedule and waiting times.", answer: "P1 runs 0–1, P2 1–3, P1 3–7; waiting times are P1=2 and P2=0." },
    { prompt: "Two threads each read x=0, add 1 locally, then write back without a lock. What final values are possible?", answer: "1 or 2. Interleaved reads can lose one update; serial execution gives 2." },
    { prompt: "P1 holds (1,0) and may need (2,1); P2 holds (0,1) and may need (1,1); available is (0,0). Is the state safe?", answer: "No. Neither remaining need fits available, so no process can complete; the state is unsafe and, without another release, deadlocked." },
    { prompt: "With 2 FIFO page frames, count faults for the reference string 1,2,1,3,1.", answer: "4 faults: references 1, 2, 3, and the final 1 fault; the middle 1 is a hit." }
  ],
  db: [
    { prompt: "For T(id,score)={(1,10),(2,NULL),(3,20)}, what do COUNT(*) and COUNT(score) return?", answer: "COUNT(*)=3; COUNT(score)=2 because COUNT(column) ignores NULL." },
    { prompt: "R(A,B,C) has FDs A→B and B→C. What is a candidate key and the highest normal form?", answer: "A is a candidate key; the relation is in 2NF but not 3NF because B→C has a non-superkey determinant and C is non-prime." },
    { prompt: "A 1:N Department–Employee relationship requires every employee to belong to one department. Where does the foreign key go?", answer: "Put Department's key as a NOT NULL foreign key in Employee; the N-side carries the key." },
    { prompt: "A schedule has r1(X), w1(X), r2(X), w2(X). Is its precedence graph serializable?", answer: "Yes: all conflicts point T1→T2, so it is conflict-serializable in the order T1 then T2." }
  ],
  networks: [
    { prompt: "For 192.168.10.0/26, give the address range and number of usable host addresses.", answer: "Range 192.168.10.0–192.168.10.63; usable hosts .1–.62, so 62." },
    { prompt: "Edges are A–B=1, B–C=2, A–C=4. From A, what next hop and cost does shortest-path routing choose for C?", answer: "Next hop B, total cost 3." },
    { prompt: "If TCP has rwnd=4000 bytes and cwnd=6000 bytes, what is the maximum currently usable send window?", answer: "min(rwnd,cwnd)=4000 bytes." },
    { prompt: "For data 1101 and generator 1011, what CRC remainder is appended?", answer: "Append three zeros and divide; the remainder is 001." },
    { prompt: "On a new TCP connection, what exchange must complete before a normal HTTP request can be sent?", answer: "The three-way handshake (SYN, SYN-ACK, ACK); then the client sends the HTTP request." }
  ]
};

const phases = [
  { number: "PHASE 01", title: "Map the syllabus", text: "One fast, honest pass across all ten sections. Build short notes only after understanding.", time: "Coverage / 8–10 weeks" },
  { number: "PHASE 02", title: "Turn topics into patterns", text: "Do topic-wise official PYQs and the question bank here. Tag every miss in an error log.", time: "Retrieval / 6–8 weeks" },
  { number: "PHASE 03", title: "Mix and time", text: "Alternate full subjects with mixed sets. Train the switch from proof to numerical to code.", time: "Application / 4–6 weeks" },
  { number: "PHASE 04", title: "Simulate + refine", text: "Use full mocks, rigorous analysis, spaced repair, and deliberate skip decisions.", time: "Exam mode / final cycle" }
];

const focusItems = [
  ["01", "Finish one foundation topic", "Use the checklist; explain it aloud in 60 seconds."],
  ["02", "Solve 10–15 official PYQs", "Untimed first, then redo the misses with a clock."],
  ["03", "Update the error log", "C / S / A / T: concept, setup, arithmetic, time."],
  ["04", "Re-test after 72 hours", "A topic is stable when it survives a new-looking question."]
];

const dontMiss = [
  ["PYQs", "Every official PYQ", "Use recent papers for pattern and older papers for breadth."],
  ["LOG", "A real error notebook", "Record the trigger, wrong path, fix, and retest date."],
  ["MIX", "Timed mixed sets", "Rank needs switching skill, not only chapter comfort."],
  ["REVISE", "Spaced retrieval", "Revisit formulas, traps, and misses at 1 / 3 / 7 / 14 days."]
];

const STORAGE_KEY = "rankroom-gate-cs-2027-v1";
const state = loadState();
let toastTimer;

function loadState() {
  try {
    const saved = JSON.parse(localStorage.getItem(STORAGE_KEY) || "{}");
    return {
      checks: saved.checks || {},
      mastered: saved.mastered || {},
      revealed: saved.revealed || {},
      activeView: saved.activeView || "overview",
      topicFilter: saved.topicFilter || "all",
      topicQuery: saved.topicQuery || "",
      questionQuery: saved.questionQuery || ""
    };
  } catch (error) {
    return { checks: {}, mastered: {}, revealed: {}, activeView: "overview", topicFilter: "all", topicQuery: "", questionQuery: "" };
  }
}

function saveState() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
}

function allTopics() {
  return subjects.flatMap(subject => subject.topics.map(topic => ({ subject, topic })));
}

function allQuestions() {
  return subjects.flatMap(subject => subject.questionTypes.map((question, index) => ({ subject, question, id: `${subject.id}-q${index}` })));
}

function checkedCount() {
  return allTopics().filter(({ subject, topic }) => state.checks[`${subject.id}:${topic[0]}`]).length;
}

function masteredCount() {
  return allQuestions().filter(item => state.mastered[item.id]).length;
}

function percent(done, total) {
  return total ? Math.round((done / total) * 100) : 0;
}

function esc(value) {
  return String(value).replace(/[&<>'"]/g, char => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" }[char]));
}

function renderStats() {
  const done = checkedCount();
  const qDone = masteredCount();
  const stats = [
    [allTopics().length, "syllabus checkpoints", "◌"],
    [subjects.length, "core sections", "◈"],
    [allQuestions().length, "question archetypes", "?"],
    [`${percent(qDone, allQuestions().length)}%`, "recall bank mastered", "↗"]
  ];
  document.getElementById("statGrid").innerHTML = stats.map(([value, label, icon]) => `<div class="stat-card"><div class="stat-top"><strong>${value}</strong><span class="stat-icon">${icon}</span></div><p>${label}</p></div>`).join("");
}

function renderOverview() {
  const done = checkedCount();
  const total = allTopics().length;
  const pct = percent(done, total);
  const ring = document.getElementById("progressRing");
  ring.style.background = `conic-gradient(var(--forest-2) ${pct * 3.6}deg, var(--paper-deep) 0deg)`;
  ring.setAttribute("aria-label", `${pct} percent syllabus complete`);
  document.getElementById("progressPercent").textContent = `${pct}%`;
  document.getElementById("progressBar").style.width = `${pct}%`;
  document.getElementById("checkedCount").textContent = `${done} of ${total} topics`;
  document.getElementById("checklistPercent").textContent = `${pct}%`;

  const message = pct === 0 ? "Every checked topic is one less open loop." : pct < 35 ? "Build breadth before polishing favourite topics." : pct < 75 ? "Coverage is moving. Keep the repair loop visible." : pct < 100 ? "Close the remaining gaps, then mix the set." : "First pass complete. Now make it fast and durable.";
  document.getElementById("progressMessage").textContent = message;
  document.getElementById("coverageLabel").textContent = pct === 0 ? "Starting line" : pct === 100 ? "Full coverage" : `${pct}% in motion`;
  const firstOpen = subjects.find(subject => subject.topics.some(topic => !state.checks[`${subject.id}:${topic[0]}`]));
  document.getElementById("nextSubject").textContent = firstOpen ? `Next: ${firstOpen.short}` : "Next: mixed revision";

  document.getElementById("focusList").innerHTML = focusItems.map(([number, title, body]) => `<div class="focus-item"><span class="focus-index">${number}</span><div><strong>${title}</strong><span>${body}</span></div></div>`).join("");
  document.getElementById("dontMissList").innerHTML = dontMiss.map(([key, title, body]) => `<div class="non-negotiable"><span>${key.slice(0, 1)}</span><div><strong>${title}</strong><p>${body}</p></div></div>`).join("");

  document.getElementById("subjectStrip").innerHTML = subjects.map(subject => {
    const subjectDone = subject.topics.filter(topic => state.checks[`${subject.id}:${topic[0]}`]).length;
    const subjectPct = percent(subjectDone, subject.topics.length);
    return `<div class="subject-strip-item ${subjectPct === 100 ? "complete" : ""}" title="${esc(subject.name)}: ${subjectPct}%"><span style="width:${subjectPct}%"></span><b>${subject.abbr}</b></div>`;
  }).join("");

  document.getElementById("subjectOverviewGrid").innerHTML = subjects.map(subject => {
    const subjectDone = subject.topics.filter(topic => state.checks[`${subject.id}:${topic[0]}`]).length;
    const subjectPct = percent(subjectDone, subject.topics.length);
    return `<article class="subject-card" style="--subject-color:${subject.color}">
      <div class="subject-number"><span>${subject.number}</span><b>${subjectPct}%</b></div>
      <h3>${esc(subject.name)}</h3>
      <p>${esc(subject.description)}</p>
      <div class="subject-card-footer"><div class="card-bar"><span style="width:${subjectPct}%"></span></div><span class="card-percent">${subjectDone}/${subject.topics.length}</span></div>
    </article>`;
  }).join("");
}

function renderChecklist() {
  const query = state.topicQuery.trim().toLowerCase();
  const filtered = subjects.map(subject => {
    const topics = subject.topics.filter(topic => {
      const matchesFilter = state.topicFilter === "all" || topic[3] === state.topicFilter;
      const matchesQuery = !query || `${subject.name} ${topic.join(" ")}`.toLowerCase().includes(query);
      return matchesFilter && matchesQuery;
    });
    return { subject, topics };
  }).filter(item => item.topics.length);

  const visibleTopics = filtered.reduce((sum, item) => sum + item.topics.length, 0);
  document.getElementById("checklistSummary").innerHTML = `<strong>Showing ${visibleTopics} checkpoint${visibleTopics === 1 ? "" : "s"}</strong><span>${state.topicFilter === "all" ? "Full map" : `${state.topicFilter === "must" ? "Must know" : state.topicFilter === "high" ? "High yield" : "Build next"} only`}</span>`;
  document.getElementById("checklistEmpty").hidden = filtered.length > 0;
  document.getElementById("checklistGrid").innerHTML = filtered.map(({ subject, topics }) => {
    const subjectDone = subject.topics.filter(topic => state.checks[`${subject.id}:${topic[0]}`]).length;
    return `<article class="checklist-card" style="--subject-color:${subject.color}">
      <div class="checklist-card-header"><div class="checklist-card-title"><span class="subject-dot">${subject.abbr}</span><h2>${esc(subject.name)}</h2></div><small>${subjectDone}/${subject.topics.length} done</small></div>
      <div class="topic-list">${topics.map(topic => {
        const key = `${subject.id}:${topic[0]}`;
        const isDone = !!state.checks[key];
        return `<div class="topic-row ${isDone ? "done" : ""}">
          <div class="topic-check"><input type="checkbox" id="topic-${key}" data-topic-key="${key}" ${isDone ? "checked" : ""} /><label for="topic-${key}" aria-label="Mark ${esc(topic[1])} complete">✓</label></div>
          <div class="topic-content"><strong>${esc(topic[1])}</strong><p>${esc(topic[2])}</p></div>
          <span class="priority ${topic[3]}">${topic[3] === "must" ? "MUST" : topic[3] === "high" ? "HIGH" : "BUILD"}</span>
        </div>`;
      }).join("")}</div>
    </article>`;
  }).join("");

  document.getElementById("topicSearch").value = state.topicQuery;
  document.querySelectorAll("[data-topic-filter]").forEach(button => button.classList.toggle("active", button.dataset.topicFilter === state.topicFilter));
}

function renderQuestions() {
  const query = state.questionQuery.trim().toLowerCase();
  const groups = subjects.map(subject => {
    const questions = subject.questionTypes.map((question, index) => ({ subject, question, index, id: `${subject.id}-q${index}` })).filter(({ subject: itemSubject, question }) => {
      const haystack = `${itemSubject.name} ${question.type} ${question.pattern} ${question.why} ${question.method} ${question.tags.join(" ")}`.toLowerCase();
      return !query || haystack.includes(query);
    });
    return { subject, questions };
  }).filter(group => group.questions.length);

  document.getElementById("questionEmpty").hidden = groups.length > 0;
  document.getElementById("questionSubjects").innerHTML = groups.map(({ subject, questions }) => `<section class="question-section">
    <div class="question-section-header"><div class="question-section-title"><span class="subject-dot" style="--subject-color:${subject.color}">${subject.abbr}</span><div><h2>${esc(subject.name)}</h2><p>${esc(subject.focus)}</p></div></div><span class="question-section-meta">${questions.length} pattern${questions.length === 1 ? "" : "s"} / ${subject.short}</span></div>
    <div class="question-grid">${questions.map(({ question, id, index }) => {
      const mastered = !!state.mastered[id];
      const revealed = !!state.revealed?.[id];
      const sample = practicePrompts[subject.id]?.[index] || { prompt: "Write a fresh question for this pattern from your current PYQ set.", answer: "Use the official solution only after a cold attempt, then record the trap in your error log." };
      return `<article class="question-card ${mastered ? "mastered" : ""} ${revealed ? "revealed" : ""}" data-question-id="${id}">
        <div class="question-card-top"><span class="question-type">${esc(question.type)}</span><span class="difficulty">${esc(question.difficulty)}</span></div>
        <div class="question-card-body"><h3>${esc(question.pattern)}</h3>
          <div class="practice-prompt"><span>TRY IT</span><p>${esc(sample.prompt)}</p></div>
          <div class="answer-wrap"><button class="reveal-button" data-reveal-id="${id}">${revealed ? "Hide answer + lens ↑" : "Reveal answer + lens ↓"}</button><div class="answer"><strong>Answer:</strong> ${esc(sample.answer)}<br /><strong>Why it appears:</strong> ${esc(question.why)}<br /><strong>Attempt it like this:</strong> ${esc(question.method)}</div></div>
          <div class="question-card-bottom"><div class="question-tags">${question.tags.map(tag => `<span class="question-tag">${esc(tag)}</span>`).join("")}</div><button class="master-button" data-master-id="${id}">${mastered ? "✓ Mastered" : "Mark mastered"}</button></div>
        </div>
      </article>`;
    }).join("")}</div>
  </section>`).join("");

  const total = allQuestions().length;
  const done = masteredCount();
  document.getElementById("questionMastery").textContent = `${percent(done, total)}%`;
  document.getElementById("questionSearch").value = state.questionQuery;
}

function renderPlaybook() {
  document.getElementById("phaseGrid").innerHTML = phases.map((phase, index) => `<article class="phase-card" data-phase="${String(index + 1).padStart(2, "0")}"><span class="phase-number">${phase.number}</span><h2>${phase.title}</h2><p>${phase.text}</p><span class="phase-time">${phase.time}</span></article>`).join("");
}

function renderAll() {
  renderStats();
  renderOverview();
  renderChecklist();
  renderQuestions();
  renderPlaybook();
  setView(state.activeView, false);
}

function setView(view, persist = true) {
  const validView = ["overview", "checklist", "questions", "playbook"].includes(view) ? view : "overview";
  state.activeView = validView;
  document.querySelectorAll(".view").forEach(section => {
    const active = section.id === `view-${validView}`;
    section.classList.toggle("active", active);
    section.hidden = !active;
  });
  document.querySelectorAll("[data-view-target]").forEach(button => button.classList.toggle("active", button.dataset.viewTarget === validView));
  if (persist) saveState();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

function showToast(message) {
  const toast = document.getElementById("toast");
  toast.textContent = message;
  toast.classList.add("show");
  clearTimeout(toastTimer);
  toastTimer = setTimeout(() => toast.classList.remove("show"), 2300);
}

document.addEventListener("click", event => {
  const viewTrigger = event.target.closest("[data-view-target]");
  if (viewTrigger) {
    setView(viewTrigger.dataset.viewTarget);
    document.getElementById("mobileMenu").setAttribute("aria-expanded", "false");
    document.getElementById("mobileNav").hidden = true;
    return;
  }

  const filter = event.target.closest("[data-topic-filter]");
  if (filter) {
    state.topicFilter = filter.dataset.topicFilter;
    saveState();
    renderChecklist();
    return;
  }

  const reveal = event.target.closest("[data-reveal-id]");
  if (reveal) {
    state.revealed = state.revealed || {};
    const id = reveal.dataset.revealId;
    state.revealed[id] = !state.revealed[id];
    saveState();
    renderQuestions();
    return;
  }

  const master = event.target.closest("[data-master-id]");
  if (master) {
    const id = master.dataset.masterId;
    state.mastered[id] = !state.mastered[id];
    saveState();
    renderStats();
    renderQuestions();
    showToast(state.mastered[id] ? "Pattern added to mastered." : "Pattern moved back to practice.");
  }
});

document.addEventListener("change", event => {
  const checkbox = event.target.closest("[data-topic-key]");
  if (!checkbox) return;
  state.checks[checkbox.dataset.topicKey] = checkbox.checked;
  saveState();
  renderStats();
  renderOverview();
  renderChecklist();
  showToast(checkbox.checked ? "Checkpoint saved." : "Checkpoint reopened.");
});

document.getElementById("topicSearch").addEventListener("input", event => {
  state.topicQuery = event.target.value;
  renderChecklist();
});
document.getElementById("questionSearch").addEventListener("input", event => {
  state.questionQuery = event.target.value;
  renderQuestions();
});

document.getElementById("resetProgress").addEventListener("click", () => {
  if (!confirm("Reset all checklist and question-bank progress on this device?")) return;
  state.checks = {};
  state.mastered = {};
  state.revealed = {};
  saveState();
  renderAll();
  showToast("Progress reset. Fresh page, same plan.");
});

document.getElementById("mobileMenu").addEventListener("click", event => {
  const expanded = event.currentTarget.getAttribute("aria-expanded") === "true";
  event.currentTarget.setAttribute("aria-expanded", String(!expanded));
  document.getElementById("mobileNav").hidden = expanded;
});

document.addEventListener("keydown", event => {
  if (event.target.matches("input")) return;
  const key = event.key.toLowerCase();
  if (["1", "2", "3", "4"].includes(key)) setView(["overview", "checklist", "questions", "playbook"][Number(key) - 1]);
  if (key === "r" && state.activeView === "questions") {
    const first = document.querySelector(".question-card:not(.revealed)");
    if (first) first.querySelector("[data-reveal-id]").click();
  }
  if (key === "m" && state.activeView === "questions") {
    const first = document.querySelector(".question-card:not(.mastered)");
    if (first) first.querySelector("[data-master-id]").click();
  }
});

renderAll();
