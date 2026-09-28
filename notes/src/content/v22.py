from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=22,
    slug="subarrays-with-xor-k",
    title="Number of Subarrays with XOR = K",
    meta="Striver A2Z · Arrays Playlist #22 · 24:55 · youtube.com/watch?v=eZr-6p0B7ME",
    tag="ARRAYS · PART 22",
    topic="prefix XOR + count map (the sum-K skeleton with ^)",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Count subarrays whose XOR equals k. `{4,2,2,6,4}, k=6` -> `4` "
        "(`{4,2}`, `{2,2,6}`, `{6}`, `{4,2,2,6,4}`... check below).")

    P.h2("1 · Brute — all (i,j), running XOR", color=RED)
    P.bullets(["Two loops carrying `xorr ^= arr[j]`, count when `== k`. `O(n^2)`. "
               "No sliding window exists for XOR with arbitrary values."])

    P.h2("2 · Optimal — prefix XOR + COUNT map", color=GREEN)
    P.p("XOR is its own inverse: `a ^ a = 0`. So `xor(i..j) = pre[j] ^ pre[i]`, and we want "
        "`pre[j] ^ pre[i] == k` <=> `pre[i] == pre[j] ^ k`. Same question as the sum version, "
        "with ^ instead of -.")
    P.code("cpp", """
unordered_map<int, int> cnt;
cnt[0] = 1;                       // empty prefix
int pre = 0, ans = 0;
for (int x : arr) {
    pre ^= x;
    ans += cnt[pre ^ k];          // earlier prefixes that complete the XOR
    cnt[pre]++;
}
return ans;
""", caption="O(n) average · O(n) space")
    P.dryrun("Dry run on {4,2,2,6,4}, k = 6",
             ["x", "pre", "pre^k", "cnt", "ans", "map after"],
             [["-", "0", "-", "-", "0", "{0:1}"],
              ["4", "4", "2", "0", "0", "{0:1,4:1}"],
              ["2", "6", "0", "1", "1", "{...,6:1}"],
              ["2", "4", "2", "0", "1", "4:2"],
              ["6", "2", "4", "2", "3", "2:1"],
              ["4", "6", "0", "1", "4", "6:2"]],
             "ans = 4. Rows with hits: [4,2], [2,2,6]? (pre 6 vs pre0), [6] and the whole array.")
    P.callout("trick", "XOR identities to tattoo on your hand",
              "`a^a=0`, `a^0=a`, `(p^q)^q = p`, and the inversion trick `pre[i] = pre[j] ^ k`. "
              "Everything else is identical to the count-subarrays-sum-K video.")
    P.callout("note", "map vs sorting",
              "Sorting cannot help here — XOR has no order/monotonicity. Hashing is the only O(n) path "
              "(expected). If hashing is banned, O(n^2) brute is your honest answer.")
    P.chips(["brute O(n^2)", "prefix XOR map O(n)/O(n)"])
    P.divider()
    P.h2("The prefix family — complete", color=PURPLE)
    P.table(["Problem", "Prefix op", "Map key asked", "Map stores"],
            [["longest sum k (v4)", "+", "pre - k", "first index"],
             ["count sum k (v17)", "+", "pre - k", "count"],
             ["count XOR k (v22)", "^", "pre ^ k", "count"]],
            fracs=[0.28, 0.14, 0.28, 0.3])
    P.quote("Subtract for sums, XOR for xors. The map never changes its job: 'who was here before me?'")
