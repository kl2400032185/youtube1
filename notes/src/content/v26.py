from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=26,
    slug="count-inversions",
    title="Count Inversions (merge-sort counting)",
    meta="Striver A2Z · Arrays Playlist #26 · 24:17 · youtube.com/watch?v=AseUmwVNaoY",
    tag="ARRAYS · PART 26",
    topic="inversion pairs via modified merge sort",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("An **inversion** is a pair `i < j` with `arr[i] > arr[j]` — how unsorted the array is. "
        "`{5,4,3,2,1}` -> 10 (every pair). `{5,3,2,1}` -> 6.")

    P.h2("1 · Brute — nested loops", color=RED)
    P.code("cpp", """
long long cnt = 0;
for (int i = 0; i < n; i++)
    for (int j = i + 1; j < n; j++)
        if (arr[i] > arr[j]) cnt++;
""", caption="O(n^2) · the definition, verbatim")

    P.h2("2 · Optimal — count DURING merge sort", color=GREEN)
    P.p("Inside `merge()`, left and right halves are sorted. When `left[i] > right[j]`, then left[i] "
        "and **every element after it in the left half** also beat right[j] (sorted!) — so that is "
        "`mid - i + 1` inversions at once. Never compare across a merge again.")
    P.code("cpp", """
long long merge(vector<int> &a, int lo, int mid, int hi) {
    vector<int> tmp;
    int i = lo, j = mid + 1;
    long long cnt = 0;
    while (i <= mid && j <= hi) {
        if (a[i] <= a[j]) tmp.push_back(a[i++]);
        else {
            cnt += mid - i + 1;        // a[i..mid] all > a[j]
            tmp.push_back(a[j++]);
        }
    }
    while (i <= mid) tmp.push_back(a[i++]);
    while (j <= hi)  tmp.push_back(a[j++]);
    copy(tmp.begin(), tmp.end(), a.begin() + lo);
    return cnt;
}
// in mergeSort: total = left + right + merge(...)
""", caption="O(n log n) time · O(n) temp space")
    P.dryrun("merge of [3 | 1 2] (lo..mid=1..1? picture it)",
             ["compare", "decision", "count added"],
             [["3 vs 1", "3 > 1 -> take 1; left has 1 element >= i", "+ (mid-i+1) = 1"],
              ["3 vs 2", "3 > 2 -> take 2", "+1"],
              ["3 vs -", "flush left", "+0"]],
             "Two inversions: (3,1) and (3,2). One comparison each — that is the speed.")
    P.arr([5, 3, 2, 1], label="sorted halves during recursion do the counting")
    P.callout("trick", "why left <= right (not <) on the take-left branch",
              "Equal values are NOT inversions. Taking left first on equality keeps the count exact and "
              "keeps the merge stable.")
    P.callout("note", "the count lives in the MERGE step",
              "Do not try to count during the recursive splits — pairs are counted exactly once, at the "
              "first merge level where they land in different halves.")
    P.chips(["brute O(n^2)", "merge sort O(n log n)"])
    P.divider()
    P.h2("Cheat sheet — video 26", color=PURPLE)
    P.table(["Approach", "Idea", "TC/SC"],
            [["Nested loops", "count every violating pair", "O(n^2)/O(1)"],
             ["Merge sort", "left[i] > right[j] adds mid-i+1", "O(n log n)/O(n)"]],
            fracs=[0.3, 0.46, 0.24])
