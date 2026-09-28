from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=13,
    slug="longest-consecutive-sequence",
    title="Longest Consecutive Sequence (Google favourite)",
    meta="Striver A2Z · Arrays Playlist #13 · 23:11 · youtube.com/watch?v=oO5uLE7EUlM",
    tag="ARRAYS · PART 13",
    topic="longest run of x, x+1, x+2... in O(n)",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Longest run of **consecutive integers** (order in the array does not matter). "
        "`{100,4,200,1,3,2}` -> `4` (the run 1,2,3,4).")

    P.h2("1 · Brute — extend every element linearly", color=RED)
    P.bullets([
        "For each `x`, count `x+1, x+2, ...` with a linear search each time -> `O(n^2)`.",
        "This is the same idea as the optimal one, but with the WRONG lookup structure.",
    ])

    P.h2("2 · Better — sort then scan runs", color=ORANGE)
    P.code("cpp", """
sort(arr.begin(), arr.end());
int len = 1, cur = 1;
for (int i = 1; i < n; i++) {
    if (arr[i] == arr[i - 1] + 1)      cur++;
    else if (arr[i] != arr[i - 1])     cur = 1;     // duplicate: ignore
    len = max(len, cur);
}
""", caption="O(n log n) · remember to SKIP duplicates, not reset on them")

    P.h2("3 · Optimal — hash SET + only start a run at its BEGINNING", color=GREEN)
    P.p("Key trick: only **start counting from `x` when `x-1` is NOT in the set**. That makes each "
        "element visited at most twice overall -> true `O(n)`.")
    P.code("cpp", """
unordered_set<int> s(arr.begin(), arr.end());
int best = 0;
for (int x : s) {
    if (s.count(x - 1)) continue;      // x is NOT a run start -> skip
    int len = 1;
    while (s.count(x + len)) len++;    // walk the run to the right
    best = max(best, len);
}
return best;
""", caption="O(n) expected (unordered_set) · O(n) space")
    P.dryrun("Dry run on {100,4,200,1,3,2}",
             ["x", "x-1 in set?", "action", "run length"],
             [["100", "no", "walk: 101? no", "1"],
              ["4", "YES (3)", "skip — mid-run element", "-"],
              ["200", "no", "walk: 201? no", "1"],
              ["1", "no", "walk 2,3,4,5...", "4"],
              ["3", "YES", "skip", "-"],
              ["2", "YES", "skip", "-"]],
             "Only the run's first brick does any walking — that is why it is O(n).")
    P.arr([100, 4, 200, 1, 3, 2], marks={3: GREEN}, captions={3: "run start"},
          label="set view — only 1 starts a walk")
    P.callout("gotcha", "unordered_set worst case",
              "Hash collisions can degrade to O(n^2) worst case; say 'O(n) expected'. Using `std::set` "
              "makes it O(n log n). Know what your container costs.")
    P.chips(["brute O(n^2)", "sort O(n log n)", "hashset O(n) expected"])
    P.divider()
    P.h2("Cheat sheet — video 13", color=PURPLE)
    P.table(["Approach", "Idea", "TC / SC"],
            [["Linear extend", "search x+1, x+2.. each time", "O(n^2)/O(1)"],
             ["Sort + scan", "count runs, skip dups", "O(n log n)/O(1)"],
             ["HashSet + run starts", "walk only from x with no x-1", "O(n)/O(n)"]],
            fracs=[0.28, 0.4, 0.32])
