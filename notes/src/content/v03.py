from render import RED, GREEN, TEAL, PURPLE, ORANGE, INK, INK_SOFT, GRAY

META = dict(
    num=3,
    slug="appears-once-missing-number-max-ones",
    title="Appears Once · Missing Number · Max Consecutive 1s",
    meta="Striver A2Z · Arrays Playlist #3 · 38:00 · youtube.com/watch?v=bYWLJb3vCWY",
    tag="ARRAYS · PART 3",
    topic="XOR magic, sum formulas and simple scans",
)


def build(P):
    P.h2("1 · Number that appears ONCE (all others twice)", color=RED)
    P.h3("Brute — count for everyone")
    P.bullets([
        "Take each element, linear-search how many times it appears. `O(n^2)` time.",
        "Better: frequency hash map — `O(n)` time, O(n) space.",
    ])
    P.h3("Optimal — XOR everything", color=GREEN)
    P.p("Two XOR laws are the whole trick: `a ^ a = 0` and `a ^ 0 = a`. Pairs cancel, the loner survives.")
    P.code("cpp", """
int xorr = 0;
for (int i = 0; i < n; i++) xorr = xorr ^ arr[i];
return xorr;                     // the element that appears once
""")
    P.dryrun("Dry run on {4,1,2,1,2}",
             ["step", "xorr", "binary view"],
             [["^4", "4", "100"],
              ["^1", "5", "101"],
              ["^2", "7", "111"],
              ["^1", "6", "110   (the 1s cancel)"],
              ["^2", "4", "100   -> answer 4"]],
             "Every duplicate flips its bits ON and then OFF again.")
    P.chips(["TC  O(n)", "SC  O(1)"])
    P.callout("trick", "XOR cheat list",
              "`a^a=0`, `a^0=a`, XOR is commutative + associative, and `x ^ y ^ x == y`. "
              "Any time pairs must cancel, think XOR.")

    P.divider()
    P.h2("2 · Missing number from 1..N", color=RED)
    P.p("Array has `n` numbers out of `1..n+1`… (LeetCode form: size `n` out of `0..n`). Find the missing one.")
    P.h3("Brute — linear search per candidate")
    P.bullets(["For each number 1..n+1 scan the array -> `O(n^2)`. Only say this to kill it."])
    P.h3("Better — hash / frequency")
    P.bullets(["Mark what you see, return the unseen. `O(n)` time, `O(n)` space."])
    P.h3("Optimal A — SUM formula", color=GREEN)
    P.code("cpp", """
long long expected = 1LL * n * (n + 1) / 2;   // n here = the FULL count
long long actual = 0;
for (int x : arr) actual += x;
return expected - actual;
""", caption="O(n) time · O(1) space · beware overflow -> use long long")
    P.h3("Optimal B — XOR (overflow-proof)", color=GREEN)
    P.bullets([
        "XOR all array elements (`xor1`) and all numbers 1..n+1 (`xor2`); answer = `xor1 ^ xor2`.",
        "The present numbers cancel in pairs; only the missing one remains. No overflow possible.",
    ])
    P.arr([3, 0, 1], captions={0: "2 is missing"}, label="example {3,0,1} -> 2")
    P.callout("note", "formula vs XOR",
              "Sum is the first thing to say; XOR is the flex for `huge n` where `n*(n+1)/2` could overflow "
              "the type you were given. Both O(n)/O(1).")

    P.divider()
    P.h2("3 · Max consecutive 1s (binary array)", color=RED)
    P.p("`{1,1,0,1,1,1}` -> `3`. The easiest problem of the set — a counter that resets on 0.")
    P.code("cpp", """
int cnt = 0, best = 0;
for (int i = 0; i < n; i++) {
    if (arr[i] == 1) { cnt++; best = max(best, cnt); }
    else cnt = 0;                      // chain broken
}
return best;
""")
    P.bullets([
        "Update `best` **inside** the 1-branch — no need for a final `max` after the loop.",
        "Same skeleton solves max consecutive anything with a condition (flip at most k zeros -> part 4/5 era).",
    ])
    P.chips(["TC  O(n)", "SC  O(1)"])
    P.divider()
    P.h2("Cheat sheet — video 3", color=PURPLE)
    P.table(["Problem", "Brute", "Optimal", "TC/SC"],
            [["Appears once", "count each O(n^2)", "XOR fold", "O(n)/O(1)"],
             ["Missing number", "search each O(n^2)", "sum formula or XOR", "O(n)/O(1)"],
             ["Max consecutive 1s", "-", "reset-on-zero scan", "O(n)/O(1)"]],
            fracs=[0.28, 0.26, 0.28, 0.18])
    P.quote("XOR cancels pairs, SUM cancels nothing. Choose the weapon that matches the enemy.")
