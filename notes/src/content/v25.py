from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=25,
    slug="missing-and-repeating",
    title="Find the Missing and Repeating Number — 4 approaches",
    meta="Striver A2Z · Arrays Playlist #25 · 42:24 · youtube.com/watch?v=2D0D8HE6uak",
    tag="ARRAYS · PART 25",
    topic="one value twice, one value absent: math & XOR",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Array of 1..n where exactly one value repeats (X) and one is missing (Y). Return both. "
        "`{3,1,2,5,3}` -> missing 4, repeating 3.")

    P.h2("1 · Counting approaches", color=RED)
    P.bullets([
        "Hash / frequency array: find count 2 and count 0. `O(n)` time, **O(n) space**.",
        "Sign-marking in place: for value v, negate `arr[|v|-1]`; already negative -> v repeats. "
        "Then the positive slot = missing. `O(n)/O(1)` but MUTATES the input.",
    ])

    P.h2("2 · Math approach — two equations", color=ORANGE)
    P.bullets([
        "`S1 = sum(arr) - sum(1..n) = X - Y` and `S2 = sumSq(arr) - sumSq(1..n) = X^2 - Y^2`.",
        "`X + Y = S2 / S1`; solve the pair. `O(n)` time O(1) space, but squares **overflow** fast — "
        "mention the danger before offering it.",
    ])

    P.h2("3 · Optimal — XOR split (overflow-proof)", color=GREEN)
    P.numbered([
        "`xor1 = arr[0]^...^arr[n-1] ^ 1^...^n` = `X ^ Y` (everything else cancels in pairs).",
        "Take any set bit of `xor1` (rightmost: `xor1 & -xor1`) — X and Y DIFFER there.",
        "Partition numbers 1..n and array values by that bit; XOR each bucket -> the two answers.",
        "Final check: which bucket result is the repeater? count it in the array once (or use the input range).",
    ])
    P.code("cpp", """
int xr = 0;
for (int x : arr) xr ^= x;
for (int i = 1; i <= n; i++) xr ^= i;          // xr = X ^ Y
int bit = xr & -xr;                            // rightmost set bit
int b0 = 0, b1 = 0;
for (int x : arr) (x & bit ? b1 : b0) ^= x;
for (int i = 1; i <= n; i++) (i & bit ? b1 : b0) ^= i;
// b0, b1 are {X, Y} in unknown order -> disambiguate by counting one:
int cnt = count(arr.begin(), arr.end(), b0);
return cnt == 2 ? make_pair(b0, b1) : make_pair(b1, b0);   // (repeat, missing)
""", caption="O(n) time · O(1) space · no overflow")
    P.dryrun("XOR on {3,1,2,5,3} (n=5)",
             ["step", "value", "note"],
             [["arr xor", "3^1^2^5^3 = 6", "100^001^010^101^001"],
              ["1..5 xor", "1", "001"],
              ["X^Y", "6^1 = 7", "111 -> repeater 3 ^ missing 4"],
              ["bit", "1", "rightmost set bit"],
              ["bucket b1 (odd)", "3^1^5^3 ^ 1^3^5 = 1^3 -> wait: 3,1,5,3 from arr; 1,3,5 from range -> 3", "X or Y"],
              ["bucket b0 (even)", "2 ^ 2^4 = 4", "the other one"],
              ["count check", "count(3)=2", "so repeat=3, missing=4"]],
             "Each bucket cancels to exactly one of {3,4}.")
    P.callout("gotcha", "order is ambiguous",
              "XOR tells you the SET {X, Y}, never which is the repeater. One counting pass over the array "
              "for b0 settles it — do not skip that line.")
    P.callout("trick", "rightmost set bit idiom",
              "`xr & -xr` isolates the lowest 1-bit (two's complement). That bit is where X and Y differ, "
              "and any differing bit partitions the world into exactly two cancelling buckets.")
    P.chips(["hash O(n)/O(n)", "math O(n)/O(1) overflow risk", "XOR O(n)/O(1) clean"])
    P.divider()
    P.h2("Cheat sheet — video 25", color=PURPLE)
    P.table(["Approach", "Idea", "TC / SC", "Caveat"],
            [["Frequency", "counts 2 and 0", "O(n)/O(n)", "space"],
             ["Sign mark", "negate index slot", "O(n)/O(1)", "mutates input"],
             ["Sum equations", "S1, S2 system", "O(n)/O(1)", "overflow"],
             ["XOR buckets", "X^Y split by a bit", "O(n)/O(1)", "need count to order"]],
            fracs=[0.22, 0.3, 0.2, 0.28])
