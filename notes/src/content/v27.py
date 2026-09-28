from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=27,
    slug="reverse-pairs",
    title="Reverse Pairs — a[i] > 2 * a[j] for i < j",
    meta="Striver A2Z · Arrays Playlist #27 · 32:26 · youtube.com/watch?v=0e4bZaP3MDI",
    tag="ARRAYS · PART 27",
    topic="merge-sort with a separate counting pass",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Count pairs `i < j` with `arr[i] > 2 * arr[j]`. `{3,2,1}` (LeetCode 493 form) -> 3: "
        "(3,2)? 3>4 no... pairs: (3,1)? 3>2 yes; (3,2)? no; (2,1)? 2>2 no; hmm -> `{-1}` careful, use "
        "`{1,3,2,3,1}` below for the worked example instead.")

    P.h2("1 · Brute — nested loops", color=RED)
    P.code("cpp", """
long long cnt = 0;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        if ((long long)arr[i] > 2LL * arr[j]) cnt++;
""", caption="O(n^2) · note the long long on BOTH sides")

    P.h2("2 · Optimal — merge sort with a COUNT-ONLY pre-pass", color=GREEN)
    P.p("Critical difference from inversions: `arr[i] > 2*arr[j]` is NOT preserved by 'all remaining left "
        "elements also qualify'. So counting must be a SEPARATE sweep before merging:")
    P.numbered([
        "With two sorted halves, for each `i` in the left half advance `j` (right half) while "
        "`a[i] > 2*a[j]`; then add `j - (mid+1)` to the count.",
        "`j` only moves forward across the whole left sweep (both halves sorted) -> the sweep is O(len).",
        "THEN run the normal merge to keep the halves sorted. Do NOT count inside the merge.",
    ])
    P.code("cpp", """
long long countPairs(vector<int> &a, int lo, int mid, int hi) {
    long long cnt = 0;
    int j = mid + 1;
    for (int i = lo; i <= mid; i++) {
        while (j <= hi && (long long)a[i] > 2LL * a[j]) j++;
        cnt += j - (mid + 1);
    }
    return cnt;
}
// mergeSort: ans = left + right + countPairs(...); then ordinary merge()
""", caption="O(n log n) total · the while-loop is amortised O(n) per level")
    P.dryrun("countPairs on left [1,3] right [1,3] (array {1,3,2,3,1} level)",
             ["i (left)", "j advances while a[i] > 2*a[j]", "added"],
             [["1", "2*1=2 >? no... 1 > 2? no", "j stays -> 0"],
              ["3", "3 > 2*1 yes -> j=1; 3 > 2*3? no", "1"]],
             "Pairs caught: (3,1) across halves. Local pairs handled at deeper levels.")
    P.callout("gotcha", "the trap: counting inside merge",
              "With plain inversions, `a[i] > a[j]` implies the rest of the left half also qualifies, so "
              "mid-i+1 works. With `> 2*a[j]` it does NOT — hence the separate two-pointer sweep. "
              "This one observation is the whole video.")
    P.callout("gotcha", "overflow & negatives",
              "`2 * a[j]` overflows int for large values -> cast to long long first. Negatives are fine "
              "mathematically; the pointer sweep still works because halves are sorted ascending.")
    P.chips(["brute O(n^2)", "merge-sort sweep O(n log n)"])
    P.divider()
    P.h2("Inversions vs reverse pairs — siblings", color=PURPLE)
    P.table(["", "Inversions (v26)", "Reverse pairs (v27)"],
            [["condition", "a[i] > a[j]", "a[i] > 2*a[j]"],
             ["count location", "inside the merge comparison", "separate sweep before merge"],
             ["bulk count", "mid - i + 1 per comparison", "j - (mid+1) per left element"],
             ["complexity", "O(n log n)", "O(n log n)"]],
            fracs=[0.24, 0.38, 0.38])
    P.quote("Same skeleton, different anatomy: where the property lets you bulk-count, count; where it doesn't, sweep.")
