from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=28,
    slug="maximum-product-subarray",
    title="Maximum Product Subarray — the finale",
    meta="Striver A2Z · Arrays Playlist #28 · 20:27 · youtube.com/watch?v=hnswaLJvr6g",
    tag="ARRAYS · PART 28",
    topic="prefix/suffix products & the min/max flip",
)


def build(P):
    P.h2("Problem", color=TEAL)
    P.p("Largest product of a contiguous subarray. `{2,3,-2,4}` -> `6`. `{−2,0,−1}` -> `0`. "
        "Negatives flip signs, zeros kill products — Kadane alone is not enough.")

    P.h2("1 · Brute — every subarray", color=RED)
    P.bullets(["Two loops with a running product, track max. `O(n^2)`."])

    P.h2("2 · Optimal A — prefix & suffix products (Striver's intuition)", color=GREEN)
    P.p("Think: a zero splits the array into segments; inside a segment the max product subarray "
        "touches either its left or its right end (an even count of negatives on one side). "
        "So take running products from the LEFT and from the RIGHT; the answer is the max ever seen.")
    P.code("cpp", """
long long pre = 1, suf = 1, best = LLONG_MIN;
for (int i = 0; i < n; i++) {
    if (pre == 0) pre = 1;              // crossed a zero -> fresh segment
    if (suf == 0) suf = 1;
    pre *= arr[i];
    suf *= arr[n - 1 - i];
    best = max({best, pre, suf});
}
return (int)best;
""", caption="O(n) · O(1) space · zeros handled by the reset")
    P.dryrun("On {2,3,-2,4}",
             ["i", "pre (from left)", "suf (from right)", "best"],
             [["0", "2", "4", "4"],
              ["1", "6", "-8", "6"],
              ["2", "-12", "-24", "6"],
              ["3", "-48", "-48", "6"]],
             "pre row: 2, 2*3, *-2, *4. suf row: 4, 4*-2, *3, *2. Best ever seen = 6 = 2*3. "
             "The winning window always showed up at a PREFIX or SUFFIX boundary — that is the theorem.")
    P.arr([2, 3, -2, 4], marks={0: GREEN, 1: GREEN}, captions={0: "pre wins", 1: "6"}, label="max product = 2*3")

    P.h2("3 · Optimal B — Kadane with a MIN twin", color=GREEN)
    P.p("Carry BOTH the max and min product ending at i: a negative number swaps their roles "
        "(min*negative can become the new max).")
    P.code("cpp", """
long long maxi = arr[0], mini = arr[0], best = arr[0];
for (int i = 1; i < n; i++) {
    if (arr[i] < 0) swap(maxi, mini);              // sign flip exchanges the two
    maxi = max((long long)arr[i], maxi * arr[i]);
    mini = min((long long)arr[i], mini * arr[i]);
    best = max(best, maxi);
}
""", caption="O(n) · O(1) · the 'Kadane for products'")
    P.callout("trick", "two mental models, same answer",
              "A) prefix/suffix: the winner touches a segment boundary. B) min/max twin: every negative is "
              "a mirror. In interviews, present B for safety and A as the slick one-liner story.")
    P.callout("gotcha", "zeros",
              "In A, the `== 0 -> reset to 1` lines are the whole zero story. In B, `max(arr[i], ...)` "
              "restarts at 0 automatically. Forgetting either turns `{−2,0,−1}` into -2 instead of 0.")
    P.chips(["brute O(n^2)", "prefix/suffix O(n)", "min-max Kadane O(n)"])
    P.divider()
    P.h2("The 28-video arc — your arrays toolkit", color=PURPLE)
    P.table(["Pattern", "Videos", "Weapon"],
            [["one pass carries", "1,3,8,10,12", "running max/sum/cnt"],
             ["two pointers", "2,4,5,6,20,21", "sorted or monotone input"],
             ["prefix + hashmap", "4,17,22", "ask 'who was here before'"],
             ["voting / cancelling", "7,19", "duels until survivors"],
             ["index mapping on matrices", "14,15,16", "boundaries & mirrors"],
             ["merge-sort counting", "26,27", "count at first split level"],
             ["sign gymnastics", "9,28", "order or product flips"]],
            fracs=[0.3, 0.3, 0.4])
    P.quote("Arrays are not 28 tricks — they are 7 patterns wearing 28 costumes.")
