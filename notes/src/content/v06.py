from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=6,
    slug="sort-012-dutch-national-flag",
    title="Sort an Array of 0s, 1s and 2s (Dutch National Flag)",
    meta="Striver A2Z · Arrays Playlist #6 · 25:07 · youtube.com/watch?v=tp8JIuCXBaU",
    tag="ARRAYS · PART 6",
    topic="sorting 0/1/2 with three pointers",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Given an array containing only 0s, 1s, 2s — sort it **in place, in one pass**. "
        "`{2,0,2,1,1,0}` -> `{0,0,1,1,2,2}`.")

    P.h2("1 · Brute — just call sort()", color=RED)
    P.bullets(["Comparison sort = `O(n log n)`. You threw away the 'only three values' information."])

    P.h2("2 · Better — count and rewrite", color=ORANGE)
    P.bullets([
        "Count `c0, c1, c2` in one pass; overwrite the array with c0 zeros, c1 ones, c2 twos.",
        "`O(2n)` time, O(1) space. Good, but it is **two** traversals — the flag algorithm does one.",
    ])

    P.h2("3 · Optimal — Dutch National Flag (3 pointers)", color=GREEN)
    P.p("Three regions are maintained at all times. `low` ends the 0s, `mid` scans, `high` starts the 2s.")
    P.bullets([
        "`arr[0 .. low-1]` = 0s  ·  `arr[low .. mid-1]` = 1s  ·  `arr[high+1 .. n-1]` = 2s",
        "Look at `arr[mid]`:",
    ])
    P.numbered([
        "`0` -> swap(arr[low], arr[mid]); low++; mid++   (the thing at low was a 1, safe to take)",
        "`1` -> mid++                                    (already in the right region)",
        "`2` -> swap(arr[mid], arr[high]); high--        (do NOT mid++: the value arriving from high is unexamined!)",
    ])
    P.code("cpp", """
int low = 0, mid = 0, high = n - 1;
while (mid <= high) {
    if (arr[mid] == 0)      { swap(arr[low], arr[mid]); low++; mid++; }
    else if (arr[mid] == 1) { mid++; }
    else                    { swap(arr[mid], arr[high]); high--; }   // no mid++
}
""", caption="one traversal · O(n) · O(1) space")
    P.dryrun("Dry run on {2,0,2,1,1,0}",
             ["mid", "arr", "low,high", "action"],
             [["0", "{2,0,2,1,1,0}", "0,5", "2 -> swap with high, high=4"],
              ["0", "{0,0,2,1,1,2}", "0,4", "0 -> swap low/mid, low=1 mid=1"],
              ["1", "{0,0,2,1,1,2}", "1,4", "0 -> swap, low=2 mid=2"],
              ["2", "{0,0,2,1,1,2}", "2,4", "2 -> swap with high, high=3"],
              ["2", "{0,0,1,1,2,2}", "2,3", "1 -> mid=3"],
              ["3", "{0,0,1,1,2,2}", "2,3", "1 -> mid=4 > high, stop"]],
             "Final: {0,0,1,1,2,2}. Watch row 1: after bringing a value FROM high, mid stayed put.")
    P.arr([2, 0, 2, 1, 1, 0], captions={0: "low", 0: "low"}, label="initial")
    P.arr([0, 0, 1, 1, 2, 2], marks={0: GREEN, 1: GREEN, 4: RED, 5: RED},
          captions={1: "0s done", 3: "1s done"}, label="after")
    P.callout("gotcha", "the ONE line everyone flubs",
              "Case `arr[mid] == 2`: **do not advance mid**. The element swapped in from `high` has never "
              "been examined — skipping it can leave a 0 stranded in the middle.")
    P.callout("interview", "why not count-and-rewrite?",
              "It is acceptable; but DNF is the expected answer and it generalises: same skeleton sorts any "
              "3-way partition (e.g. negative/zero/positive). Name-drop 'Dutch National Flag / Dijkstra'.")
    P.chips(["brute O(n log n)", "count O(2n)", "DNF O(n) one pass"])
    P.divider()
    P.h2("Cheat sheet — video 6", color=PURPLE)
    P.table(["Approach", "Traversals", "TC / SC", "In place"],
            [["sort()", "-", "O(n log n)/O(1..n)", "yes"],
             ["count + overwrite", "2", "O(2n)/O(1)", "yes"],
             ["Dutch national flag", "1", "O(n)/O(1)", "yes"]],
            fracs=[0.3, 0.22, 0.28, 0.2])
