from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=24,
    slug="merge-sorted-arrays-no-extra-space",
    title="Merge Two Sorted Arrays WITHOUT Extra Space",
    meta="Striver A2Z · Arrays Playlist #24 · 32:47 · youtube.com/watch?v=n7uwj04E0I4",
    tag="ARRAYS · PART 24",
    topic="in-place merge: swap windows + gap method",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Two sorted arrays `a` (size n) and `b` (size m). Rearrange **in place** so that the combined "
        "n+m elements are sorted, first n in `a`, rest in `b`. `a={1,3,5,7}, b={0,2,6,8,9}` -> "
        "`a={0,1,2,3}, b={5,6,7,8,9}`.")

    P.h2("1 · Brute — merge with a temp array", color=RED)
    P.bullets(["Standard merge of two sorted lists into temp, copy halves back. `O(n+m)` time, "
               "**O(n+m) space** — banned by the question, but say it to show you know the baseline."])

    P.h2("2 · Optimal 1 — 'insertion' swaps from the boundary", color=ORANGE)
    P.p("Compare from the END of `a` and the START of `b`: while `a[l] > b[r]` they are on the wrong "
        "sides — swap. Then each array is internally fixed with a small insertion-sort pass.")
    P.code("cpp", """
int l = n - 1, r = 0;
while (l >= 0 && r < m && a[l] > b[r]) { swap(a[l], b[r]); l--; r++; }
// now every element of a <= every element of b; tidy each side
sort(a.begin(), a.end());     // or insertion-sort shifts -> O(min(n,m)) swaps
sort(b.begin(), b.end());
""", caption="O(min(n,m)) + O(n log n + m log m) with sorts; insertion version tighter")
    P.callout("gotcha", "why not just sort both at the end without the swap loop?",
              "Sorting a and b separately keeps {1,3,5,7}|{0,2..} wrongly partitioned. The swap loop first "
              "guarantees 'all of a <= all of b'; only then do local sorts give the global order.")

    P.h2("3 · Optimal 2 — the GAP method (shell-sort style)", color=GREEN)
    P.p("Treat `a` followed by `b` as ONE virtual array of size `n+m`. Compare pairs `gap` apart and "
        "swap if out of order; halve the gap (rounded UP) until it hits 0. `O((n+m) log(n+m))`, O(1) space.")
    P.code("cpp", """
auto at = [&](int i) -> int& { return i < n ? a[i] : b[i - n]; };
int gap = (n + m) / 2 + (n + m) % 2;      // ceil
while (gap > 0) {
    for (int i = 0; i + gap < n + m; i++)
        if (at(i) > at(i + gap)) swap(at(i), at(i + gap));
    gap = gap == 1 ? 0 : (gap / 2 + gap % 2);
}
""", caption="three index zones: both-in-a, a-then-b, both-in-b — the at() helper hides them")
    P.dryrun("Gap walk on {1,3,5,7}|{0,2,6,8,9} (size 9)",
             ["gap", "effect", "state"],
             [["5", "(1,2)(3,6)(5,8)(7,9) all fine", "unchanged"],
              ["3", "3-0, 5-2, 7-6 swap", "1 0 2 6 | 3 5 7 8 9"],
              ["2", "6-5 swap", "1 0 2 5 | 3 6 7 8 9"],
              ["1", "1-0 swap, then 5-3 swap", "0 1 2 3 | 5 6 7 8 9"]],
             "Four sweeps, each O(n+m), gap = ceil(half) each time: 5,3,2,1 -> sorted split.")
    P.chips(["optimal1 ~ O(n log n + m log m)", "gap O((n+m) log(n+m))", "both O(1) space"])
    P.callout("trick", "which to present?",
              "Swap-window first (simpler, intuitive), then offer the gap method when they demand "
              "'no sorting at all'. The `at(i)` virtual-index helper is the elegance point.")
    P.divider()
    P.h2("Cheat sheet — video 24", color=PURPLE)
    P.table(["Approach", "Idea", "TC / SC"],
            [["Temp merge", "classic merge + copy back", "O(n+m)/O(n+m)"],
             ["Swap at boundary", "a-right vs b-left, then tidy", "O((n+m) log(n+m)) worst /O(1)"],
             ["Gap method", "virtual array, halving gap", "O((n+m) log(n+m))/O(1)"]],
            fracs=[0.26, 0.42, 0.32])
