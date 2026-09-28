from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=7,
    slug="majority-element-moores-voting",
    title="Majority Element I — appears more than n/2 (Moore's Voting)",
    meta="Striver A2Z · Arrays Playlist #7 · 18:13 · youtube.com/watch?v=nP_ns3uSh80",
    tag="ARRAYS · PART 7",
    topic="majority element > n/2 with Moore's voting",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Find the element that appears **more than n/2 times** (majority element). "
        "`{2,2,1,1,1,2,2}` n=7 -> `2` (appears 4 > 3.5). At most one such element can exist.")

    P.h2("1 · Brute — count with nested loops", color=RED)
    P.bullets(["For each element count its occurrences; return if count > n/2. `O(n^2)`."])

    P.h2("2 · Better — frequency hashmap", color=ORANGE)
    P.bullets(["One pass counting; check `count > n/2`. `O(n)` time, **O(n)** space."])

    P.h2("3 · Optimal — Moore's Voting Algorithm", color=GREEN)
    P.p("Imagine a fight: the majority element's copies cancel every OTHER element one-for-one, "
        "and still have soldiers left. So pair up different elements and delete both — the survivor "
        "is the *candidate*.")
    P.numbered([
        "Keep `el` (candidate) and `count`.",
        "If `count == 0` -> adopt `arr[i]` as the new candidate (`el = arr[i]`, `count = 1`).",
        "Else if `arr[i] == el` -> `count++`, else -> `count--` (a duel, both die).",
        "Optional 2nd pass: verify `el` really appears > n/2 times (needed when a majority is not guaranteed).",
    ])
    P.code("cpp", """
int el = 0, count = 0;
for (int i = 0; i < n; i++) {
    if (count == 0)          { el = arr[i]; count = 1; }
    else if (arr[i] == el)   count++;
    else                     count--;
}
// verification pass (do it in interviews!)
int c = 0;
for (int x : arr) if (x == el) c++;
return (c > n / 2) ? el : -1;
""", caption="O(n) time · O(1) space")
    P.dryrun("Dry run on {2,2,1,1,1,2,2}",
             ["i", "arr[i]", "el", "count", "what happened"],
             [["0", "2", "2", "1", "adopted"],
              ["1", "2", "2", "2", "supporter"],
              ["2", "1", "2", "1", "duel"],
              ["3", "1", "2", "0", "duel -> trono vacante"],
              ["4", "1", "1", "1", "re-adopted"],
              ["5", "2", "1", "0", "duel"],
              ["6", "2", "2", "1", "adopted -> verify count(2)=4 > 3.5"]],
             "Survivor 2, confirmed by the verification pass.")
    P.arr([2, 2, 1, 1, 1, 2, 2], marks={0: GREEN, 1: GREEN, 5: GREEN, 6: GREEN},
          label="the four 2s out-fight everyone")
    P.callout("trick", "why cancelling is legal",
              "If a value truly owns > n/2 seats, removing one of ITS copies together with one copy of "
              "anything else still leaves it > n/2 of what remains. Majority survives any pairwise deletion.")
    P.callout("gotcha", "when to skip verification",
              "Only when the statement GUARANTEES a majority ('it is guaranteed that...' on LeetCode 169). "
              "Otherwise always run the second counting pass.")
    P.chips(["brute O(n^2)", "hash O(n)/O(n)", "Moore O(n)/O(1)"])
    P.divider()
    P.h2("Cheat sheet — video 7", color=PURPLE)
    P.table(["Approach", "Idea", "TC / SC"],
            [["Nested counting", "count each candidate", "O(n^2)/O(1)"],
             ["Hashmap", "frequencies", "O(n)/O(n)"],
             ["Moore's voting", "cancel different pairs, verify", "O(n)/O(1)"]],
            fracs=[0.3, 0.42, 0.28])
    P.quote("The majority element wins every election it fights — even unfair ones where pairs cancel.")
