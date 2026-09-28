from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=4,
    slug="longest-subarray-sum-k",
    title="Longest Subarray with Sum K (+ generating subarrays)",
    meta="Striver A2Z · Arrays Playlist #4 · 41:42 · youtube.com/watch?v=frf7qxiN2qU",
    tag="ARRAYS · PART 4",
    topic="subarray generation · brute/better/optimal for sum K",
)


def build(P):
    P.h2("0 · What even IS a subarray?", color=TEAL)
    P.bullets([
        "A **contiguous** part of the array. `n` elements -> `n*(n+1)/2` subarrays.",
        "Generating them all = fix start `i`, extend end `j`, keep a running sum (no 3rd loop!).",
    ])
    P.code("cpp", """
for (int i = 0; i < n; i++) {
    long long sum = 0;
    for (int j = i; j < n; j++) {      // extend the window
        sum += arr[j];
        if (sum == k) len = max(len, j - i + 1);
    }
}
""", caption="the 'better' O(n^2) generator — note there is NO 3rd loop")

    P.h2("1 · Brute — three nested loops", color=RED)
    P.bullets([
        "For every `(i, j)` recompute the sum with a 3rd loop -> `O(n^3)`. Mention once, never code it.",
    ])

    P.h2("2 · Better — two loops, running sum", color=ORANGE)
    P.bullets([
        "The code above: `O(n^2)` time, O(1) space. Works with negatives too. Keep as fallback.",
    ])

    P.h2("3 · Optimal (POSITIVES only) — two pointers / sliding window", color=GREEN)
    P.p("Only valid when every element is `>= 0`: then growing the window only **increases** the sum, "
        "so once `sum > k` we must shrink from the left. That monotonicity is the whole proof.")
    P.code("cpp", """
int l = 0, r = 0;
long long sum = arr[0], len = 0;
while (r < n) {
    while (l <= r && sum > k) { sum -= arr[l]; l++; }   // shrink until legal
    if (sum == k) len = max(len, r - l + 1);
    r++;
    if (r < n) sum += arr[r];
}
""", caption="amortised O(2n) · O(1) space")
    P.callout("gotcha", "why it FAILS with negatives",
              "With negatives the sum is no longer monotone: shrinking might RAISE the sum. "
              "Example `{-1, 3, -2, 4}` k=3 — the pointer dance skips the answer. Use hashing instead.")
    P.dryrun("Dry run on {1,2,3,1,1,1,1}, k = 4",
             ["r", "window", "sum", "len"],
             [["0", "[1]", "1", "0"],
              ["1", "[1,2]", "3", "0"],
              ["2", "6>4 -> shrink -> [3]", "3", "0"],
              ["3", "[3,1]", "4 == k", "2"],
              ["4", "shrink -> [1,1]", "2", "2"],
              ["5", "[1,1,1]", "3", "2"],
              ["6", "[1,1,1,1]", "4 == k", "4"]],
             "Answer 4: the last four 1s.")

    P.h2("4 · Optimal with NEGATIVES — prefix sum + hashmap", color=GREEN)
    P.bullets([
        "Idea: if `prefix[j] - prefix[i] == k` then subarray `i+1..j` has sum k.",
        "While walking, ask the map: `have we seen prefix - k before?` Longest = `j - stored_index`.",
        "Store only the **first** index of each prefix sum (earliest = longest window).",
    ])
    P.code("cpp", """
unordered_map<long long, int> first;   // prefix sum -> earliest index
first[0] = -1;                          // empty prefix before the array
long long pre = 0, len = 0;
for (int j = 0; j < n; j++) {
    pre += arr[j];
    if (first.count(pre - k))
        len = max(len, j - first[pre - k]);
    if (!first.count(pre)) first[pre] = j;   // keep the EARLIEST index
}
""", caption="O(n) average · O(n) space · handles negatives")
    P.arr([2, 3, -1, 4, -2, 4], label="example, k = 6 -> longest is [3,-1,4] or [4,-2,4], len 3")
    P.chips(["positives: O(2n)/O(1) two pointers", "any ints: O(n)/O(n) hashmap"])
    P.callout("interview", "which one first?",
              "Ask: 'any negatives in the array?'  If no -> sliding window. If yes -> prefix-sum hashmap. "
              "Asking this question IS the interview win.")
    P.divider()
    P.h2("Cheat sheet — video 4", color=PURPLE)
    P.table(["Approach", "Idea", "TC", "Works with negatives"],
            [["Brute 3 loops", "recompute each window", "O(n^3)", "yes"],
             ["2 loops + running sum", "extend j, carry sum", "O(n^2)", "yes"],
             ["Two pointers", "shrink while sum > k", "O(2n)", "NO — positives only"],
             ["Prefix sum + map", "seen[pre-k] -> window", "O(n)", "yes"]],
            fracs=[0.26, 0.32, 0.16, 0.26])
