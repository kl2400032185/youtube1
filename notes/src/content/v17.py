from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=17,
    slug="count-subarrays-sum-k",
    title="Count Subarrays with Sum = K (prefix-sum hashmap)",
    meta="Striver A2Z · Arrays Playlist #17 · 24:09 · youtube.com/watch?v=xvNwoz-ufXA",
    tag="ARRAYS · PART 17",
    topic="counting, not longest — the map stores COUNTS",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("**Count** subarrays whose sum equals k — negatives allowed. "
        "`{1,2,3}, k=3` -> `2` (`{1,2}` and `{3}`).")

    P.h2("1 · Brute — every (i,j) with running sum", color=RED)
    P.bullets(["Two loops, running sum, `if (sum==k) count++`. `O(n^2)`. Sliding window is WRONG here "
               "(negatives kill monotonicity)."])

    P.h2("2 · Optimal — prefix sum + COUNT hashmap", color=GREEN)
    P.p("Same skeleton as video 4's hashmap, but the map now stores **how many times** each prefix sum "
        "has occurred — because many equal prefixes each give a valid start.")
    P.bullets([
        "If `pre[j] - pre[i] == k`, subarray `i+1..j` sums to k.",
        "At each j: `count += map[pre - k]`, then `map[pre]++`.",
        "Seed with `map[0] = 1` (the empty prefix) — otherwise subarrays starting at index 0 are missed.",
    ])
    P.code("cpp", """
unordered_map<long long, int> cnt;
cnt[0] = 1;
long long pre = 0, ans = 0;
for (int x : arr) {
    pre += x;
    ans += cnt[pre - k];        // every earlier prefix (pre-k) closes a valid window
    cnt[pre]++;
}
return ans;
""", caption="O(n) average · O(n) space")
    P.dryrun("Dry run on {1,2,3}, k = 3",
             ["x", "pre", "pre-k", "cnt[pre-k]", "ans", "map after"],
             [["-", "0", "-", "-", "0", "{0:1}"],
              ["1", "1", "-2", "0", "0", "{0:1,1:1}"],
              ["2", "3", "0", "1", "1", "{0:1,1:1,3:1}"],
              ["3", "6", "3", "1", "2", "{...,6:1}"]],
             "ans = 2. Row x=2 hit prefix 0 (empty) -> [1,2]; row x=3 hit prefix 3 -> [3].")
    P.callout("gotcha", "longest vs count — swap the stored value",
              "LONGEST subarray (video 4) stores the FIRST index and never overwrites; COUNT stores the "
              "number of occurrences and always increments. Same skeleton, different payload — say which "
              "one you are writing.")
    P.callout("trick", "why cnt[0]=1 saves you",
              "When `pre == k` itself, the window starts at index 0 and `pre - k == 0` — the seeded zero is "
              "exactly what gets counted. Forgetting it is the most common bug in this family.")
    P.chips(["brute O(n^2)", "map O(n)/O(n)", "negatives OK"])
    P.divider()
    P.h2("The prefix-sum family so far", color=PURPLE)
    P.table(["Question", "Map stores", "Update"],
            [["Longest subarray sum k", "first index of each prefix", "set-if-absent"],
             ["Count subarrays sum k", "occurrence count of each prefix", "always ++"],
             ["Subarrays with XOR k (video 22)", "count of each prefix XOR", "always ++"]],
            fracs=[0.34, 0.36, 0.3])
    P.quote("One skeleton, three problems. Master the payload, not the problem.")
