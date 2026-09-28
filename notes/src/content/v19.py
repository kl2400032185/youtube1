from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=19,
    slug="majority-element-2",
    title="Majority Element II — appears more than n/3 times",
    meta="Striver A2Z · Arrays Playlist #19 · 26:58 · youtube.com/watch?v=vwZj1K0e9U8",
    tag="ARRAYS · PART 19",
    topic="extended Moore voting with two candidates",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Return **all** elements appearing more than `n/3` times. At most **two** can exist "
        "(three would need > n seats). `{1,1,1,3,3,2,2,2}` -> `{1,2}`.")

    P.h2("1 · Brute / Better", color=RED)
    P.bullets([
        "Brute: nested counting `O(n^2)`. Better: hashmap frequencies `O(n)` time, O(n) space — "
        "perfectly fine, but the voting trick is the star.",
    ])

    P.h2("2 · Optimal — Moore voting with TWO thrones", color=GREEN)
    P.p("Now cancellations happen in TRIPLES of three distinct values. Two candidates with counters; "
        "a value that matches neither spends one count from BOTH, and when a count hits 0 the throne "
        "is up for grabs.")
    P.numbered([
        "`arr[i] == el1` -> c1++ ; `== el2` -> c2++.",
        "`c1 == 0` -> adopt as el1 (c1=1); else `c2 == 0` -> adopt as el2 (c2=1).",
        "Otherwise -> `c1--; c2--` (a three-way duel).",
        "**Mandatory** verification pass: the survivors are only candidates, n/3 is not guaranteed.",
    ])
    P.code("cpp", """
int el1 = 0, el2 = 0, c1 = 0, c2 = 0;
for (int x : arr) {
    if (x == el1)      c1++;
    else if (x == el2) c2++;
    else if (c1 == 0)  { el1 = x; c1 = 1; }
    else if (c2 == 0)  { el2 = x; c2 = 1; }
    else               { c1--; c2--; }
}
c1 = c2 = 0;                                  // verification
for (int x : arr) { if (x == el1) c1++; else if (x == el2) c2++; }
vector<int> ans;
if (c1 > n / 3) ans.push_back(el1);
if (c2 > n / 3) ans.push_back(el2);
""", caption="O(n) · O(1) space · verification is NOT optional here")
    P.callout("gotcha", "check el2 BEFORE adopting into el1",
              "Order of the if-chain matters: `x == el2` must be tested before `c1 == 0`, otherwise a value "
              "equal to el2 could be adopted as a NEW el1 — double counting and wrong survivors.")
    P.callout("gotcha", "el1 == el2 pollution",
              "When the first throne frees up, the incoming value might equal el2 — the if-chain order "
              "prevents that because the el2 branch fires first. Write it exactly as above.")
    P.dryrun("Partial run on {1,1,1,3,3,2,2,2}",
             ["x", "el1/c1", "el2/c2", "event"],
             [["1", "1/1", "-/0", "adopt el1"],
              ["1", "1/2", "-/0", "support"],
              ["1", "1/3", "-/0", "support"],
              ["3", "1/3", "3/1", "adopt el2"],
              ["3", "1/3", "3/2", "support"],
              ["2", "1/2", "3/1", "three-way duel"],
              ["2", "1/1", "3/0", "duel"],
              ["2", "1/1", "2/1", "el2 throne refilled by 2"]],
             "Verify: count(1)=3 > 8/3, count(2)=3 > 8/3 -> answer {1,2}.")
    P.chips(["brute O(n^2)", "hash O(n)/O(n)", "2-throne voting O(n)/O(1)"])
    P.divider()
    P.h2("The voting family", color=PURPLE)
    P.table(["Threshold", "Max winners", "Thrones", "Verification"],
            [["> n/2", "1", "1", "needed unless guaranteed"],
             ["> n/3", "2", "2", "ALWAYS needed"],
             ["> n/k", "k-1", "k-1", "ALWAYS needed"]],
            fracs=[0.24, 0.22, 0.24, 0.3])
    P.quote("n/2 fights in pairs, n/3 in triples. The duel generalises — the throne count is k-1.")
